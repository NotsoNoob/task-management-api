from flask import Blueprint, request, jsonify
from app import db
from app.models import Task
from app.routes.helpers import login_required, get_current_user

# Create blueprint for task routes
tasks_bp = Blueprint('tasks', __name__)

# Allowed values for validation
VALID_STATUSES = ['pending', 'in_progress', 'completed']
VALID_PRIORITIES = ['low', 'medium', 'high']


# POST /api/tasks - Create new task
@tasks_bp.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    # Get current logged-in user
    current_user = get_current_user()
    
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required field
    if not data or not data.get('title'):
        return jsonify({"error": "Bad Request", "message": "Title is required"}), 400
    
    # Validate status if provided
    if data.get('status') and data.get('status') not in VALID_STATUSES:
        return jsonify({
            "error": "Bad Request",
            "message": f"Status must be one of: {', '.join(VALID_STATUSES)}"
        }), 400
    
    # Validate priority if provided
    if data.get('priority') and data.get('priority') not in VALID_PRIORITIES:
        return jsonify({
            "error": "Bad Request",
            "message": f"Priority must be one of: {', '.join(VALID_PRIORITIES)}"
        }), 400
    
    # Create new task for the current user
    task = Task(
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium'),
        user_id=current_user.id  # Assign to logged-in user
    )
    
    # Save to database
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201


# GET /api/tasks - Get all tasks for current user
@tasks_bp.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    # Get current logged-in user
    current_user = get_current_user()
    
    # Get only tasks belonging to current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # Convert to list of dictionaries
    return jsonify([task.to_dict() for task in tasks]), 200


# GET /api/tasks/<id> - Get single task
@tasks_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    # Get current logged-in user
    current_user = get_current_user()
    
    # Find task by ID
    task = Task.query.get(task_id)
    
    # Check if task exists
    if not task:
        return jsonify({"error": "Not Found", "message": f"Task with id {task_id} not found"}), 404
    
    # Check if task belongs to current user
    if task.user_id != current_user.id:
        return jsonify({"error": "Forbidden", "message": "You don't have permission to access this task"}), 403
    
    return jsonify(task.to_dict()), 200


# PUT /api/tasks/<id> - Update task
@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    # Get current logged-in user
    current_user = get_current_user()
    
    # Find task by ID
    task = Task.query.get(task_id)
    
    # Check if task exists
    if not task:
        return jsonify({"error": "Not Found", "message": f"Task with id {task_id} not found"}), 404
    
    # Check if task belongs to current user
    if task.user_id != current_user.id:
        return jsonify({"error": "Forbidden", "message": "You don't have permission to modify this task"}), 403
    
    # Get JSON data from request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Bad Request", "message": "No data provided"}), 400
    
    # Validate status if provided
    if data.get('status') and data.get('status') not in VALID_STATUSES:
        return jsonify({
            "error": "Bad Request",
            "message": f"Status must be one of: {', '.join(VALID_STATUSES)}"
        }), 400
    
    # Validate priority if provided
    if data.get('priority') and data.get('priority') not in VALID_PRIORITIES:
        return jsonify({
            "error": "Bad Request",
            "message": f"Priority must be one of: {', '.join(VALID_PRIORITIES)}"
        }), 400
    
    # Update fields if provided
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
    if 'priority' in data:
        task.priority = data['priority']
    if 'due_date' in data:
        task.due_date = data['due_date']
    
    # Save changes
    db.session.commit()
    
    return jsonify(task.to_dict()), 200


# DELETE /api/tasks/<id> - Delete task
@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    # Get current logged-in user
    current_user = get_current_user()
    
    # Find task by ID
    task = Task.query.get(task_id)
    
    # Check if task exists
    if not task:
        return jsonify({"error": "Not Found", "message": f"Task with id {task_id} not found"}), 404
    
    # Check if task belongs to current user
    if task.user_id != current_user.id:
        return jsonify({"error": "Forbidden", "message": "You don't have permission to delete this task"}), 403
    
    # Delete from database
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"message": f"Task {task_id} deleted successfully"}), 200