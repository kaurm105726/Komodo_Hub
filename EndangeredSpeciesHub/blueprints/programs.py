from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import ConservationProgram
from forms import ProgramForm

programs = Blueprint('programs', __name__)

@programs.route('/programs')
def list():
    programs = ConservationProgram.query.order_by(ConservationProgram.start_date.desc()).all()
    form = ProgramForm()  # Create form instance for the modal
    return render_template('programs/index.html', programs=programs, form=form)

@programs.route('/programs/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.role not in ['teacher', 'community']:
        flash('Access denied', 'danger')
        return redirect(url_for('programs.list'))

    form = ProgramForm()
    if form.validate_on_submit():
        program = ConservationProgram(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            coordinator_id=current_user.id
        )
        db.session.add(program)
        db.session.commit()
        flash('Program added successfully!', 'success')
        return redirect(url_for('programs.list'))
    return render_template('programs/add.html', form=form)