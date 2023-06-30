from project.model.model import Ticket, Task
from project.utils.sql_connection import BaseDao
from sqlalchemy import desc


class TicketDao(BaseDao):

    def get_ticket_by_id(self, id):     

        ticket = self.session.query(Ticket) \
            .filter(Ticket.id == id).first()

        return ticket

    def create_ticket(self, title, description, state, severity, priority,
                      SLA, product_version_id, resource_name, client_id):

        ticket = Ticket(title, description, state, severity, priority,
                        SLA, product_version_id, resource_name, client_id)

        self.session.add(ticket)

        return ticket

    def delete_ticket_by_id(self, ticket_id):

        return self.session.query(Ticket) \
            .filter(Ticket.id == ticket_id).delete()
            
    def get_all_tickets(self, product_version_id):
        query = self.session.query(Ticket)
        
        if product_version_id:
            query = query.filter(
                Ticket.product_version_id.in_(product_version_id))

        return query.all()

    def get_tickets_by(self, ticket_ids=[], prioritys=[], severitys=[], product_version_ids=[],
                       resource_names=[], client_ids=[], states=[], date_from=None, date_to=None):

        query = self.session.query(Ticket)

        if ticket_ids:
            query = query.filter(Ticket.id.in_(ticket_ids))
        if prioritys:
            query = query.filter(Ticket.priority.in_(prioritys))
        if severitys:
            query = query.filter(Ticket.severity.in_(severitys))
        if product_version_ids:
            query = query.filter(
                Ticket.product_version_id.in_(product_version_ids))
        if resource_names:
            query = query.filter(Ticket.resource_name.in_(resource_names))
        if client_ids:
            query = query.filter(Ticket.client_id.in_(client_ids))
        if states:
            query = query.filter(Ticket.state.in_(states))

        if date_from:
            query = query.filter(Ticket.SLA >= date_from)
        if date_to:
            query = query.filter(Ticket.SLA <= date_to)

        query = query.order_by(desc(Ticket.updated_date))

        return query.all()
    
    def add_task_to_ticket(self, ticket_id, task_id):
        task = Task(ticket_id, task_id)
        self.session.add(task)

        return task
    
    def get_ticket_task(self, ticket_id, task_id):
        return self.session.query(Task) \
            .filter(Task.ticket_id == ticket_id, Task.task_id == task_id).all()
    
    def get_ticket_tasks(self, ticket_id):
        return self.session.query(Task).filter(Task.ticket_id == ticket_id).all()
