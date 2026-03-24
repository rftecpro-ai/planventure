import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # --- App Configuration ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- CORS Configuration ---
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000')
    CORS(app, origins=cors_origins)

    # --- Initialize Extensions ---
    db.init_app(app)

    # --- Create Tables ---
    with app.app_context():
        db.create_all()

    # --- Routes ---
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Welcome to PlanVenture API',
            'status': 'running',
            'version': '1.0.0'
        })

    @app.route('/health')
    def health_check():
        try:
            db.session.execute(db.text('SELECT 1'))
            db_status = 'connected'
        except Exception as e:
            db_status = f'error: {str(e)}'

        return jsonify({
            'status': 'healthy',
            'database': db_status
        })

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
