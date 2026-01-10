"""
Configuration settings for Task Management API.
"""

import os


class Config:
    """
    Application configuration class.
    
    Attributes:
        SECRET_KEY: Key for session encryption
        SQLALCHEMY_DATABASE_URI: Database connection string
        SQLALCHEMY_TRACK_MODIFICATIONS: Disable modification tracking
    """
    # Secret key for session security
    # In production, set this via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database location (SQLite file in instance folder)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tasks.db'
    
    # Disable modification tracking (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False