from flask_restful import Api

from .views import ApiEstacao, ApiEstacaoId, ApiSensor, ApiSensorId

api = Api()
api.add_resource(ApiEstacao, "/api/v1.1/estacao")
api.add_resource(ApiEstacaoId, "/api/v1.1/estacao/<int:id>")
api.add_resource(ApiSensor, "/api/v1.1/sensor")
api.add_resource(ApiSensorId, "/api/v1.1/sensor/<int:id>")


def init_app(app):
    api.init_app(app)
