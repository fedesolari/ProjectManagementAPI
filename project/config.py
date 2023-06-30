from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class DevConfig:
    ENV = "dev"
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "pass"
    POSTGRES_IP = "0.0.0.0"
    POSTGRES_PORT = "5434"
    APISPEC_SWAGGER_URL = '/swagger/'
    APISPEC_SWAGGER_UI_URL = '/swagger-ui/'
    THIS_URL = "http://0.0.0.0:5001"

class LocalConfig:
    ENV = "local"
    POSTGRES_USER = "postgres"
    POSTGRES_IP = "localhost"
    POSTGRES_PORT = "5434"
    POSTGRES_PASSWORD = "pass"
    THIS_URL = "http://0.0.0.0:5001"

class ProdConfig:
    ENV = "prod"
    POSTGRES_USER = "support"
    POSTGRES_IP = "dpg-chsk4uhmbg57s5r5m1d0-a.oregon-postgres.render.com"
    POSTGRES_PASSWORD = "0aFeWQNYnsFSpYDeaW9jwpDhxKfQXRC2"
    POSTGRES_PORT = "5432"
    APISPEC_SWAGGER_URL = '/swagger/'
    APISPEC_SWAGGER_UI_URL = '/swagger-ui/'
