import sqlite3
import time
import math 
import re 
from flask import url_for

class FDataBase:
    def __init__(self, db):
        self.__db = db 
        self.__cur = db.cursor()
    
    # def getMenu(self):
    #     sql = '''SELECT * FROM mainmenu'''
    #     try:
    #         self.__cur.execute(sql)
    #         res = self.__cur.fetchall()
    #         if res: return res 
    #     except:
    #         print("Ошибка чтения из БД")
    #     return []
    def addUser(self, username, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False 
            
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (username, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД" + str(e))
            return False 

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

                
            return res 

        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))
        
        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            
            return res 
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

        return False