from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)  # allow cross-origin requests; configure origins in production
    JWTManager(app)
    
    # Register blueprints
    from routes import main_bp
    app.register_blueprint(main_bp)
    
    with app.app_context():
        db.create_all()  # Create database tables for our models

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
