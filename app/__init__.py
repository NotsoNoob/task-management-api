from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Create SQLAlchemy instance (database handler)
db = SQLAlchemy()

def create_app():
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    # Create Flask application instance
    app = Flask(__name__)
    
    # Load configuration settings
    app.config.from_object('app.config.Config')
    
    # Initialize extensions with app
    db.init_app(app)
    CORS(app, supports_credentials=True)
    
    # ========== Base Routes ==========
    
    @app.route('/')
    def home():
        """Welcome endpoint"""
        return jsonify({
            "message": "Welcome to Task Management API",
            "status": "running",
            "version": "1.0.0"
        })
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({"status": "healthy"})
    
    # ========== Error Handlers ==========
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors"""
        return jsonify({
            "error": "Bad Request",
            "message": "The request was invalid or cannot be processed"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors"""
        return jsonify({
            "error": "Method Not Allowed",
            "message": "The HTTP method is not allowed for this endpoint"
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors"""
        db.session.rollback()
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server"
        }), 500
    
    # ========== Register Blueprints ==========
    
    from app.routes.tasks import tasks_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)
    
    # ========== Initialize Database ==========
    
    with app.app_context():
        from app import models
        db.create_all()
    
    return app