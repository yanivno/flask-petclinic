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

# WSGI middleware for Flask
wsgi_middleware = func.WsgiMiddleware(flask_app.wsgi_app)

# Create the Azure Functions app
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.function_name("FlaskApp")
@app.route(route="{*route}", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Main route handler for the Flask app."""
    return wsgi_middleware.handle(req, context)
