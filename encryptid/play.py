from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import db, Level, User, Log
import time

bp = Blueprint('play', __name__)

@bp.route('/play', strict_slashes=False)
@login_required
def play():
    if current_user.banned:
        return render_template('banned.html', **{'name': current_user.name})
    level_id = current_user.current_level + 1
    level = Level.query.filter_by(id=level_id).first()
    if current_user.current_level != 0 and level is None:
        return render_template('fin.html', **{'name': current_user.name})
    level_question = level.question
    level_points = level.points
    level_hint = level.hint

    user = User.query.filter_by(id=current_user.id).first()

    context = {
        'question': level_question,
        'points': level_points,
        'hint': level_hint,
        'level': str(level.id),
        'name': current_user.name,
        'user_id': current_user.id,
        'completed_levels': user.current_level,
        'user_points': user.points
    }

    return render_template('play.html', **context)

@bp.route('/submit', methods=['POST'], strict_slashes=False)
@login_required
def submit():
    if request.method != 'POST':
        return "Only POST requests are allowed."

    r = eval(request.data)
    level_id = current_user.current_level + 1
    answer = ''.join(r['answer'].split()).lower()
    ip = request.remote_addr

    log = Log(text=answer, level=level_id, username=current_user.name, user_email=current_user.id, time=time.time(), ip=ip)
    db.session.add(log)
    db.session.commit()

    level = Level.query.filter_by(id=level_id).first()

    if level.answer == answer:
        user = User.query.filter_by(id=current_user.id).first()
        user.current_level = level.id
        user.points += level.points
        user.last_answer = time.time()
        db.session.commit()

        return jsonify({ 'success': True, 'message': 'Correct answer. Good work there!' })

    return jsonify({ 'success': False, 'message': 'Incorrect answer. Please try again.' })

# Level-related
@bp.route('/play/1', strict_slashes=False)
@bp.route('/play/level1', strict_slashes=False)
@login_required
def level():
    return render_template('lvl1.html', name=current_user.name)