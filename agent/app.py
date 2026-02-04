import os
from flask import Flask, request, render_template_string
#from agent import run_agent

PORT = int(os.environ["PORT"])

app = Flask(__name__)

HTML = """
<!doctype html>
<title>lucos_comhra</title>
<h1>lucos_comhra</h1>

<form method="post">
	<textarea name="prompt" rows="8" cols="80">{{ prompt }}</textarea><br>
	<button type="submit">Send</button>
</form>

{% if response %}
<h2>Response</h2>
<pre>{{ response }}</pre>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
	prompt = ""
	response = None

	if request.method == "POST":
		prompt = request.form["prompt"]
		#response = run_agent(prompt)
		response = "You need to log in for access.  Unfortunately, login hasn't been implemented yet 🤷"

	return render_template_string(
		HTML,
		prompt=prompt,
		response=response,
	)

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
