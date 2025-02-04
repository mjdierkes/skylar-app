from flask import Blueprint, request, jsonify
from app.tasks import build_project_task
from uuid import uuid4

bp = Blueprint("projects", __name__)

@bp.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data or "app_name" not in data:
        return jsonify({"error": "Missing 'app_name' in request payload."}), 400

    app_name = data["app_name"]
    # Create a unique job ID
    job_id = str(uuid4())

    # Enqueue the build task
    task = build_project_task.apply_async(args=[app_name, job_id])
    
    return jsonify({
        "message": "Build job submitted.",
        "job_id": job_id,
        "celery_task_id": task.id
    }), 202