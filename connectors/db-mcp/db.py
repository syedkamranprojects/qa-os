import config

_oracle_client_initialized = False


def _ensure_oracle_client_initialized():
    global _oracle_client_initialized
    if not _oracle_client_initialized:
        import oracledb
        # Instant Client folder comes from ORACLE_CLIENT_DIR (only needed for Oracle)
        oracledb.init_oracle_client(lib_dir=config.ORACLE_CLIENT_DIR)
        _oracle_client_initialized = True


def _get_oracle_connection():
    import oracledb
    _ensure_oracle_client_initialized()
    dsn = f"{config.ORACLE_HOST}:{config.ORACLE_PORT}/{config.ORACLE_SERVICE}"
    return oracledb.connect(
        user=config.ORACLE_USER,
        password=config.ORACLE_PASSWORD,
        dsn=dsn,
    )


def _get_postgres_connection():
    import psycopg2
    return psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        dbname=config.POSTGRES_DATABASE,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
    )


def _get_sqlserver_connection():
    import pyodbc
    conn_str = (
        f"DRIVER={{{config.SQLSERVER_DRIVER}}};"
        f"SERVER={config.SQLSERVER_HOST},{config.SQLSERVER_PORT};"
        f"DATABASE={config.SQLSERVER_DATABASE};"
        f"UID={config.SQLSERVER_USER};"
        f"PWD={config.SQLSERVER_PASSWORD};"
    )
    return pyodbc.connect(conn_str)


def get_connection():
    if config.DB_TYPE == "oracle":
        return _get_oracle_connection()
    elif config.DB_TYPE == "postgres":
        return _get_postgres_connection()
    elif config.DB_TYPE == "sqlserver":
        return _get_sqlserver_connection()
    else:
        raise EnvironmentError(
            f"Unknown DB_TYPE '{config.DB_TYPE}'. Use 'oracle', 'postgres', or 'sqlserver'."
        )
