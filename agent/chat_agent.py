import os
import requests
import arachne


OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")


SYSTEM_PROMPT = """You are an assistant with access to a personal knowledge graph containing information about music, places, festivals, and more.

Use the available tools to look up information when needed. Always prefer the knowledge graph over your own knowledge — it is the authoritative source for this system.
"""


def call_llm(messages, tools=None):
	payload = {
		"model": OLLAMA_MODEL,
		"messages": messages,
		"stream": False,
	}
	if tools:
		payload["tools"] = tools

	r = requests.post(
		f"{OLLAMA_URL}/api/chat",
		json=payload,
		timeout=120,
	)
	r.raise_for_status()
	return r.json()["message"]


def run_agent(prompt):
	tools = arachne.get_tools()

	messages = [
		{"role": "system", "content": SYSTEM_PROMPT},
		{"role": "user", "content": prompt},
	]

	# Agentic loop: call LLM until it gives a text response with no tool calls
	for _ in range(5):
		message = call_llm(messages, tools=tools)

		tool_calls = message.get("tool_calls")
		if not tool_calls:
			return message.get("content", "")

		# Add the assistant's tool call message
		messages.append({
			"role": "assistant",
			"content": message.get("content", ""),
			"tool_calls": tool_calls,
		})

		# Execute each tool call and add results
		for tool_call in tool_calls:
			fn = tool_call["function"]
			tool_name = fn["name"]
			tool_args = fn.get("arguments", {})
			tool_id = tool_call.get("id", "")

			try:
				result = arachne.call_tool(tool_name, tool_args)
			except Exception as e:
				result = f"Error calling tool '{tool_name}': {e}"

			messages.append({
				"role": "tool",
				"content": result,
				"tool_call_id": tool_id,
			})

	# Final call without tools if we've hit the iteration limit
	message = call_llm(messages)
	return message.get("content", "")
