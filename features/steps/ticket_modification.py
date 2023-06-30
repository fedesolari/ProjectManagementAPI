from project.dao.ticket_dao import *
from project.responses.response_constants import INVALID_PRODUCT_VERSION_ID
from project.service import ticket_service
from project.service.ticket_service import *
from project.model.model import *
from behave import *

from http import HTTPStatus
from project.service.ticket_service import *

from project import app

from project.service.ticket_service import calculate_sla

args = []

result = ""

ticket_id = None

@given("A Ticket")
def create_ticket_with_no_arguments(context):
    with app.app_context():
        global ticket_id
        response, ticket, _ = ticket_service.create_ticket("title1","description1",1,1,1,None,1)
        ticket_id = ticket.get('id')
        assert response == OK

@given("A ticket with a state of OPEN")
def create_ticket_open(context):
    with app.app_context():
        global ticket_id
        r = ticket_service.create_ticket("title1","description1",1,1,1,None,1)
        ticket_id = r[1].get('id')
        assert(r[0] == OK)
        r = ticket_service.update_ticket_by_id(ticket_id,None,None,None,None,None,"resource1",None,TicketState.OPEN.value)
        assert(OK == r[0])

@when("I change its title to {title}")
def modify_ticket_title(context,title):
    with app.app_context():
        global ticket_id

        result = ticket_service.update_ticket_by_id(ticket_id,title)

        assert(result[0] == OK)

@when("I change its description to {description}")
def modify_ticket_description(context,description):
    with app.app_context():
        global ticket_id

        result = ticket_service.update_ticket_by_id(ticket_id,None,description)

        assert(result[0] == OK)

@when("I change its priority to {priority}")
def modify_ticket_priority(context,priority):
    with app.app_context():
        global ticket_id
        global result
        result = ticket_service.update_ticket_by_id(ticket_id,None,None,int(priority))

@when("I change its severity to {severity}")
def modify_ticket_severity(context,severity):
    with app.app_context():
        global ticket_id
        global result
        result = ticket_service.update_ticket_by_id(ticket_id,None,None,None,int(severity))

@when("I change its client_id to {client_id}")
def modify_ticket_client_id(context,client_id):
    with app.app_context():
        global ticket_id
        global result
        result = ticket_service.update_ticket_by_id(ticket_id,None,None,None,None,None,None,int(client_id))

@when("I change its product_version_id to {product_version_id} being that this product_version_id is valid")
def modify_ticket_product_version_id(context,product_version_id):
    with app.app_context():
        global ticket_id
        global result
        result = ticket_service.update_ticket_by_id(ticket_id,None,None,None,None,int(product_version_id))

@when("I change its product_version_id to {product_version_id} being that this product_version_id is invalid")
def modify_ticket_product_version_id(context,product_version_id):
    with app.app_context():
        global ticket_id
        global result
        try:
            result = ticket_service.update_ticket_by_id(ticket_id,None,None,None,None,int(product_version_id))[0]
        except:
            result = INVALID_PRODUCT_VERSION_ID

@when("I change its state to IN_PROGRESS with a resource_name of {resource_name}")
def modify_ticket_state_and_resource_name(context,resource_name):
    with app.app_context():
        global ticket_id
        global result
        result = ticket_service.update_ticket_by_id(ticket_id,None,None,None,None,None,resource_name,None,TicketState.IN_PROGRESS.value)

@when("I change its state to OPEN")
def modify_ticket_state_open(context):
    with app.app_context():
        global ticket_id
        global result
        result = ticket_service.update_ticket_by_id(ticket_id,None,None,None,None,None,None,None,TicketState.OPEN.value)

@when("I change its state to IN_PROGRESS without a resource_name")
def modify_ticket_state_and_resource_name(context):
    with app.app_context():
        global ticket_id
        global result
        result = ticket_service.update_ticket_by_id(ticket_id,None,None,None,None,None,None,None,TicketState.IN_PROGRESS.value)

@when("I change its state to NEW")
def modify_ticket_state_to_new(context):
    with app.app_context():
        global ticket_id
        global result
        result = ticket_service.update_ticket_by_id(ticket_id,None,None,None,None,None,None,None,TicketState.NEW.value)


@when("I change its product_version_id to {product_version_id} being that there is a product_version_id of 2")
def modify_ticket_product_version_id(context,product_version_id):
    with app.app_context():
        global ticket_id
        global result
        result = ticket_service.update_ticket_by_id(ticket_id,None,None,None,None,int(product_version_id))

@then("The Ticket title changes to {title}")
def check_change_title(context,title):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[0] == OK)
        assert(result[1].get('title') == title)

@then("The Ticket state changes to OPEN")
def check_change_state(context):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[0] == OK)
        assert(result[1].get('state') == TicketState.OPEN.value)


@then("The Ticket description changes to {description}")
def check_change_description(context,description):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[0] == OK)
        assert(result[1].get('description') == description)

@then("The Ticket priority changes to {priority}")
def check_change_priority(context,priority):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[0] == OK)
        assert(result[1].get('priority') == int(priority))

@then("The Ticket severity changes to {severity}")
def check_change_severity(context,severity):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[0] == OK)
        assert(result[1].get('severity') == int(severity))

@then("The Ticket client_id changes to {client_id}")
def check_change_client_id(context,client_id):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[0] == OK)
        assert(result[1].get('client_id') == int(client_id))

@then("The Ticket state changes to IN_PROGRESS")
def check_valid_change_state(context):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[0] == OK)
        assert(result[1].get('state') == TicketState.IN_PROGRESS.value)

@then("The Ticket product_version_id changes to {product_version_id}")
def check_change_product_version_id(context,product_version_id):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[0] == OK)
        assert(result[1].get('product_version_id') == int(product_version_id))

@then("The resource_name changes to {resource_name}")
def check_change_resource_name(context,resource_name):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[0] == OK)
        assert(result[1].get('resource_name') == resource_name)

@then("The state update fails because cant change state to NEW")
def check_state_update(context):
    global result
    assert(result[0] == STATE_CHANGE_TO_NEW)

@then("The state update fails because no resource")
def check_state_update(context):
    global result
    assert(result[0] == NO_RESOURCE_ASSIGNED)

@then("The priority update fails")
def check_priority_update(context):
    global result
    assert(result[0] == NOT_VALID_PRIORITY)

@then("The severity update fails")
def check_severity_update(context):
    global result
    assert(result[0] == NOT_VALID_SEVERITY)

@then("The product_version_id update fails")
def check_product_version_id_update(context):
    global result
    assert(result == INVALID_PRODUCT_VERSION_ID)

@then("Its state doesnt change")
def check_state_update(context):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[1].get('state') == TicketState.NEW.value)

@then("its state is still OPEN")
def check_state_update(context):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[1].get('state') == TicketState.OPEN.value)

@then("Its priority doesnt change")
def check_priority_update(context):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[1].get('priority') == 1)

@then("Its severity doesnt change")
def check_severity_update(context):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[1].get('severity') == 1)

@then("Its product_version_id doesnt change")
def check_product_version_id_update(context):
    with app.app_context():
        global ticket_id
        result = get_ticket_by_id(ticket_id)
        assert(result[1].get('product_version_id') == 1)
