"""
Azure Functions entry point for Flask PetClinic application.
Uses the WSGI middleware to run Flask as an Azure Function.
"""

import azure.functions as func
from app import create_app, db

# Create the Flask application
flask_app = create_app()

# Initialize database within app context
with flask_app.app_context():
    db.create_all()

# Create the Azure Functions WSGI app
app = func.WsgiFunctionApp(app=flask_app.wsgi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
