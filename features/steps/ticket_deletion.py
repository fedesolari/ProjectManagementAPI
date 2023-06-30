from project.dao.ticket_dao import *
from project.service import ticket_service
from project.service.ticket_service import *
from project.model.model import *
from behave import *

from http import HTTPStatus
from project.service.ticket_service import *

from project import app


@given("Im a resource that wants to delete a ticket")
def resource(context):
    pass


@when("I delete a ticket")
def delete_ticket(context):
    with app.app_context():
        _, ticket, _= ticket_service.create_ticket("Reports contain missing data", "Price column is missing from the downloaded report", 1, 1, 1, "John Doe", 5)
        code, _, _ = ticket_service.delete_ticket_by_id(ticket["id"])
        assert code == OK
        
@when("I delete a ticket by an invalid id")
def delete_ticket_with_invalid_id(context):
    with app.app_context():
        _, ticket, _= ticket_service.create_ticket("Reports contain missing data", "Price column is missing from the downloaded report", 1, 1, 1, "John Doe", 5)
        code, _, _ = ticket_service.delete_ticket_by_id(-1)
        assert code != OK


@then("The ticket is deleted and I no longer have access to it")
def ticket_not_found(context):
    with app.app_context():
        code, _, _ = ticket_service.get_ticket_by_id(1)
        assert TICKET_NOT_FOUND == code
        
@then("The deletion fails")
def ticket_not_found(context):
    with app.app_context():
        code, _, _ = ticket_service.get_ticket_by_id(1)
        assert TICKET_NOT_FOUND == code
