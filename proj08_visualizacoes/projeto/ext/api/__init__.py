from flask_restful import Api

from .views import (ApiEstacao, ApiEstacaoId, ApiEstacaoIdSensor,
                    ApiEstacaoIdSensorId, ApiSensorIdParam,
                    ApiSensorIdParamLast)

api = Api()
api.add_resource(ApiEstacao, "/api/v1.1/estacao")
api.add_resource(ApiEstacaoId, "/api/v1.1/estacao/<int:estacao_id>")
api.add_resource(ApiEstacaoIdSensor,
                 "/api/v1.1/estacao/<int:estacao_id>/sensor")
api.add_resource(ApiEstacaoIdSensorId,
                 "/api/v1.1/estacao/<int:estacao_id>/sensor/<int:sensor_id>")
api.add_resource(ApiSensorIdParam,
                 "/api/v1.1/sensor/<int:sensor_id>/<string:param>")
api.add_resource(ApiSensorIdParamLast,
                 "/api/v1.1/sensor/<int:sensor_id>/<string:param>/last")


def init_app(app):
    api.init_app(app)
