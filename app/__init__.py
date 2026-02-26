from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Register web routes
    from app.routes import main, owners, vets
    app.register_blueprint(main.bp)
    app.register_blueprint(owners.bp)
    app.register_blueprint(vets.bp)

    # Register REST API routes
    from app.api import api_bp
    app.register_blueprint(api_bp)

    with app.app_context():
        # Check if we need to initialize the database
        # This is especially important on Azure where /tmp is ephemeral
        db_needs_init = False
        
        if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
            # Extract database path from URI
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if 'sqlite:///' in db_uri:
                db_path = db_uri.replace('sqlite:///', '')
                db_needs_init = not os.path.exists(db_path)
        
        db.create_all()
        
        # Initialize with sample data if database is new
        if db_needs_init and os.environ.get('WEBSITE_INSTANCE_ID'):
            try:
                from app.models import Owner, Pet, PetType, Visit, Vet, Specialty
                from datetime import date
                
                # Only initialize if tables are empty
                if PetType.query.first() is None:
                    # Create pet types
                    pet_types = [
                        PetType(name='cat'), PetType(name='dog'),
                        PetType(name='lizard'), PetType(name='snake'),
                        PetType(name='bird'), PetType(name='hamster'),
                    ]
                    for pt in pet_types:
                        db.session.add(pt)
                    
                    # Create specialties
                    specialties = [
                        Specialty(name='radiology'),
                        Specialty(name='surgery'),
                        Specialty(name='dentistry'),
                    ]
                    for s in specialties:
                        db.session.add(s)
                    
                    db.session.commit()
                    app.logger.info("Database initialized with sample data on Azure")
            except Exception as e:
                app.logger.error(f"Error initializing database: {e}")

    return app
