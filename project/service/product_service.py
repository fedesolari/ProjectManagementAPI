from http import HTTPStatus
from project.dao.product_dao import ProductDao
from project.utils.sql_connection import BaseSQLConnection
from project.responses.response_constants import OK

def get_products():

    with BaseSQLConnection("main") as base_dao:
        product_dao = ProductDao(base_dao.get_session())
        products = product_dao.get_products()

        return OK, [product.to_dict() for product in products], HTTPStatus.OK
    

def get_products_version():

    with BaseSQLConnection("main") as base_dao:
        product_dao = ProductDao(base_dao.get_session())
        products = product_dao.get_products_version()

        return OK, [product.to_dict() for product in products], HTTPStatus.OK