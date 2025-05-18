from flask import Flask, request, jsonify
import logging
from logtail.handler import LogtailHandler

app = Flask(__name__)

# Configure Logtail handler
logtail_handler = LogtailHandler(source_token="qZn7dMCn3jThEW6SJWEs3YK6")
app.logger.addHandler(logtail_handler)
app.logger.setLevel(logging.INFO)

# In-memory data store
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book", "done": False}
]

@app.route("/")
def home():
    app.logger.info("Home route accessed")
    return "Welcome to the To-Do API!"

@app.route("/health")
def health():
    app.logger.info("Health check accessed")
    return "OK", 200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    app.logger.info("Fetching all tasks")
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    if not data or "title" not in data:
        app.logger.warning("Task creation failed: Title is missing")
        return {"error": "Title is required"}, 400
    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "done": False
    }
    tasks.append(task)
    app.logger.info("Task created", extra={"task": task})
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        app.logger.warning("Task update failed: Task not found", extra={"task_id": task_id})
        return {"error": "Task not found"}, 404
    data = request.json
    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])
    app.logger.info("Task updated", extra={"task": task})
    return jsonify(task)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception("An error occurred")
    return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
