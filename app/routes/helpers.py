from functools import wraps
from flask import session, jsonify
from app.models import User


def get_current_user():
    """Get the currently logged-in user from session"""
    user_id = session.get('user_id')
    
    if not user_id:
        return None
    
    return User.query.get(user_id)


def login_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user_id exists in session
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                "error": "Unauthorized",
                "message": "Login required to access this resource"
            }), 401
        
        # Verify user exists in database
        user = User.query.get(user_id)
        
        if not user:
            # Invalid session, clear it
            session.pop('user_id', None)
            return jsonify({
                "error": "Unauthorized",
                "message": "Invalid session. Please login again"
            }), 401
        
        # User is authenticated, proceed with the request
        return f(*args, **kwargs)
    
    return decorated_function