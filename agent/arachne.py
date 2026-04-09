import os
import asyncio
import json
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

ARACHNE_ENDPOINT = os.environ["ARACHNE_ENDPOINT"].rstrip("/")
ARACHNE_KEY = os.environ["KEY_LUCOS_ARACHNE"]
MCP_URL = f"{ARACHNE_ENDPOINT}/mcp"


async def _list_tools():
	headers = {"Authorization": f"Bearer {ARACHNE_KEY}"}
	async with httpx.AsyncClient(headers=headers) as http_client:
		async with streamable_http_client(MCP_URL, http_client=http_client) as (read, write, _):
			async with ClientSession(read, write) as session:
				await session.initialize()
				result = await session.list_tools()
				return result.tools


async def _call_tool(name, arguments):
	headers = {"Authorization": f"Bearer {ARACHNE_KEY}"}
	async with httpx.AsyncClient(headers=headers) as http_client:
		async with streamable_http_client(MCP_URL, http_client=http_client) as (read, write, _):
			async with ClientSession(read, write) as session:
				await session.initialize()
				result = await session.call_tool(name, arguments)
				if result.content:
					return result.content[0].text
				return "(no result)"


def get_tools():
	"""Return available MCP tools in Ollama's tool format."""
	tools = asyncio.run(_list_tools())
	return [
		{
			"type": "function",
			"function": {
				"name": tool.name,
				"description": tool.description or "",
				"parameters": tool.inputSchema,
			}
		}
		for tool in tools
	]


def call_tool(name, arguments):
	"""Call a named MCP tool and return the result as a string."""
	if isinstance(arguments, str):
		try:
			arguments = json.loads(arguments)
		except json.JSONDecodeError:
			arguments = {}
	return asyncio.run(_call_tool(name, arguments))
