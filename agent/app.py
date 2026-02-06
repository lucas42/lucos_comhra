import os
from flask import Flask, request, render_template_string, make_response
import auth
from chat_agent import run_agent

PORT = int(os.environ["PORT"])

app = Flask(__name__, static_url_path='')

HTML = """
<!doctype html>
<html>
<head>
	<title>lucOS Comhrá</title>
</head>
<body>
	<lucos-navbar>lucOS Comhrá</lucos-navbar>

	Start a chat:
	<form method="post">
		<textarea name="prompt" rows="8" cols="80">{{ prompt }}</textarea><br>
		<button type="submit">Send</button>
	</form>

	{% if response %}
	<h2>Response</h2>
	<pre>{{ response }}</pre>
	{% endif %}
	<script src="/lucos_navbar.js" type="text/javascript"></script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
	try:
		auth.checkAuth()
	except auth.AuthException:
		return auth.authenticate()
	prompt = ""
	response = None

	if request.method == "POST":
		prompt = request.form["prompt"]
		response = run_agent(prompt)

	return auth.setAuthCookies(make_response(render_template_string(
		HTML,
		prompt=prompt,
		response=response,
	)))

@app.route("/_info", methods=["GET"])
def info():
	return {
		"system": os.environ["SYSTEM"],
		"title": "Comhrá",
		"ci": {
			"circle": f"gh/lucas42/{os.environ["SYSTEM"]}",
		},
		"checks": {
		},
		"metrics": {
		},
		"network_only": True,
		"show_on_homepage": False,
	}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=PORT)
