"""
Product DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from dotenv import load_dotenv, find_dotenv
import mysql.connector
from models.product import Product

class ProductDAO:
    def __init__(self):
        try:
            env_path = find_dotenv(".env.local") or find_dotenv()
            print("Using .env:", env_path)
            load_dotenv(dotenv_path=env_path)
            db_host = os.getenv("MYSQL_HOST")
            db_name = os.getenv("MYSQL_DB_NAME")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD")     
            self.conn = mysql.connector.connect(
                host=db_host, 
                user=db_user, 
                password=db_pass, 
                database=db_name
            )   
            self.cursor = self.conn.cursor(dictionary=True)  # retour sous forme de dict
        except FileNotFoundError:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """Select all products from MySQL"""
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()
        return [Product(r["id"], r["name"], r["brand"], r["price"]) for r in rows]

    def select_by_id(self, product_id):
        """Select one product by ID"""
        self.cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        row = self.cursor.fetchone()
        if row:
            return Product(row["id"], row["name"], row["brand"], row["price"])
        return None

    def insert(self, product):
        """Insert given product into MySQL"""
        sql = "INSERT INTO products (name, brand, price) VALUES (%s, %s, %s)"
        values = (product.name, product.brand, product.price)
        self.cursor.execute(sql, values)
        self.conn.commit()
        return self.cursor.lastrowid  # retourne l'ID inséré

    def update(self, product):
        """Update given product in MySQL"""
        sql = "UPDATE products SET name=%s, brand=%s, price=%s WHERE id=%s"
        values = (product.name, product.brand, product.price, product.id)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def delete(self, product_id):
        """Delete product from MySQL with given product ID"""
        sql = "DELETE FROM products WHERE id=%s"
        self.cursor.execute(sql, (product_id,))
        self.conn.commit()

    def delete_all(self):  # optional
        """Empty products table in MySQL"""
        self.cursor.execute("DELETE FROM products")
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
