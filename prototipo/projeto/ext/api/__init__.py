from flask_restful import Api
from projeto.ext.api.views import (ApiEstacao, ApiEstacaoId,
                                   ApiEstacaoIdSensor, ApiSensorId,
                                   ApiSensorIdParam, ApiSensorIdParamLast)

api = Api()
versao = "v1.2"

api.add_resource(ApiEstacao, f"/api/{versao}/estacao")
api.add_resource(ApiEstacaoId, f"/api/{versao}/estacao/<int:estacao_id>")
api.add_resource(ApiEstacaoIdSensor,
                 f"/api/{versao}/estacao/<int:estacao_id>/sensor")
api.add_resource(ApiSensorId, f"/api/{versao}/sensor/<int:sensor_id>")
api.add_resource(ApiSensorIdParam,
                 f"/api/{versao}/sensor/<int:sensor_id>/<string:param>")
api.add_resource(
    ApiSensorIdParamLast,
    f"/api/{versao}/sensor/<int:sensor_id>/<string:param>/<int:qty>")


def init_app(app):
    api.init_app(app)
