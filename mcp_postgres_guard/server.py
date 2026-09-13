import sys
import json
from typing import Dict, Any
from .security_analyzer import PostgresSecurityAnalyzer

TOOLS = [
    {
        "name": "pg_validate_query",
        "description": "Validates an AI-generated SQL query for safety, checking against destructive commands (DROP, TRUNCATE, stacked queries) before execution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "The SQL query to audit."}
            },
            "required": ["sql"]
        }
    },
    {
        "name": "pg_check_read_only",
        "description": "Verifies that an agent query is strictly non-mutating (SELECT / EXPLAIN only).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "The SQL query to verify."}
            },
            "required": ["sql"]
        }
    }
]

def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    sql = arguments.get("sql", "")
    audit = PostgresSecurityAnalyzer.audit_query(sql)

    if name == "pg_validate_query":
        return audit
    elif name == "pg_check_read_only":
        return {
            "is_read_only": audit["is_read_only"],
            "allow_execution": audit["is_read_only"] and audit["is_safe_for_agent_execution"],
            "threats": audit["detected_threats"]
        }
    else:
        raise ValueError(f"Unknown tool: {name}")

def run_stdio_server():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "mcp-postgres-guard", "version": "0.1.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                res = handle_call_tool(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]
                    }
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method '{method}' not found"}
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": req.get("id") if 'req' in locals() else None,
                "error": {"code": -32000, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run_stdio_server()
