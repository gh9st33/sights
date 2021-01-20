from flask import jsonify
from flask_restplus import Namespace, Resource
from sights.components.sensor import Sensors
from sights.api import v1 as papi

api = Namespace('plugins', description='Plugin related operations')


@api.route('/sensors/')
class Sensors(Resource):
    def get(self):
        sensor_plugins: Sensors = papi._private.sensor_plugins
        return jsonify([plugin for plugin in sensor_plugins])
