from sqlalchemy import INTEGER, VARCHAR, BOOLEAN, DATETIME, Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func
from project.model.base import Base
import enum
from datetime import timedelta
from sqlalchemy.orm import relationship
from datetime import datetime

DAYS_NEXT_TO_EXPIRATION = 2

class Severity(enum.Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class Priority(enum.Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class ServiceLevelAgreement(enum.Enum):
    S1 = timedelta(days=7)
    S2 = timedelta(days=30)
    S3 = timedelta(days=90)
    S4 = timedelta(days=365)

class TicketState(enum.Enum):
    NEW = 1
    OPEN = 2
    IN_PROGRESS = 3
    CLOSED = 4

class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    description = Column(VARCHAR(100), nullable=False)
    title = Column(VARCHAR(100), nullable=False)
    state = Column(INTEGER, nullable=False)
    severity = Column(INTEGER, nullable=False)
    priority = Column(INTEGER, nullable=False)
    SLA = Column(DATETIME, nullable=False)
    product_version_id = Column(INTEGER, nullable=False)
    resource_name = Column(VARCHAR(100), nullable=True)
    client_id = Column(INTEGER, nullable=False)
    created_date = Column(DATETIME, nullable=False, default=datetime.now())
    updated_date = Column(DATETIME, nullable=False, default=datetime.now())

    def __init__(self, title, description, state, severity, priority,
        SLA, product_version_id, resource_name, client_id):

        self.description = description
        self.title = title
        self.state = state
        self.severity = severity
        self.priority = priority
        self.SLA = SLA + datetime.now()
        self.product_version_id = product_version_id
        self.resource_name = resource_name
        self.client_id = client_id

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'title': self.title,
            'state': self.state,
            'severity' : self.severity,
            'priority' : self.priority,
            'SLA' : self.SLA,
            'product_version_id' : self.product_version_id,
            'client_id' : self.client_id,
            'resource_name' : self.resource_name,
        }
    

class Task(Base):
    __tablename__ = 'task'
    ticket_id = Column(INTEGER, ForeignKey("ticket.id"), primary_key=True, nullable=False)
    task_id = Column(INTEGER, primary_key=True, nullable=False)

    def __init__(self, ticket_id, task_id):
        self.ticket_id = ticket_id
        self.task_id = task_id

    def to_dict(self):
        return {
            'ticket_id': self.ticket_id,
            'task_id': self.task_id,
        }
    
class Product(Base):
    __tablename__ = 'product'
    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    product_versions = relationship("ProductVersion", uselist=False)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        version = self.product_versions.to_dict()
        return {
            'id': self.id,
            'name' : self.name,
            'version_name': version.get('version', ''), 
            'version_id': version.get('id', ''), 
        }

class ProductVersion(Base):
    __tablename__ = 'product_version'
    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    version = Column(VARCHAR(10), nullable=False)
    product_id = Column(INTEGER, ForeignKey("product.id"), nullable=False)

    def __init__(self, version, product_id):
        self.version = version
        self.product_id = product_id

    def to_dict(self):
        return {
            'id': self.id,
            'version' : self.version,
            'product_id' : self.product_id
        }