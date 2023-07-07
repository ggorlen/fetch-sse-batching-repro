import json
from flask import (
    Flask,
    render_template,
    request,
    Response,
    stream_with_context,
)
from time import sleep


app = Flask(__name__)


def run_stream():
    for i in range(150):
        payload = {"data": f"{i}"}
        yield f'data: {json.dumps(payload)}\n\n'
        sleep(0.0002) # adjust to help reproduce


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/stream")
def stream():
    if request.headers.get("accept") != "text/event-stream":
        return {"error": "missing accept: text/event-stream header"}, 400

    with_context = stream_with_context(run_stream())
    r = Response(with_context, mimetype="text/event-stream")

    r.headers["Cache-Control"] = (
        "no-store, max-age=0, no-cache, no-store, must-revalidate"
    )
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"

    # also attempted just:
    #r.headers["Cache-Control"] = "no-store, max-age=0"
    return r


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
    )

