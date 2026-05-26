import os
from flask import Flask, render_template, request, send_file
from io import BytesIO

from content_agent import create_gameplan

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    plan = None
    niche = ""
    goal = ""
    error = None

    if request.method == "POST":
        niche = request.form.get("niche", "").strip()
        goal = request.form.get("goal", "").strip()
        if not niche:
            error = "Please enter a niche for the gameplan."
        else:
            try:
                plan = create_gameplan(niche, goal)
            except Exception as exc:
                error = str(exc)

    return render_template("index.html", plan=plan, niche=niche, goal=goal, error=error)

@app.route("/download", methods=["POST"])
def download():
    niche = request.form.get("niche", "").strip()
    goal = request.form.get("goal", "").strip()
    if not niche:
        return "Niche is required", 400

    plan = create_gameplan(niche, goal)
    buffer = BytesIO(plan.encode("utf-8"))
    buffer.seek(0)
    filename = f"7-day-content-gameplan-{niche.replace(' ', '_')}.md"
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="text/markdown",
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
