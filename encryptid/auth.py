from flask import Blueprint, request, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required
import requests, os
from dotenv import load_dotenv
from .models import db, User
from .utils import is_valid_host

load_dotenv()

bp = Blueprint('auth', __name__)

@bp.route('/callback', strict_slashes=False)
def callback():
    if not is_valid_host(request):
        return abort(403)

    code = request.args.get('code')
    token_endpoint = 'https://login.microsoftonline.com/organizations/oauth2/v2.0/token'
    body = {
        'client_id': os.environ.get('AZURE_CLIENT_ID'),
        'scope': 'openid profile email',
        'grant_type': 'authorization_code',
        'redirect_uri': os.environ.get('BASE_URL') + '/callback',
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'code': code
    }

    response = requests.post(token_endpoint, data=body)
    access_token = response.json()['access_token']

    headers = { 'Authorization': f'Bearer {access_token}' }
    user_profile = requests.get('https://graph.microsoft.com/oidc/userinfo', headers=headers)

    user = User.query.filter_by(id=user_profile.json()['email']).first()
    if not user:
        user = User(id=user_profile.json()['email'], name=user_profile.json()['name'], non_competitive=False)
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for('play.play'))

@bp.route('/discord', strict_slashes=False)
def discord_callback():
    if not is_valid_host(request):
        return abort(403)

    code = request.args.get('code')
    token_endpoint = 'https://discord.com/api/v8/oauth2/token'
    body = {
        'client_id': os.environ.get('DISCORD_CLIENT_ID'),
        'client_secret': os.environ.get('DISCORD_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'redirect_uri': os.environ.get('BASE_URL') + '/discord',
        'code': code
    }

    response = requests.post(token_endpoint, data=body)
    access_token = response.json()['access_token']

    headers = { 'Authorization': f'Bearer {access_token}' }
    user_profile = requests.get('https://discord.com/api/v8/users/@me', headers=headers)

    user = User.query.filter_by(id=user_profile.json()['email']).first()
    if not user:
        name = f"{user_profile.json()['username']}#{user_profile.json()['discriminator']}"
        user = User(id=user_profile.json()['email'], name=name, non_competitive=True)
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for('play.play'))

@bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    if not is_valid_host(request):
        return abort(403)

    logout_user()
    return redirect(url_for('index'))