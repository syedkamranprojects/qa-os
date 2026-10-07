import re
from mcp.server.fastmcp import FastMCP
from schema_discovery import get_all_table_names, build_schema_memory
from query_plan import get_query_plan
from db import get_connection

mcp = FastMCP("db-schema")

# Keywords that must never appear in a query run through this server.
# This is a hard code-level block, not just an instruction to the model.
_FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE",
    "MERGE", "CREATE", "GRANT", "REVOKE", "EXEC", "CALL",
]


def _validate_select_only(sql: str) -> str:
    """
    Ensures `sql` is a single, plain SELECT statement before it's allowed
    anywhere near the database - shared by every tool below that accepts
    caller-supplied SQL. Returns the cleaned statement, or raises ValueError.
    """
    cleaned = sql.strip().rstrip(";")

    if not re.match(r"(?is)^\s*SELECT\b", cleaned):
        raise ValueError("Only SELECT statements are allowed through this tool.")

    upper_sql = cleaned.upper()
    for keyword in _FORBIDDEN_KEYWORDS:
        if re.search(r"\b" + keyword + r"\b", upper_sql):
            raise ValueError(f"Query rejected: contains forbidden keyword '{keyword}'.")

    return cleaned


@mcp.tool()
def list_tables(name_contains: str = "") -> list[str]:
    """
    List table names in the configured database schema.
    Optionally filter to names containing the given substring (case-insensitive).
    Use this first to find the correct table name before calling get_table_schema.
    """
    tables = get_all_table_names()
    if name_contains:
        # Case-insensitive on both sides: Oracle table names come back
        # uppercase, Postgres lowercase, SQL Server as originally created.
        tables = [t for t in tables if name_contains.lower() in t.lower()]
    return tables


@mcp.tool()
def get_table_schema(table_name: str) -> dict:
    """
    Get column definitions and foreign-key join relationships for a single
    table. Results are cached to disk (schema_cache.json) after first
    lookup, so repeated calls for the same table are fast.
    """
    memory = build_schema_memory([table_name])
    return memory.get(table_name.upper(), {})


@mcp.tool()
def run_readonly_query(sql: str, max_rows: int = 100) -> list[dict]:
    """
    Execute a read-only SELECT query against the configured database.
    Only SELECT statements are permitted - any write/DDL keyword is
    rejected before the query ever reaches the database. Results are
    capped at max_rows (default 100) to avoid pulling huge result sets.
    """
    cleaned = _validate_select_only(sql)

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(cleaned)
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchmany(max_rows)
        cursor.close()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()


@mcp.tool()
def explain_query(sql: str) -> list[str]:
    """
    Return the database's execution plan for a SELECT query, without
    actually running it. Useful for checking how a query will be executed
    (index usage, join order, estimated cost/rows) before optimizing it.
    Only SELECT statements are permitted, same as run_readonly_query.
    """
    cleaned = _validate_select_only(sql)
    return get_query_plan(cleaned)


if __name__ == "__main__":
    mcp.run()