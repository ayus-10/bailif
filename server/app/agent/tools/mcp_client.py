"""
Structured, ad-hoc query tool via CockroachDB's Cloud Managed MCP Server.

Flow this stub represents:
  1. Pass the natural-language request (or an LLM-generated query plan)
     to the MCP server as a tool call.
  2. The MCP server executes it against your cluster in read-only mode
     and returns rows.
  3. Return results to the agent to summarize for the user.

Left unimplemented on purpose - wire up the actual MCP client library /
HTTP calls once you've connected your cluster via the Cloud Console and
have real credentials. Endpoint + auth come from app.core.config.
"""

import httpx

from app.core.config import settings


async def run_structured_query(natural_language_request: str) -> list[dict]:
    async with httpx.AsyncClient(timeout=30) as client:
        # Shape of this call depends on the MCP server's actual tool schema -
        # check the CockroachDB MCP docs for the exact tool name/payload
        # once you've connected it via the Cloud Console.
        resp = await client.post(
            settings.mcp_server_url,
            headers={"Authorization": f"Bearer {settings.mcp_api_key}"},
            json={"request": natural_language_request},
        )
        resp.raise_for_status()
        return resp.json().get("rows", [])
