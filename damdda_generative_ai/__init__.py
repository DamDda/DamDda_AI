from flask import Flask

def create_app():
    app = Flask(__name__)  # Initialize the Flask application

    from .routes import main_bp  # Import the blueprint containing the routes
    app.register_blueprint(main_bp)  # Register the routes with the Flask app

    return app  # Return the Flask app instance
