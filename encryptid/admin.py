from flask import Blueprint, render_template, request, jsonify, abort
from .models import User, Log, db, Level
from flask_login import login_required, current_user
from datetime import datetime
from .utils import paginate, is_valid_host

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/', strict_slashes=False)
@login_required
def index():
    if not is_valid_host(request):
        return abort(403)

    user = User.query.filter_by(id=current_user.id).first()
    if not user.admin:
        return 'You need to be an administrator to access this functionality.', 403

    return render_template('admin/index.html')

@bp.route('/logs', strict_slashes=False)
@login_required
def logs():
    if not is_valid_host(request):
        return abort(403)

    user = User.query.filter_by(id=current_user.id).first()
    if not user.admin:
        return 'You need to be an administrator to access this functionality.', 403

    logs = Log.query.order_by(Log.time.desc()).limit(100).all()
    return render_template('admin/logs.html', logs=logs)

@bp.route('/users', strict_slashes=False)
@login_required
def users():
    if not is_valid_host(request):
        return abort(403)

    user = User.query.filter_by(id=current_user.id).first()
    if not user.admin:
        return 'You need to be an administrator to access this functionality.', 403

    users = User.query.all()
    return render_template('admin/users.html', users=paginate(users))

@bp.route('/user', strict_slashes=False)
@login_required
def user():
    if not is_valid_host(request):
        return abort(403)

    user = User.query.filter_by(id=current_user.id).first()
    if not user.admin:
        return 'You need to be an administrator to access this functionality.', 403

    player_id = request.args.get('player')
    player = User.query.filter_by(id=player_id).first()
    player_logs = Log.query.filter_by(user_email=player_id).order_by(Log.time.desc()).limit(50).all()

    return render_template('admin/user.html', player=player, logs=player_logs)

@bp.route('/ban', strict_slashes=False)
@login_required
def ban():
    if not is_valid_host(request):
        return abort(403)

    user = User.query.filter_by(id=current_user.id).first()
    if not user.admin:
        return 'You need to be an administrator to access this functionality.', 403

    player_id = request.args.get('player')
    player = User.query.filter_by(id=player_id).first()

    if player.banned:
        player.banned = False
        db.session.commit()
        return jsonify({ 'banned': False, 'message': f'Unbanned {player.name} successfully.' })

    player.banned = True
    db.session.commit()

    return jsonify({ 'banned': True, 'message': f'Banned {player.name} successfully.' })

@bp.route('/levels', strict_slashes=False)
@login_required
def levels():
    if not is_valid_host(request):
        return abort(403)

    user = User.query.filter_by(id=current_user.id).first()
    if not user.admin:
        return 'You need to be an administrator to access this functionality.', 403

    levels = Level.query.all()
    return render_template('admin/levels.html', levels=paginate(levels))

@bp.route('/levels/add', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def add_level():
    if not is_valid_host(request):
        return abort(403)

    if request.method == 'POST':
        level_id = request.form['number']
        question = request.form['question']
        answer = request.form['answer']
        points = request.form['points']
        hint = request.form['hint']

        level = Level(id=level_id, question=question, answer=answer, points=points, hint=hint)
        db.session.add(level)
        db.session.commit()

    return render_template('admin/add_level.html')