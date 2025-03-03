from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Species, UserProgress
from forms import SpeciesForm

species = Blueprint('species', __name__)

@species.route('/species')
def list():
    species = Species.query.all()

    # Track progress for students
    if current_user.is_authenticated and current_user.role == 'student':
        for s in species:
            # Check if progress already exists
            progress = UserProgress.query.filter_by(
                user_id=current_user.id,
                content_type='species',
                content_id=s.id
            ).first()

            if not progress:
                progress = UserProgress(
                    user_id=current_user.id,
                    content_type='species',
                    content_id=s.id,
                    completed=True
                )
                db.session.add(progress)
        db.session.commit()

    return render_template('species/list.html', species=species)

@species.route('/species/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.role != 'teacher':
        flash('Access denied', 'danger')
        return redirect(url_for('species.list'))

    form = SpeciesForm()
    if form.validate_on_submit():
        species = Species(
            name=form.name.data,
            scientific_name=form.scientific_name.data,
            description=form.description.data,
            population=form.population.data,
            conservation_status=form.conservation_status.data,
            habitat=form.habitat.data,
            threats=form.threats.data
        )
        db.session.add(species)
        db.session.commit()
        flash('Species added successfully!', 'success')
        return redirect(url_for('species.list'))
    return render_template('species/add.html', form=form)