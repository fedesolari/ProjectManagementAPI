from project.utils.sql_connection import BaseDao
from project.model.model import Product, ProductVersion

class ProductDao(BaseDao):

    def get_products(self):
        return self.session.query(Product).all()
        
    def get_products_version(self):
        return self.session.query(ProductVersion) \
            .all()