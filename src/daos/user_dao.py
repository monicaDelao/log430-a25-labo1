"""
User DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from dotenv import load_dotenv, find_dotenv
from models import user
import mysql.connector
from models.user import User

class UserDAO:
    def __init__(self):
        try:
            env_path = find_dotenv(".env.local") or find_dotenv()
            print("Using .env:", env_path)
            load_dotenv(dotenv_path=env_path)
            db_host = os.getenv("MYSQL_HOST")
            db_name = os.getenv("MYSQL_DB_NAME")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD")    
            self.conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pass, database=db_name) 
            self.cursor = self.conn.cursor()
        except FileNotFoundError as e:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all users from MySQL """
        self.cursor.execute("SELECT id, name, email FROM users")
        rows = self.cursor.fetchall()
        return [User(*row) for row in rows]

    def insert(self, user):
        """ Insert given user into MySQL """
        self.cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (user.name, user.email)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, user):
        try:
            sql = "UPDATE users SET name = %s, email = %s WHERE id = %s"
            values = (user.name, user.email, user.id)
            self.cursor.execute(sql, values)
            self.conn.commit()
        except Exception as e:
            print("Erreur update :", e)
        

    def delete(self, user_id):
        try:
            sql = "DELETE FROM users WHERE id = %s"
            self.cursor.execute(sql, (user_id,))
            self.conn.commit()
        except Exception as e:
            print("Erreur delete :", e)

    def delete_all(self): #optional
        """ Empty users table in MySQL """
        pass
        
    def close(self):
        self.cursor.close()
        self.conn.close()
