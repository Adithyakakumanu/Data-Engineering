from flask import Flask, request, jsonify, send_from_directory
from db import run_query
from llm import generate_sql
from prompt import build_prompt
import os

app = Flask(__name__)

# Serve frontend files
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("frontend", path)

@app.route("/chat", methods=["POST"])
def chat():
    user_question = request.json["message"]
    prompt = build_prompt(user_question)
    sql_query = generate_sql(prompt)

    try:
        result = run_query(sql_query)
        return jsonify({"sql": sql_query, "result": result})
    except Exception as e:
        return jsonify({"error": str(e), "sql": sql_query})

if __name__ == "__main__":
    app.run(debug=True)