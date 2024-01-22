from flask.views import MethodView
from flask_smorest import Blueprint


blp = Blueprint('Message', 'messages', description='Operation on messages for a particular ticket')


@blp.route('/tickets/<string:ticket_id>/message')
class Message(MethodView):
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def get(self, ticket_id):
        pass
    
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def post(self, ticket_id):
        pass

