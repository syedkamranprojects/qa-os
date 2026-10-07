import uuid
import config
from db import get_connection


def get_query_plan(sql: str) -> list[str]:
    """
    Returns the database's execution plan for `sql` as a list of text lines,
    without actually running the query. Dialect-specific under the hood
    (Oracle EXPLAIN PLAN/DBMS_XPLAN, Postgres EXPLAIN, SQL Server
    SET SHOWPLAN_ALL), but always returns the same plain-text-lines shape
    regardless of DB_TYPE.
    """
    if config.DB_TYPE == "oracle":
        return _get_oracle_plan(sql)
    elif config.DB_TYPE == "postgres":
        return _get_postgres_plan(sql)
    elif config.DB_TYPE == "sqlserver":
        return _get_sqlserver_plan(sql)
    else:
        raise EnvironmentError(f"Unknown DB_TYPE '{config.DB_TYPE}'")


def _get_oracle_plan(sql: str) -> list[str]:
    # A unique STATEMENT_ID keeps this call from colliding with any other
    # session's rows in PLAN_TABLE (which isn't always a session-private
    # global temporary table, depending on how it was created).
    statement_id = f"mcp_{uuid.uuid4().hex[:24]}"

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN PLAN SET STATEMENT_ID = '{statement_id}' FOR {sql}")
        cursor.execute(
            "SELECT PLAN_TABLE_OUTPUT FROM TABLE(DBMS_XPLAN.DISPLAY(NULL, :sid))",
            sid=statement_id,
        )
        lines = [r[0] for r in cursor.fetchall()]
        cursor.execute("DELETE FROM PLAN_TABLE WHERE STATEMENT_ID = :sid", sid=statement_id)
        cursor.close()
        return lines
    finally:
        conn.close()


def _get_postgres_plan(sql: str) -> list[str]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN {sql}")
        lines = [r[0] for r in cursor.fetchall()]
        cursor.close()
        return lines
    finally:
        conn.close()


def _get_sqlserver_plan(sql: str) -> list[str]:
    # SHOWPLAN_ALL must be the only statement in its batch, and while it's ON
    # the very next statement isn't executed - SQL Server returns its plan
    # instead. StmtText already contains the indented plan tree as text.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SET SHOWPLAN_ALL ON")
        cursor.execute(sql)
        lines = [str(r.StmtText) for r in cursor.fetchall()]
        cursor.execute("SET SHOWPLAN_ALL OFF")
        cursor.close()
        return lines
    finally:
        conn.close()
