from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User

# Create blueprint for auth routes
auth_bp = Blueprint('auth', __name__)


# POST /api/auth/register - Register new user
@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({"error": "Bad Request", "message": "No data provided"}), 400
    
    if not data.get('username'):
        return jsonify({"error": "Bad Request", "message": "Username is required"}), 400
    
    if not data.get('email'):
        return jsonify({"error": "Bad Request", "message": "Email is required"}), 400
    
    if not data.get('password'):
        return jsonify({"error": "Bad Request", "message": "Password is required"}), 400
    
    # Check if username already exists
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "Conflict", "message": "Username already exists"}), 409
    
    # Check if email already exists
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Conflict", "message": "Email already exists"}), 409
    
    # Create new user
    user = User(
        username=data.get('username'),
        email=data.get('email')
    )
    user.set_password(data.get('password'))
    
    # Save to database
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201


# POST /api/auth/login - Login user
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({"error": "Bad Request", "message": "No data provided"}), 400
    
    if not data.get('email'):
        return jsonify({"error": "Bad Request", "message": "Email is required"}), 400
    
    if not data.get('password'):
        return jsonify({"error": "Bad Request", "message": "Password is required"}), 400
    
    # Find user by email
    user = User.query.filter_by(email=data.get('email')).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data.get('password')):
        return jsonify({"error": "Unauthorized", "message": "Invalid email or password"}), 401
    
    # Store user ID in session (this logs them in)
    session['user_id'] = user.id
    
    return jsonify({
        "message": "Logged in successfully",
        "user": user.to_dict()
    }), 200


# POST /api/auth/logout - Logout user
@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    # Remove user ID from session
    session.pop('user_id', None)
    
    return jsonify({"message": "Logged out successfully"}), 200


# GET /api/auth/me - Get current user
@auth_bp.route('/api/auth/me', methods=['GET'])
def get_current_user():
    # Check if user is logged in
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"error": "Unauthorized", "message": "Not logged in"}), 401
    
    # Find user by ID
    user = User.query.get(user_id)
    
    if not user:
        # Session has invalid user ID, clear it
        session.pop('user_id', None)
        return jsonify({"error": "Unauthorized", "message": "User not found"}), 401
    
    return jsonify(user.to_dict()), 200