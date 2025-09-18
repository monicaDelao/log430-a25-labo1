from daos.product_dao import ProductDAO
from models.product import Product

class ProductController:
    def __init__(self):
        self.dao = ProductDAO()

    def get_all_products(self):
        return self.dao.select_all()

    def add_product(self, name, brand, price):
        product = Product(None, name, brand, price)
        self.dao.insert(product)

    def delete_product(self, product_id):
        self.dao.delete(product_id)
