from controllers.product_controller import ProductController

class ProductView:
    def __init__(self):
        self.controller = ProductController()

    def show_all(self):
        products = self.controller.get_all_products()
        for product in products:
            print(f"{product.id}: {product.name} - {product.brand} - ${product.price}")

    def add_product(self):
        name = input("Nom du produit: ")
        brand = input("Marque: ")
        price = float(input("Prix: "))
        self.controller.add_product(name, brand, price)
        print("Produit ajouté avec succès !")

    def delete_product(self):
        product_id = int(input("ID du produit à supprimer: "))
        self.controller.delete_product(product_id)
        print("Produit supprimé.")
