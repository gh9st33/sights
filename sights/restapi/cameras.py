from flask import request, jsonify, Response
from flask_restx import Namespace, Resource, fields
from sights.api import v1 as api

restapi = Namespace('cameras', description='Camera stream related operations')


@restapi.route('/')
class Cameras(Resource):
    def get(self):
        return api.cameras.list_all()


@restapi.route('/<camera_id>/stream')
class Stream(Resource):
    def get(self, camera_id: str):
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(api.cameras.stream(camera_id),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


@restapi.route('/<camera_id>/resolution')
class CameraResolution(Resource):
    @restapi.expect(restapi.model('Resolution', {
        'width': fields.Integer,
        'height': fields.Integer,
    }))
    def post(self, camera_id: str):
        res = request.get_json()
        api.cameras.set_resolution(camera_id, res["width"], res["height"])
        return '', 200

    def get(self, camera_id: str):
        res = api.cameras.get_resolution(camera_id)
        return {
            "width": res[0],
            "height": res[1]
        }


@restapi.route('/<camera_id>/framerate')
class CameraFramerate(Resource):
    def post(self, camera_id: str):
        api.cameras.set_framerate(camera_id, request.get_data())
        return '', 200

    def get(self, camera_id: str) -> int:
        return api.cameras.get_framerate(camera_id)
