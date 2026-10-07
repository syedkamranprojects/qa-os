from db import get_connection
import config
import json
import os

# One cache file per database/schema, so several connectors (snd-schema,
# selenium-framework-db, ...) running from this same folder never mix tables.
_cache_key = "_".join(
    str(p).replace("\\", "_").replace("/", "_").replace(":", "_")
    for p in (
        config.DB_TYPE,
        config.POSTGRES_DATABASE or config.ORACLE_SERVICE or config.SQLSERVER_DATABASE or "db",
        config.SCHEMA_OWNER,
    )
)
CACHE_FILE = os.path.join(
    os.getenv("QAOS_DB_CACHE_DIR", os.path.join(os.path.expanduser("~"), ".qa-os", "db-cache")),
    f"schema_cache_{_cache_key}.json",
)
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)


def load_schema_cache() -> dict:
    """Loads the persistent schema memory from disk, if it exists yet."""
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_schema_cache(cache: dict) -> None:
    """Writes the current schema memory to disk so it persists across runs."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def _normalize_identifier(name: str) -> str:
    """
    Folds a table/schema name to the case the active database actually stores
    it in for unquoted identifiers: Oracle -> upper, Postgres -> lower,
    SQL Server -> left as-is (default collation is case-insensitive anyway).
    """
    if config.DB_TYPE == "oracle":
        return name.upper()
    elif config.DB_TYPE == "postgres":
        return name.lower()
    return name


def _execute(cursor, query: str, **params):
    """
    Runs `query` with `params` using whatever bind-parameter style the active
    driver expects:
      - oracledb (Oracle):   named binds, e.g. :owner            -> keyword args
      - psycopg2 (Postgres): named binds, e.g. %(owner)s         -> a dict
      - pyodbc (SQL Server): positional binds, e.g. ?            -> a list,
        in the same order the params were passed to this function (Python
        dicts preserve insertion order, so callers below list kwargs in the
        same left-to-right order the '?' marks appear in the SQL text).
    """
    if config.DB_TYPE == "oracle":
        cursor.execute(query, **params)
    elif config.DB_TYPE == "postgres":
        cursor.execute(query, params)
    elif config.DB_TYPE == "sqlserver":
        cursor.execute(query, list(params.values()))
    else:
        raise EnvironmentError(f"Unknown DB_TYPE '{config.DB_TYPE}'")


def get_all_table_names(owner: str = None) -> list[str]:
    """
    Returns every table name in the given schema. Used to give the LLM a
    menu of tables to choose from when identifying which ones are relevant
    to a question — cheap to fetch since it's just names, no columns/joins.
    """
    owner = _normalize_identifier(owner or config.SCHEMA_OWNER)

    if config.DB_TYPE == "oracle":
        query = "SELECT table_name FROM all_tables WHERE owner = :owner ORDER BY table_name"
    elif config.DB_TYPE == "postgres":
        query = """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = %(owner)s AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """
    elif config.DB_TYPE == "sqlserver":
        query = """
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = ? AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """
    else:
        raise EnvironmentError(f"Unknown DB_TYPE '{config.DB_TYPE}'")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        _execute(cursor, query, owner=owner)
        rows = cursor.fetchall()
        cursor.close()
    finally:
        conn.close()
    return [r[0] for r in rows]


def get_columns(table_name: str, owner: str = None) -> list[dict]:
    """
    Returns column metadata for a given table (bare name, no schema prefix).
    Oracle is queried via ALL_TAB_COLUMNS; Postgres/SQL Server share the same
    ANSI INFORMATION_SCHEMA.COLUMNS query. Filtered by owner/schema in all
    three cases to avoid duplicate rows when the same table name exists in
    more than one schema you have grants on.
    """
    owner = _normalize_identifier(owner or config.SCHEMA_OWNER)
    table_name = _normalize_identifier(table_name)

    if config.DB_TYPE == "oracle":
        query = """
            SELECT DISTINCT column_name, data_type, nullable, column_id
            FROM all_tab_columns
            WHERE table_name = :table_name
              AND owner = :owner
            ORDER BY column_id
        """
    elif config.DB_TYPE == "postgres":
        query = """
            SELECT column_name, data_type, is_nullable, ordinal_position
            FROM information_schema.columns
            WHERE table_name = %(table_name)s
              AND table_schema = %(owner)s
            ORDER BY ordinal_position
        """
    elif config.DB_TYPE == "sqlserver":
        query = """
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, ORDINAL_POSITION
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
              AND TABLE_SCHEMA = ?
            ORDER BY ORDINAL_POSITION
        """
    else:
        raise EnvironmentError(f"Unknown DB_TYPE '{config.DB_TYPE}'")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        _execute(cursor, query, table_name=table_name, owner=owner)
        rows = cursor.fetchall()
        cursor.close()
    finally:
        conn.close()

    return [
        {"column_name": r[0], "data_type": r[1], "nullable": r[2]}
        for r in rows
    ]


def get_joins(table_name: str, owner: str = None) -> list[dict]:
    """
    Returns foreign-key join relationships involving this table, in either
    direction (as the child/referencing table, or as the parent/referenced
    table). Each result describes: child_table.child_column -> parent_table.parent_column

    Oracle is queried via ALL_CONS_COLUMNS/ALL_CONSTRAINTS. Postgres and SQL
    Server share the same ANSI INFORMATION_SCHEMA query, matching composite
    (multi-column) keys by ordinal_position the same way the Oracle query
    matches them by `position`.
    """
    owner = _normalize_identifier(owner or config.SCHEMA_OWNER)
    table_name = _normalize_identifier(table_name)

    if config.DB_TYPE == "oracle":
        query = """
            SELECT a.table_name  AS child_table,
                   a.column_name AS child_column,
                   c_pk.table_name AS parent_table,
                   b.column_name AS parent_column,
                   a.constraint_name
            FROM all_cons_columns a
            JOIN all_constraints c
              ON a.constraint_name = c.constraint_name AND a.owner = c.owner
            JOIN all_constraints c_pk
              ON c.r_constraint_name = c_pk.constraint_name AND c.r_owner = c_pk.owner
            JOIN all_cons_columns b
              ON c_pk.constraint_name = b.constraint_name
              AND c_pk.owner = b.owner
              AND a.position = b.position
            WHERE c.constraint_type = 'R'
              AND a.owner = :owner
              AND (a.table_name = :table_name OR c_pk.table_name = :table_name)
        """
        exec_args = dict(table_name=table_name, owner=owner)
    elif config.DB_TYPE == "postgres":
        query = """
            SELECT kcu_child.table_name  AS child_table,
                   kcu_child.column_name AS child_column,
                   kcu_parent.table_name AS parent_table,
                   kcu_parent.column_name AS parent_column,
                   rc.constraint_name
            FROM information_schema.referential_constraints rc
            JOIN information_schema.key_column_usage kcu_child
              ON rc.constraint_name = kcu_child.constraint_name
              AND rc.constraint_schema = kcu_child.constraint_schema
            JOIN information_schema.key_column_usage kcu_parent
              ON rc.unique_constraint_name = kcu_parent.constraint_name
              AND rc.unique_constraint_schema = kcu_parent.constraint_schema
              AND kcu_child.ordinal_position = kcu_parent.ordinal_position
            WHERE kcu_child.table_schema = %(owner)s
              AND (kcu_child.table_name = %(table_name)s OR kcu_parent.table_name = %(table_name)s)
        """
        # psycopg2 substitutes every occurrence of a named placeholder from
        # the same dict key, so table_name appearing twice is fine here.
        exec_args = dict(table_name=table_name, owner=owner)
    elif config.DB_TYPE == "sqlserver":
        query = """
            SELECT kcu_child.table_name  AS child_table,
                   kcu_child.column_name AS child_column,
                   kcu_parent.table_name AS parent_table,
                   kcu_parent.column_name AS parent_column,
                   rc.constraint_name
            FROM information_schema.referential_constraints rc
            JOIN information_schema.key_column_usage kcu_child
              ON rc.constraint_name = kcu_child.constraint_name
              AND rc.constraint_schema = kcu_child.constraint_schema
            JOIN information_schema.key_column_usage kcu_parent
              ON rc.unique_constraint_name = kcu_parent.constraint_name
              AND rc.unique_constraint_schema = kcu_parent.constraint_schema
              AND kcu_child.ordinal_position = kcu_parent.ordinal_position
            WHERE kcu_child.table_schema = ?
              AND (kcu_child.table_name = ? OR kcu_parent.table_name = ?)
        """
        # pyodbc needs one positional value per '?', in left-to-right order:
        # owner once, then table_name twice (child side OR parent side).
        exec_args = None
        positional_params = [owner, table_name, table_name]
    else:
        raise EnvironmentError(f"Unknown DB_TYPE '{config.DB_TYPE}'")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        if config.DB_TYPE == "sqlserver":
            cursor.execute(query, positional_params)
        else:
            _execute(cursor, query, **exec_args)
        rows = cursor.fetchall()
        cursor.close()
    finally:
        conn.close()

    return [
        {
            "child_table": r[0],
            "child_column": r[1],
            "parent_table": r[2],
            "parent_column": r[3],
            "constraint_name": r[4],
        }
        for r in rows
    ]


def build_schema_memory(table_names: list[str], use_cache: bool = True) -> dict:
    """
    Builds a schema 'memory' dict for a list of tables: each table maps to
    its columns and its join relationships. This is the structure the
    LangGraph agent injects into its SQL-generation prompt.

    With use_cache=True (default), previously discovered tables are read
    from schema_cache.json on disk instead of re-querying the database -
    this matters a lot on a 1000+ table schema, where re-discovering the
    same handful of frequently-used tables every run would be wasteful.
    Newly discovered tables are added to the cache and saved back to disk.
    """
    cache = load_schema_cache() if use_cache else {}
    memory = {}
    cache_updated = False

    for table_name in table_names:
        key = table_name.upper()
        if use_cache and key in cache:
            memory[key] = cache[key]
            continue

        memory[key] = {
            "columns": get_columns(table_name),
            "joins": get_joins(table_name),
        }
        cache[key] = memory[key]
        cache_updated = True

    if use_cache and cache_updated:
        save_schema_cache(cache)

    return memory
