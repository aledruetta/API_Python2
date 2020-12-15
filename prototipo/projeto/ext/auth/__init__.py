from flask_login import LoginManager
from projeto.ext.auth.models import UserAuth
from projeto.ext.auth.views import bp

login_manager = LoginManager()


def init_app(app):
    app.register_blueprint(bp)
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserAuth.query.get(int(user_id))
