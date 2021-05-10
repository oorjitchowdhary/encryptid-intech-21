from flask import Blueprint, render_template, request, abort
from .models import User
from .utils import is_valid_host

bp = Blueprint('leaderboard', __name__)

@bp.route('/leaderboard', strict_slashes=False)
def leaderboard():
    if not is_valid_host(request):
        print(request.host_url)
        return abort(403)

    lb = User.query.filter_by(banned=False).filter_by(non_competitive=False).filter_by(admin=False).order_by(User.points.desc()).order_by(User.last_answer.asc()).all()
    lb_nc = User.query.filter_by(banned=False).filter_by(non_competitive=True).filter_by(admin=False).order_by(User.points.desc()).order_by(User.last_answer.asc()).limit(10).all()

    return render_template('leaderboard.html', lb=list(lb), lb_nc=list(lb_nc))