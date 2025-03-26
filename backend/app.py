from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow CORS for all routes, specifying the origin for security.
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        from routes import main_bp
        app.register_blueprint(main_bp)
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
