from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # 'species', 'resource', 'quiz', etc.
    content_id = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False)  # teacher, student, community
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    resources = db.relationship('EducationalResource', backref='author', lazy=True)
    programs = db.relationship('ConservationProgram', backref='coordinator', lazy=True)
    progress = db.relationship('UserProgress', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_progress_percentage(self):
        if self.role != 'student':
            return 100

        total_items = (
            Species.query.count() +
            EducationalResource.query.count() +
            ConservationProgram.query.count()
        )

        if total_items == 0:
            return 0

        completed_items = UserProgress.query.filter_by(
            user_id=self.id,
            completed=True
        ).count()

        return int((completed_items / total_items) * 100)

class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    population = db.Column(db.Integer)
    conservation_status = db.Column(db.String(50))
    habitat = db.Column(db.String(100))
    threats = db.Column(db.Text)

class EducationalResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ConservationProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    coordinator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)