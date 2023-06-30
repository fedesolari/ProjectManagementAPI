#export PYTHONPATH="/home/tomi/Escritorio/aninfo/Memo-TPFinal/project:$PYTHONPATH"
from project.dao.ticket_dao import *
from project.service import ticket_service
from project.service.ticket_service import *
from project.model.model import *
from behave import *

from http import HTTPStatus
from project.service.ticket_service import *

from project import app

result = None

ticket_id1 = None
ticket_id2 = None

@given("two valid tickets with different priority and equal severity")
def create_ticket_with_no_arguments(context):
    with app.app_context():
        global ticket_id1
        global ticket_id2
        r = ticket_service.create_ticket("title1","description1",1,1,1,None,1)
        r2 = ticket_service.create_ticket("title2","description2",1,4,1,None,1)
        ticket_id1 = r[1].get('id')
        ticket_id2 = r2[1].get('id')
        assert(r[0] == OK and r2[0] == OK)

@when("trying to filter the tickets by expiracy")
def delete_ticket_with_valid_id(context,):
    with app.app_context():
        global result
        result = ticket_service.get_tickets_by(None,None,None,None,None,None,None,True)

@when("trying to filter the tickets by priority {priority}")
def delete_ticket_with_valid_id(context,priority):
    global ticket_id1
    global ticket_id2
    with app.app_context():
        global result
        result = ticket_service.get_tickets_by([ticket_id1,ticket_id2],[priority],None,None,None,None,None,False)
        print(result[1])

@when("trying to filter the tickets by severity {severity}")
def delete_ticket_with_valid_id(context,severity):
    global ticket_id1
    global ticket_id2
    with app.app_context():
        global result
        result = ticket_service.get_tickets_by([ticket_id1,ticket_id2],None,[severity],None,None,None,None,False)
        print(result[1])


@then("we get an emptly tickets list")
def check_ticket_not_created(context):
    global result
    assert(result[0] == OK and result[1] == [])

@then("we get only the first ticket")
def check_ticket_not_created(context):
    global result
    assert(result[0] == OK and result[1][0].get("id") == ticket_id1)

@then("we get both tickets")
def check_ticket_not_created(context):
    global result
    global ticket_id1
    global ticket_id2
    assert(result[0] == OK and result[1][0].get("id") == ticket_id1 and result[1][1].get("id") == ticket_id2)