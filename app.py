import re

from flask import Flask, jsonify, request, send_from_directory

from ideco_client import IDECOFetchError, fetch_receivable

app = Flask(__name__, static_folder="static", static_url_path="/static")


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/lookup")
def lookup():
    data = request.get_json(silent=True) or {}
    subscriber = (data.get("subscriber") or "").strip()

    if not re.fullmatch(r"\d{10}", subscriber):
        return jsonify({"error": "رقم الاشتراك يجب أن يتكون من 10 خانات رقمية"}), 400

    try:
        return jsonify(fetch_receivable(subscriber))
    except IDECOFetchError:
        return jsonify({"error": "تعذر الاتصال بموقع شركة الكهرباء، يرجى المحاولة لاحقاً"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12000)
