from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models import Species, EducationalResource

games = Blueprint('games', __name__)

@games.route('/quiz/species')
@login_required
def species_quiz():
    species = Species.query.all()
    return render_template('games/species_quiz.html', species=species)

@games.route('/quiz/conservation')
@login_required
def conservation_quiz():
    resources = EducationalResource.query.all()
    return render_template('games/conservation_quiz.html', resources=resources)

@games.route('/games/habitat-explorer')
@login_required
def habitat_explorer():
    species = Species.query.all()
    return render_template('games/habitat_explorer.html', species=species)

@games.route('/api/quiz/get-question')
@login_required
def get_quiz_question():
    # Example quiz question
    return jsonify({
        "question": "Which of these species is critically endangered?",
        "options": [
            "Sumatran Tiger",
            "Komodo Dragon",
            "Javan Rhinoceros",
            "Proboscis Monkey"
        ],
        "correct": 2,  # Index of correct answer
        "explanation": "The Javan Rhinoceros is one of the rarest large mammals on Earth, with only about 74 individuals remaining in the wild."
    })
