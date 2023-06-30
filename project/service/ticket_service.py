from http import HTTPStatus
from project.responses.response_constants import (NO_RESOURCE_ASSIGNED, NONE_PARAMETER, OK, STATE_CHANGE_TO_NEW, TICKET_NOT_FOUND, TICKET_NOT_CREATED,
                                                  TITLE_TOO_LONG, DESCRIPTION_TOO_LONG, NOT_VALID_PRIORITY, NOT_VALID_SEVERITY, NOT_VALID_STATE,
                                                  TASK_NOT_CREATED, TASK_ALREADY_ASSIGNED)
from project.dao.ticket_dao import TicketDao
from project.dao.product_dao import ProductDao
from project.utils.sql_connection import BaseSQLConnection
from project.model.model import ServiceLevelAgreement, Severity, TicketState, Priority, DAYS_NEXT_TO_EXPIRATION
from datetime import datetime, timedelta


def get_ticket_by_id(id):

    with BaseSQLConnection("main") as base_dao:
        ticket_dao = TicketDao(base_dao.get_session())
        ticket = ticket_dao.get_ticket_by_id(id)

        if not ticket:
            return TICKET_NOT_FOUND, {}, HTTPStatus.NOT_FOUND

        return OK, ticket.to_dict(), HTTPStatus.OK


def get_all_tickets(id):

    with BaseSQLConnection("main") as base_dao:
        ticket_dao = TicketDao(base_dao.get_session())
        tickets = ticket_dao.get_ticket_by_id(id)

        if not tickets:
            return OK, [], HTTPStatus.OK

        return OK, [t.to_dict() for t in tickets], HTTPStatus.OK


def calculate_sla(severity):

    if severity == Severity.CRITICAL.value:
        return ServiceLevelAgreement.S1.value
    elif severity == Severity.HIGH.value:
        return ServiceLevelAgreement.S2.value
    elif severity == Severity.MEDIUM.value:
        return ServiceLevelAgreement.S3.value
    return ServiceLevelAgreement.S4.value

def create_ticket(title, description, severity, priority, product_version_id,
                  resource_name, client_id):

    result = assert_ticket_data_is_valid_creation(
        title, description, priority, severity)
    if result != OK:
        return result, {}, HTTPStatus.BAD_REQUEST

    sla = calculate_sla(severity)

    with BaseSQLConnection("main") as base_dao:
        ticket_dao = TicketDao(base_dao.get_session())

        ticket = ticket_dao.create_ticket(title, description, TicketState.NEW.value, severity, priority,
                                          sla, product_version_id, resource_name, client_id)

        if not ticket:
            return TICKET_NOT_CREATED, {}, HTTPStatus.BAD_REQUEST
        ticket_dao.session.commit()

        return OK, ticket.to_dict(), HTTPStatus.OK


def delete_ticket_by_id(ticket_id):
    with BaseSQLConnection("main") as base_dao:
        ticket_dao = TicketDao(base_dao.get_session())

        ticket = ticket_dao.delete_ticket_by_id(ticket_id)
        if not ticket:
            return TICKET_NOT_FOUND, {}, HTTPStatus.NOT_FOUND

        ticket_dao.session.commit()

        return OK, {}, HTTPStatus.OK

def assert_ticket_data_is_valid_creation(title=None, description=None, priority=None, severity=None, state=None):

    res = assert_title_is_valid_creation(title)
    if res != OK:
        return res
    res = assert_description_is_valid_creation(description)
    if res != OK:
        return res
    res = assert_priority_is_valid_creation(priority)
    if res != OK:
        return res
    res = assert_severity_is_valid_creation(severity)
    if res != OK:
        return res
    res = assert_state_is_valid_creation(state)
    if res != OK:
        return res

    return OK


def assert_title_is_valid_creation(title=None):
    if title is None:
        return NONE_PARAMETER
    if title is not None and (len(title) >= 100 or len(title) < 1):
        return TITLE_TOO_LONG
    return OK


def assert_description_is_valid_creation(description=None):
    if description is None:
        return NONE_PARAMETER
    if description is not None and (len(description) >= 1000 or len(description) < 1):
        return DESCRIPTION_TOO_LONG
    return OK


def assert_priority_is_valid_creation(priority=None):
    if priority is None:
        return NONE_PARAMETER
    valid_priorities = {Priority.HIGH.value, Priority.MEDIUM.value, Priority.LOW.value}

    if int(priority) not in valid_priorities:
        return NOT_VALID_PRIORITY
    return OK


def assert_severity_is_valid_creation(severity=None):
    if severity is None:
        return NONE_PARAMETER
    valid_severities = {Severity.CRITICAL.value,
                        Severity.HIGH.value, Severity.MEDIUM.value, Severity.LOW.value}

    if int(severity) not in valid_severities:
        return NOT_VALID_SEVERITY
    return OK


def assert_state_is_valid_creation(state=None):
    valid_states = {TicketState.NEW.value, TicketState.OPEN.value,
                    TicketState.IN_PROGRESS.value, TicketState.CLOSED.value}

    if state is not None and state not in valid_states:
        return NOT_VALID_STATE
    return OK
    
def assert_needs_resource_assignment_creation(ticket, state):
    if state != TicketState.NEW.value and not ticket.resource_name:
        return NO_RESOURCE_ASSIGNED
    return OK

def assert_ticket_data_is_valid(title=None, description=None, priority=None, severity=None, state=None):

    res = assert_title_is_valid(title)
    if res != OK:
        return res
    res = assert_description_is_valid(description)
    if res != OK:
        return res
    res = assert_priority_is_valid(priority)
    if res != OK:
        return res
    res = assert_severity_is_valid(severity)
    if res != OK:
        return res
    res = assert_state_is_valid(state)
    if res != OK:
        return res

    return OK


