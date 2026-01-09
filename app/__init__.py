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
    
    # Import models and create database tables
    with app.app_context():
        from app import models  # Import models so tables are registered
        db.create_all()         # Create all tables in database
        print("Database tables created successfully!")
    
    return app