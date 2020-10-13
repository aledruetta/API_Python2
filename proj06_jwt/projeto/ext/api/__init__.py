from flask_restful import Api

from .views import ApiRest, ApiRestId, bp

api = Api()
api.add_resource(ApiRest, "/api/v1.1")
api.add_resource(ApiRestId, "/api/v1.1/<int:id>")


def init_app(app):
    api.init_app(app)
    app.register_blueprint(bp)
