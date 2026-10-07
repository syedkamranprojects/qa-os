# Read-only database connector (db-mcp)

QA OS reads two databases through this small MCP server:

| Connector name | Database | Used for |
|---|---|---|
| `snd-schema` | S&D application DB (PostgreSQL) | business data, master data, documents (base knowledge layer) |
| `selenium-framework-db` | `CTA_CONFIG_ASSERTION` (PostgreSQL) | legacy framework flows, screens, fields, events, group flows |

The same folder runs both: each connector gets its own connection settings through `env`.

**Read-only by construction.** Every query must be a single `SELECT`; `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `EXEC` and similar are rejected in code before they reach the database. Still, ask the DBA for a **read-only database user**.

Tools exposed: `list_tables`, `get_table_schema`, `run_readonly_query` (max 100 rows by default), `explain_query`.

## 1. Install (once)

Python 3.10+ is required.

```bat
cd qa-os\connectors\db-mcp
python -m venv venv
venv\Scripts\python -m pip install -r requirements.txt
```

## 2. Get your own read-only logins

Ask the DBA / QA lead for read-only credentials for both databases. **Never commit them, never paste them into chat.** You need, per database: host, port, database name, user, password, schema owner.

## 3. Register the connectors

Use the **full path** to your copy of `qa-os` in place of `<QAOS>` below.

### Claude Desktop app (Code tab)

Edit `%APPDATA%\Claude\claude_desktop_config.json` (Settings → Developer → Edit Config) and add under `mcpServers`:

```json
"snd-schema": {
  "command": "<QAOS>\\connectors\\db-mcp\\venv\\Scripts\\python.exe",
  "args": ["<QAOS>\\connectors\\db-mcp\\mcp_server.py"],
  "env": {
    "DB_TYPE": "postgres",
    "POSTGRES_HOST": "<host>",
    "POSTGRES_PORT": "<port>",
    "POSTGRES_DATABASE": "<snd database>",
    "POSTGRES_USER": "<read-only user>",
    "POSTGRES_PASSWORD": "<password>",
    "SCHEMA_OWNER": "<schema>"
  }
},
"selenium-framework-db": {
  "command": "<QAOS>\\connectors\\db-mcp\\venv\\Scripts\\python.exe",
  "args": ["<QAOS>\\connectors\\db-mcp\\mcp_server.py"],
  "env": {
    "DB_TYPE": "postgres",
    "POSTGRES_HOST": "<host>",
    "POSTGRES_PORT": "<port>",
    "POSTGRES_DATABASE": "<framework database>",
    "POSTGRES_USER": "<read-only user>",
    "POSTGRES_PASSWORD": "<password>",
    "SCHEMA_OWNER": "<schema>"
  }
}
```

Restart the Claude Desktop app.

### Claude Code in a terminal (alternative)

```bat
claude mcp add snd-schema --scope user -e DB_TYPE=postgres -e POSTGRES_HOST=<host> -e POSTGRES_PORT=<port> -e POSTGRES_DATABASE=<db> -e POSTGRES_USER=<user> -e POSTGRES_PASSWORD=<password> -e SCHEMA_OWNER=<schema> -- "<QAOS>\connectors\db-mcp\venv\Scripts\python.exe" "<QAOS>\connectors\db-mcp\mcp_server.py"
```

Repeat for `selenium-framework-db` with the framework database.

## 4. Check

In a Claude session, ask: *"list the tables in snd-schema that contain `cashmemo`"* and *"list tables in selenium-framework-db that contain `fct_pr_tf`"*. Both should answer with table names.

## Notes

- Schema lookups are cached per database in `%USERPROFILE%\.qa-os\db-cache\` (override with `QAOS_DB_CACHE_DIR`). Delete the folder to refresh after a release changes the schema.
- `fct_pr_lu_login_users` holds plain-text passwords: never `SELECT *` from it; name the columns and leave out `plu_password`.
- Origin: a trimmed copy of the team's `nl2sql-agent` MCP server (LLM parts removed; per-database cache; Oracle client path from `ORACLE_CLIENT_DIR`).
