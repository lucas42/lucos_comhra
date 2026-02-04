import os
import requests
import arachne


OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")


SYSTEM_PROMPT = """You are an assistant exploring a personal RDF knowledge graph.

When you need data, emit a SPARQL query wrapped EXACTLY like this:

```sparql
PREFIX ...
SELECT ...
````

Do not explain the query.
Do not include anything outside the code block.
Only use SPARQL 1.1.
If you don't have the URI for a concept, query based on the rdfs:label attribute, rather than guessing.
When querying for a concept, also request its skos:pref_label attribtue.
"""

def call_llm(messages):
	payload = {
		"model": OLLAMA_MODEL,
		"messages": messages,
		"stream": False,
	}


	r = requests.post(
		f"{OLLAMA_URL}/api/chat",
		json=payload,
		timeout=120,
	)
	r.raise_for_status()

	return r.json()["message"]["content"]


def run_agent(prompt):
	messages = [
		{"role": "system", "content": SYSTEM_PROMPT},
		{"role": "user", "content": prompt},
	]

	first_reply = call_llm(messages)
	sparql = arachne.extract_sparql(first_reply)

	if not sparql:
		return first_reply

	try:
		results = arachne.run_sparql(sparql)

		messages.append({"role": "assistant", "content": first_reply})
		messages.append(arachne.create_result_message(results))
	except requests.exceptions.HTTPError as e:
		messages.append({"role": "assistant", "content": first_reply})
		messages.append(arachne.create_error_message(e))

	final_reply = call_llm(messages)
	return final_reply