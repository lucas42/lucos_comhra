import os
from flask import Flask, request, render_template, make_response
import auth
from chat_agent import run_agent

PORT = int(os.environ["PORT"])

app = Flask(__name__, static_url_path='')


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

	return auth.setAuthCookies(make_response(render_template(
		"index.html",
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