def assert_title_is_valid(title=None):
    if title is not None and (len(title) >= 100 or len(title) < 1):
        return TITLE_TOO_LONG
    return OK


def assert_description_is_valid(description=None):
    if description is not None and (len(description) >= 1000 or len(description) < 1):
        return DESCRIPTION_TOO_LONG
    return OK


def assert_priority_is_valid(priority=None):
    valid_priorities = {Priority.HIGH.value, Priority.MEDIUM.value, Priority.LOW.value}

    if priority is not None and priority not in valid_priorities:
        return NOT_VALID_PRIORITY
    return OK


def assert_severity_is_valid(severity=None):
    valid_severities = {Severity.CRITICAL.value,
                        Severity.HIGH.value, Severity.MEDIUM.value, Severity.LOW.value}

    if severity is not None and severity not in valid_severities:
        return NOT_VALID_SEVERITY
    return OK


def assert_state_is_valid(state=None):
    valid_states = {TicketState.OPEN.value,
                    TicketState.IN_PROGRESS.value, TicketState.CLOSED.value}

    if state is not None and state not in valid_states:
        if state == TicketState.NEW.value:
            return STATE_CHANGE_TO_NEW
        return NOT_VALID_STATE
    return OK
    
def assert_needs_resource_assignment(ticket, state):
    if state != TicketState.NEW.value and not ticket.resource_name:
        return NO_RESOURCE_ASSIGNED
    return OK

def update_ticket_by_id(ticket_id, title=None, description=None, priority=None, severity=None,
                        product_version_id=None, resource_name=None, client_id=None, state=None):

    result = assert_ticket_data_is_valid(
        title, description, priority, severity, state)
    if result != OK:
        return result, {}, HTTPStatus.BAD_REQUEST

    with BaseSQLConnection("main") as base_dao:
        ticket_dao = TicketDao(base_dao.get_session())

        ticket = ticket_dao.get_ticket_by_id(ticket_id)

        if not ticket:
            return TICKET_NOT_FOUND, {}, HTTPStatus.NOT_FOUND

        if title and ticket.title != title:
            ticket.title = title
        if description and ticket.description != description:
            ticket.description = description
        if priority and ticket.priority != priority:
            ticket.priority = priority
        if severity and ticket.severity != severity:
            ticket.severity = severity
        if product_version_id and ticket.product_version_id != product_version_id:
            ticket.product_version_id = product_version_id
        if resource_name and ticket.resource_name != resource_name:
            ticket.resource_name = resource_name
        if client_id and ticket.client_id != client_id:
            ticket.client_id = client_id
        if state and ticket.state != state:
            result = assert_needs_resource_assignment(ticket, state)
            if result != OK:
                return result, {}, HTTPStatus.BAD_REQUEST
            ticket.state = state

        ticket.updated_date = datetime.now()
        ticket_dao.session.commit()

        return OK, ticket.to_dict(), HTTPStatus.OK


# I believe we should not handle the get of tickets by multiple parameters in this layer
# We could have two gets: get_ticket_by_id() and get_all_tickets()
# The UI should handle the filtering of tickets by multiple parameters once received
def get_tickets_by(ticket_ids=[], prioritys=[], severitys=[], product_version_ids=[],
                resource_names=[], client_ids=[], states=[], expiration=False):

    with BaseSQLConnection("main") as base_dao:
        ticket_dao = TicketDao(base_dao.get_session())

        if expiration:
            date_from = datetime.today()
            date_to = date_from + timedelta(days=DAYS_NEXT_TO_EXPIRATION)
            tickets = ticket_dao.get_tickets_by(ticket_ids, prioritys, severitys, product_version_ids,
                                                resource_names, client_ids, states, date_from, date_to)
        else:
            tickets = ticket_dao.get_tickets_by(ticket_ids, prioritys, severitys, product_version_ids,
                                                resource_names, client_ids, states)

        if not tickets:
            return OK, [], HTTPStatus.OK 

        return OK, [t.to_dict() for t in tickets], HTTPStatus.OK    
    
def add_task_to_ticket(ticket_id, task_id):
    with BaseSQLConnection("main") as base_dao:
        ticket_dao = TicketDao(base_dao.get_session())

        ticket = ticket_dao.get_ticket_by_id(ticket_id)
        if not ticket:
            return TICKET_NOT_FOUND, {}, HTTPStatus.BAD_REQUEST
        
        task = ticket_dao.get_ticket_task(ticket_id, task_id)
        if task:
            return TASK_ALREADY_ASSIGNED, {}, HTTPStatus.BAD_REQUEST

        task = ticket_dao.add_task_to_ticket(ticket_id, task_id)
        if not task:
            return TASK_NOT_CREATED, {}, HTTPStatus.BAD_REQUEST
        ticket_dao.session.commit()

        return OK, task.to_dict(), HTTPStatus.OK
    
def get_ticket_tasks(ticket_id):
    with BaseSQLConnection("main") as base_dao:
        ticket_dao = TicketDao(base_dao.get_session())

        ticket = ticket_dao.get_ticket_by_id(ticket_id)
        if not ticket:
            return TICKET_NOT_FOUND, {}, HTTPStatus.BAD_REQUEST

        tasks = ticket_dao.get_ticket_tasks(ticket_id)
        response = {
            'ticket_id': ticket_id,
            'task_ids': [t.to_dict().get('task_id', 0) for t in tasks]
        }
        return OK, response, HTTPStatus.OK