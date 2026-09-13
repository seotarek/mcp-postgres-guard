# MCP Postgres Guard 🐘🛡️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/Model%20Context%20Protocol-Compatible-purple.svg)](https://modelcontextprotocol.io/)

**A security-first Model Context Protocol (MCP) server for PostgreSQL: query auditing, destructive command interception, and SQL injection prevention for autonomous AI agents.**

Developed by **Tarek Mohamed** ([@seotarek](https://github.com/seotarek))

---

## 📌 Why MCP Postgres Guard?

Allowing AI agents (Claude, Cursor, LangChain agents) direct SQL access creates severe operational risks: accidental table dropping, unbounded deletions, or SQL injection. **MCP Postgres Guard** intercepts and audits all agent-generated SQL queries before they reach your database:

```
[ AI Agent / Claude / Cursor ]
               │
               ▼
 ┌──────────────────────────────────────────────┐
 │           MCP Postgres Guard Server          │
 │  • Destructive Query Blocker (DROP/TRUNCATE) │
 │  • Unbounded DELETE/UPDATE Prevention        │
 │  • Stacked Query & RCE Probe Detection       │
 └──────────────────────┬───────────────────────┘
                        │ (Only If Verified Safe)
                        ▼
             [ Production Database ]
```

---

## 🛠️ MCP Tools

- `pg_validate_query`: Validates whether a SQL statement is safe to execute for an autonomous agent.
- `pg_check_read_only`: Enforces a strict read-only policy (SELECT / EXPLAIN only).

---

## 🚀 Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "postgres-guard": {
      "command": "python",
      "args": ["-m", "mcp_postgres_guard.server"],
      "cwd": "/path/to/mcp-postgres-guard"
    }
  }
}
```

---

## 📜 License
Licensed under the [MIT License](LICENSE).
