import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///komodo.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["DEBUG"] = True  # Enable debug mode

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprints
from blueprints.auth import auth
from blueprints.main import main
from blueprints.species import species
from blueprints.education import education
from blueprints.programs import programs
from blueprints.games import games

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(species)
app.register_blueprint(education)
app.register_blueprint(programs)
app.register_blueprint(games)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f'Page not found: {error}')
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    return render_template('errors/500.html'), 500

with app.app_context():
    # Import models after app creation to avoid circular imports
    import models  # noqa: F401
    try:
        db.create_all()
        app.logger.info('Database tables created successfully')

        # Initialize default data
        from scripts.init_data import init_data
        init_data()
        app.logger.info('Default data initialized successfully')
    except Exception as e:
        app.logger.error(f'Error during startup: {e}')