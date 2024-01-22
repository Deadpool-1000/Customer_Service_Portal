from flask.views import MethodView
from flask_smorest import Blueprint


blp = Blueprint('Feedback', 'feedbacks', description='Operation on feedback for a particular ticket')


@blp.route('/tickets/<string:ticket_id>/feedback')
class Feedback(MethodView):
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def post(self, ticket_id):
        pass

    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def get(self, ticket_id):
        pass

