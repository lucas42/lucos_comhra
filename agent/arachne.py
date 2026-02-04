import os
import re
import json
import requests

ARACHNE_ENDPOINT = os.environ["ARACHNE_ENDPOINT"].rstrip("/")
ARACHNE_USER = os.environ["SYSTEM"]
ARACHNE_KEY = os.environ["KEY_LUCOS_ARACHNE"]

SPARQL_RE = re.compile(r"`sparql\s+(.*?)`", re.DOTALL)

def extract_sparql(text):
	match = SPARQL_RE.search(text)
	if not match:
		return None
	return match.group(1).strip()

def run_sparql(query):
	headers = {
		"Accept": "application/sparql+json",
	}

	r = requests.post(
		f"{ARACHNE_ENDPOINT}/sparql",
		data={"query": query},
		headers=headers,
		auth=(ARACHNE_USER, ARACHNE_KEY),
		timeout=30,
	)
	r.raise_for_status()
	return r.json()

def create_result_message(results):
	return {
		"role": "system",
		"content": (
			"SPARQL results (JSON):\n"
			f"{json.dumps(results, indent=2)}\n\n"
			"Explain this to the user in clear natural language."
		),
	}

def create_error_message(exception):
	return {
		"role": "system",
		"content": (
			"Error from sparql endpoint:\n"
			f"{exception.response.text}\n\n"
			"""Explain this error to the user in clear natural language.  
			If the problem was due to the SPARQL query itself, then take responsibility for writing it wrong.  
			Otherwise, take no reponsibility and suggest to the user what could be done to stop similar errors in future.
			"""
		),
	}
