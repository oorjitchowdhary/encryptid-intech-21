import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort
from .models import db, User
from .utils import is_valid_host
from flask_login import LoginManager

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') or 'sqlite:///' + os.path.join(base_dir, 'users.db')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'index'

    with app.app_context():
        db.create_all()
        db.session.commit()

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    @app.route('/')
    def index():
        if not is_valid_host(request):
            return abort(403)

        azure_client_id = os.environ.get('AZURE_CLIENT_ID')
        discord_client_id = os.environ.get('DISCORD_CLIENT_ID')
        redirect_uri = os.environ.get('BASE_URL') + '/callback'
        discord_redirect_uri = os.environ.get('BASE_URL') + '/discord'
        oauth_endpoint = f"https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize?client_id={azure_client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=openid%20offline_access%20email%20profile&state=00042"
        discord_endpoint = f"https://discord.com/api/oauth2/authorize?client_id={discord_client_id}&redirect_uri={discord_redirect_uri}&response_type=code&scope=email%20identify"

        return render_template('index.html', ms_endpoint=oauth_endpoint, discord_endpoint=discord_endpoint)

    app.add_url_rule('/', endpoint='index')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import play
    app.register_blueprint(play.bp)

    from . import leaderboard
    app.register_blueprint(leaderboard.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import utils
    app.jinja_env.filters['readable'] = utils.readable_date

    @app.errorhandler(404)
    def page_not_found(error):
        print(error)
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        print(error)
        return render_template('500.html'), 500

    return app

app = create_app()