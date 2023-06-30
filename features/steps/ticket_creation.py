from project.dao.ticket_dao import *
from project.service import ticket_service
from project.service.ticket_service import *
from project.model.model import *
from behave import *

from http import HTTPStatus
from project.service.ticket_service import *

from datetime import datetime

from project import app

ticket_id = None

@given('Im a resource')
def resource_creates_ticket(context):
    pass

@when('I create a ticket with the following data')
def ticket_creation_process(context):
    with app.app_context():
        model: Ticket = {row["property"]: row["value"] for row in context.table}
        context.error = OK
        code, message, result = ticket_service.create_ticket(
            title=model['title'],
            description=model['description'],
            severity=model['severity'],
            priority=model['priority'],
            product_version_id=model['product_version_id'],
            resource_name=model['resource_name'],
            client_id=model['client_id'],
        )
        if code != OK:
            context.error = result
        else:
            context.ticket = message
            
@when('I create a ticket with one invalid field')
def invalid_ticket_creation_process(context):
    with app.app_context():
        model: Ticket = {row["property"]: row["value"] for row in context.table}
        context.error = OK
        code, message, result = ticket_service.create_ticket(
            title=model['title'],
            description=model['description'],
            severity=model['severity'],
            priority=model['priority'],
            product_version_id=model['product_version_id'],
            resource_name=model['resource_name'],
            client_id=model['client_id'],
        )
        if code != OK:
            context.error = result
        else:
            context.ticket = message



@then('The ticket gets successfully created')
def successful_response(context):
    assert context.error ==  OK
    
@then('The ticket does not get created')
def fail_response(context):
    assert context.error !=  OK
    
@then('Contains valid ID')
def valid_id(context):
    assert context.ticket['id'] !=  None

@then('Ticket State is NEW')
def new_state(context):
    assert context.ticket['state'] ==  1
    
@then("The title is {title}, the description is {description}, the priority {priority}, the severity {severity}, the product_version_id {product_version_id}, the resource_name is {resource_name} and the client_id {client_id}")
def check_data_ticket_is_valid(context, title, description, priority, severity, product_version_id, resource_name, client_id):
    with app.app_context():
        print(context.ticket)
        assert (title == context.ticket.get('title'))
        assert (description == context.ticket.get('description'))
        assert (resource_name == context.ticket.get('resource_name'))
        assert (int(priority) == context.ticket.get('priority'))
        assert (int(severity) == context.ticket.get('severity'))
        assert (int(product_version_id) == context.ticket.get('product_version_id'))
        assert (int(client_id) == context.ticket.get('client_id'))

@when('When I create a ticket with a severity of {1}')
def ticket_with_given_severity(context, severity):
    with app.app_context():
        global ticket_id
        code, ticket, result = ticket_service.create_ticket('Reports contain missing data', 'Price column is missing from the downloaded report', int(severity), 1, 1, 'John Doe', 5)
        ticket_id = ticket['id']
        assert code == OK
        
@then('The SLA is 7 days from creation date')
def new_state(context):
    with app.app_context():
        _, ticket, _ = ticket_service.get_ticket_by_id(ticket_id)
        assert ticket['SLA'] >= datetime.now() + timedelta(days=7) and ticket['SLA'] <= (datetime.now() + timedelta(days=8))