from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Create SQLAlchemy instance (database handler)
db = SQLAlchemy()

def create_app():
    # Create Flask application instance
    app = Flask(__name__)
    
    # Load configuration settings
    app.config.from_object('app.config.Config')
    
    # Initialize extensions with app
    db.init_app(app)
    CORS(app)
    
    # Simple test route to verify app is working
    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to Task Management API",
            "status": "running"
        })
    
    # Health check route
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})
    
    # ========== Global Error Handlers ==========
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": "The request was invalid or cannot be processed"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method Not Allowed",
            "message": "The HTTP method is not allowed for this endpoint"
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback any failed database transactions
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server"
        }), 500
    
    # ========== End Error Handlers ==========
    
    # Import and register blueprints
    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    
    # Import models and create database tables
    with app.app_context():
        from app import models
        db.create_all()
    
    return app