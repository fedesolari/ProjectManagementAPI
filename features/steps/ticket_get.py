#export PYTHONPATH="/home/tomi/Escritorio/aninfo/Memo-TPFinal/project:$PYTHONPATH"
from project.dao.ticket_dao import *
from project.service import ticket_service
from project.service.ticket_service import *
from project.model.model import *
from behave import *

from http import HTTPStatus
from project.service.ticket_service import *

from project import app

args = []

result = ""
ticket_id = None

@given("a ticket with title {title}, a description {description}, a priority {priority}, a severity {severity}, a product_version_id {product_version_id}, a client_id {client_id}")
def ticket_with_arguments(context, title, description, priority, severity, product_version_id, client_id):
    global ticket_id
    with app.app_context():
        ticket_id = ticket_service.create_ticket(title,description,int(severity),int(priority),int(product_version_id),None,int(client_id))[1].get("id")

@given("I dont have any tickets with an id of {_ticket_id}")
def no_ticket(context,_ticket_id):
    global ticket_id
    ticket_id = int(_ticket_id)
    with app.app_context():
        res = ticket_service.get_ticket_by_id(ticket_id)
        assert(res[0] == TICKET_NOT_FOUND)

@when("Trying to get a Ticket with that id")
def get_ticket(context):
    global result
    global ticket_id
    with app.app_context():
        result = ticket_service.get_ticket_by_id(int(ticket_id))

@then("I dont get any ticket")
def check_ticket_creates(context):
    global result
    assert(result[0] == TICKET_NOT_FOUND)

@then("I get a valid ticket")
def check_ticket_creates(context):
    global result
    assert(result[0] == OK)

@then("We get that the title is {title}, the description is {description}, the priority {priority}, the severity {severity}, the product_version_id {product_version_id}, and the client_id {client_id}")
def check_data_ticket_is_valid(context, title, description, priority, severity, product_version_id, client_id):
    global result
    ticket = result[1]
    assert(title == ticket.get('title'))
    assert(description == ticket.get('description'))
    assert(int(priority) == ticket.get('priority'))
    assert(int(severity) == ticket.get('severity'))
    assert(int(product_version_id) == ticket.get('product_version_id'))
    assert(int(client_id) == ticket.get('client_id'))
