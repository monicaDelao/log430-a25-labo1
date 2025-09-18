from daos.product_dao import ProductDAO
from models.product import Product

dao = ProductDAO()

def setup_function():
    """Nettoie la table avant chaque test"""
    dao.delete_all()

def teardown_function():
    """Nettoie la table après chaque test"""
    dao.delete_all()

def test_product_select():
    p = Product(None, "Laptop", "Dell", 1200.00)
    new_id = dao.insert(p)
    products = dao.select_all()

    assert len(products) == 1
    assert products[0].id == new_id
    assert products[0].name == "Laptop"
    assert products[0].brand == "Dell"
    assert float(products[0].price) == 1200.00

def test_product_insert():
    p = Product(None, "Phone", "Samsung", 800.00)
    new_id = dao.insert(p)
    products = dao.select_all()

    assert any(prod.id == new_id and prod.name == "Phone" for prod in products)

def test_product_update():
    p = Product(None, "Tablet", "Apple", 900.00)
    new_id = dao.insert(p)
    p.id = new_id
    p.name = "iPad"
    dao.update(p)

    updated = dao.select_by_id(new_id)
    assert updated.name == "iPad"
    assert updated.brand == "Apple"

def test_product_delete():
    p = Product(None, "Monitor", "LG", 300.00)
    new_id = dao.insert(p)

    dao.delete(new_id)
    products = dao.select_all()
    assert len(products) == 0
