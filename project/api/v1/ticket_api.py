from flask import jsonify
from flask_apispec.views import MethodResource
from flask_restful import Resource
import requests
from project.utils.utils import log_endpoint, generate_response, get_general_response_schema
from http import HTTPStatus
from project.responses.response_constants import CLIENT_NOT_FOUND
from project.service import ticket_service, product_service
from webargs import fields
from flask_apispec import use_kwargs, marshal_with
from project.responses.ticket_schemas import TicketSchemas

EXTERNAL_CLIENT_ENDPOINT = 'https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/clientes-psa/1.0.0/m/api/clientes'


class Ticket(Resource, MethodResource):
    @log_endpoint
    @use_kwargs({'ticket_id': fields.Integer(required=True)}, location=('query'))
    def get(self, ticket_id):

        code, response, http_code = ticket_service.get_ticket_by_id(ticket_id)
        return generate_response(code, response, http_code)

    @log_endpoint
    @marshal_with(get_general_response_schema(TicketSchemas))
    @use_kwargs({'title': fields.Str(required=True),
                'description': fields.Str(required=True),
                 'priority': fields.Integer(required=True),
                 'severity': fields.Integer(required=True),
                 'product_version_id': fields.Integer(required=True),
                 'resource_name': fields.Str(required=False),
                 'client_id': fields.Integer(required=True)
                 }, location=('json'))
    def post(self, title, description, priority, severity, product_version_id,
             resource_name, client_id):

        code, response, http_code = ticket_service.create_ticket(title, description, severity, priority,
                                                                 product_version_id, resource_name, client_id)

        return generate_response(code, response, http_code)

    @log_endpoint
    @use_kwargs({'ticket_id': fields.Integer(required=True)}, location=('query'))
    def delete(self, ticket_id):
        code, response, http_code = ticket_service.delete_ticket_by_id(
            ticket_id)
        return generate_response(code, response, http_code)

    @log_endpoint
    @use_kwargs({'ticket_id': fields.Integer(required=True),
                'title': fields.Str(),
                 'description': fields.Str(),
                 'priority': fields.Integer(),
                 'severity': fields.Integer(),
                 'product_version_id': fields.Integer(),
                 'resource_name': fields.String(),
                 'client_id': fields.Integer(),
                 'state': fields.Integer(),
                 }, location=('json'))
    def put(self, ticket_id, title=None, description=None, priority=None, severity=None,
            product_version_id=None, resource_name=None, client_id=None, state=None):

        code, response, http_code = ticket_service.update_ticket_by_id(ticket_id, title, description,
                                                                       priority, severity, product_version_id, resource_name, client_id, state)
        return generate_response(code, response, http_code)


class Tickets(Resource, MethodResource):
    @log_endpoint
    @use_kwargs({
                'ticket_ids': fields.List(fields.Integer()),
                'prioritys': fields.List(fields.Integer()),
                'severitys': fields.List(fields.Integer()),
                'product_version_ids': fields.List(fields.Integer()),
                'resource_names': fields.List(fields.String()),
                'client_ids': fields.List(fields.Integer()),
                'states': fields.List(fields.Integer()),
                'expiration': fields.Boolean()
                }, location=('json'))
    def post(self, ticket_ids=[], prioritys=[], severitys=[], product_version_ids=[],
             resource_names=[], client_ids=[], states=[], expiration=False):

        code, response, http_code = ticket_service.get_tickets_by(ticket_ids, prioritys, severitys,
                                                                  product_version_ids, resource_names, client_ids, states, expiration)

        return generate_response(code, response, http_code)


class Products(Resource, MethodResource):
    @log_endpoint
    def get(self):
        code, response, http_code = product_service.get_products()
        return generate_response(code, response, http_code)

class ProductsVersion(Resource, MethodResource):
    @log_endpoint
    def get(self):
        code, response, http_code = product_service.get_products_version()
        return generate_response(code, response, http_code)
    
class Clients(Resource, MethodResource):
    @log_endpoint
    def get(self):
        data = requests.get(EXTERNAL_CLIENT_ENDPOINT)
        return jsonify(data.json())


class Client(Resource, MethodResource):
    @log_endpoint
    @use_kwargs({'client_id': fields.Integer(required=True)}, location=('query'))
    def get(self, client_id):
        clients = requests.get(EXTERNAL_CLIENT_ENDPOINT).json()
        for client in clients:
            if client['id'] == client_id:
                return client

        return generate_response(CLIENT_NOT_FOUND, [], HTTPStatus.NOT_FOUND)
    
class Task(Resource, MethodResource):
    @log_endpoint
    @use_kwargs({'ticket_id': fields.Integer(required=True),
                 'task_id': fields.Integer(required=True)}, 
                location=('json'))
    def post(self, ticket_id, task_id):
        code, response, http_code = ticket_service.add_task_to_ticket(ticket_id, task_id)
        return generate_response(code, response, http_code)
    
class Tasks(Resource, MethodResource):
    @log_endpoint
    @use_kwargs({'ticket_id': fields.Integer(required=True)}, 
                location=('query'))
    def get(self, ticket_id):
        code, response, http_code = ticket_service.get_ticket_tasks(ticket_id)
        return generate_response(code, response, http_code)