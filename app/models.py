"""
Database models for Task Management API.
Defines User and Task entities with their relationships.
"""

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    User model for authentication.
    
    Attributes:
        id: Unique identifier
        username: Display name (unique)
        email: Email address (unique)
        password_hash: Hashed password
        created_at: Account creation timestamp
        tasks: Relationship to user's tasks
    """
    __tablename__ = 'users'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: User has many Tasks
    tasks = db.relationship('Task', backref='owner', lazy=True)
    
    def set_password(self, password):
        """Hash and store the password securely."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert User object to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<User {self.username}>'


class Task(db.Model):
    """
    Task model for to-do items.
    
    Attributes:
        id: Unique identifier
        title: Task title (required)
        description: Detailed description
        status: Current status (pending/in_progress/completed)
        priority: Priority level (low/medium/high)
        due_date: Optional deadline
        created_at: Creation timestamp
        updated_at: Last modification timestamp
        user_id: Owner's user ID (foreign key)
    """
    __tablename__ = 'tasks'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(20), default='medium')
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Key: Links to User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        """Convert Task object to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id
        }
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<Task {self.title}>'