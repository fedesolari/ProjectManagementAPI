from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

ENGINES_MAP = {}

def get_db_connection_string():
    # get connection info. you cannot do it outside of app context.
    db_user = current_app.config.get('POSTGRES_USER')
    db_pass = current_app.config.get('POSTGRES_PASSWORD')
    db_host = current_app.config.get('POSTGRES_IP')
    db_port = current_app.config.get('POSTGRES_PORT')
    connection_string = 'postgresql+psycopg2://{}:{}@{}:{}/DB_NAME'.format(db_user, db_pass, db_host, db_port)
    return connection_string 
    # return 'postgresql://support:0aFeWQNYnsFSpYDeaW9jwpDhxKfQXRC2@dpg-chsk4uhmbg57s5r5m1d0-a/main_070f'


def get_session_by_db_name(name):
    connection_string = get_db_connection_string()

    engine = ENGINES_MAP.get(name)
    if not engine:
        # if not exists, we create it and save it in the map
        engine = create_engine(connection_string.replace("DB_NAME", name))
        ENGINES_MAP[name] = engine

    # create session.
    session = Session(bind=engine)
    return session

class BaseSQLConnection:

    def __init__(self, name):
        # create engine.
        self.name = name


    def __enter__(self):
        self.session = get_session_by_db_name(self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


    def get_session(self):
        return self.session

    def commit(self):
        self.session.commit()


class BaseDao:
    
    def __init__(self, session):
        self.session = session

    def get_session(self):
        return self.session