import os
from dotenv import load_dotenv

# Connection settings come from environment variables. The MCP client config
# (Claude Desktop / Claude Code) passes them per server in its "env" block, so
# snd-schema and selenium-framework-db can point at different databases from
# this one folder. A local .env file is only a fallback for testing by hand.
load_dotenv()

ORACLE_HOST = os.getenv("ORACLE_HOST")
ORACLE_PORT = os.getenv("ORACLE_PORT")
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE")
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_CLIENT_DIR = os.getenv("ORACLE_CLIENT_DIR", r"C:\oracle\instantclient_23_0")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

SQLSERVER_HOST = os.getenv("SQLSERVER_HOST")
SQLSERVER_PORT = os.getenv("SQLSERVER_PORT")
SQLSERVER_DATABASE = os.getenv("SQLSERVER_DATABASE")
SQLSERVER_USER = os.getenv("SQLSERVER_USER")
SQLSERVER_PASSWORD = os.getenv("SQLSERVER_PASSWORD")
SQLSERVER_DRIVER = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 17 for SQL Server")

# Which database backend to connect to: "oracle", "postgres", or "sqlserver"
DB_TYPE = os.getenv("DB_TYPE", "postgres").lower()

# The schema that owns the tables (catalog views return every schema you have
# grants on, so this filters them down).
_default_schema_owner = {
    "oracle": "HISAPI",
    "postgres": "public",
    "sqlserver": "dbo",
}.get(DB_TYPE, "public")
SCHEMA_OWNER = os.getenv("SCHEMA_OWNER", _default_schema_owner)

# Fail fast if something critical is missing, rather than a confusing error later.
if DB_TYPE == "oracle":
    _required = {
        "ORACLE_HOST": ORACLE_HOST,
        "ORACLE_PORT": ORACLE_PORT,
        "ORACLE_SERVICE": ORACLE_SERVICE,
        "ORACLE_USER": ORACLE_USER,
        "ORACLE_PASSWORD": ORACLE_PASSWORD,
    }
elif DB_TYPE == "postgres":
    _required = {
        "POSTGRES_HOST": POSTGRES_HOST,
        "POSTGRES_PORT": POSTGRES_PORT,
        "POSTGRES_DATABASE": POSTGRES_DATABASE,
        "POSTGRES_USER": POSTGRES_USER,
        "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
    }
elif DB_TYPE == "sqlserver":
    _required = {
        "SQLSERVER_HOST": SQLSERVER_HOST,
        "SQLSERVER_PORT": SQLSERVER_PORT,
        "SQLSERVER_DATABASE": SQLSERVER_DATABASE,
        "SQLSERVER_USER": SQLSERVER_USER,
        "SQLSERVER_PASSWORD": SQLSERVER_PASSWORD,
    }
else:
    raise EnvironmentError(
        f"Unknown DB_TYPE '{DB_TYPE}'. Use 'oracle', 'postgres', or 'sqlserver'."
    )

missing = [k for k, v in _required.items() if not v]
if missing:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing)}"
    )
