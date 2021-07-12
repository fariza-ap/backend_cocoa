import mysql.connector
import json
import secrets

from mysql.connector import cursor

def sql_connection():
    sql = mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="",
                                  database="db_cocoa")
    return sql

def input_user(user_id,username,email,no_hp,password,otoritas):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO `tb_user`(`user_id`, `username`, `email`, `no_hp`, `password`, `dt_update`, `dt_add`, `dt_expired`, `status`, `otoritas`) VALUES (%s,%s,%s,%s,%s,now(),now(),now(),0,%s)",(user_id,username,email,no_hp,password,otoritas))
        db.commit()
        info = "Input Success"
        set = True
    except(mysql.connector.Warning,mysql.connector.Error) as e:
        print(e)
        set = False
        info = e
    return set,info

def token_generator():
    return secrets.token_hex(256)


def get_user_id_base_username_and_password(username,password):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT `user_id` FROM `tb_user` WHERE `username`=%s AND password = %s",(username,password))
        c = cursor.fetchone()
        set = True
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = e
        set = False
    return set,c
    

def update_token_base_user_id(user_id):
    db = sql_connection()
    cursor = db.cursor()
    token = token_generator()
    try:
        cursor.execute("UPDATE `tb_user` SET `dt_last_login`=CURDATE(),`dt_expired`=ADDDATE(CURDATE(),INTERVAL 7 DAY),`token`=%s WHERE `user_id`=%s",(token,user_id))
        db.commit()
        set = True
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        set = False
    if set==False:
        token = token_generator()
        try:
            cursor.execute("UPDATE `tb_user` SET `dt_last_login`=CURDATE(),`dt_expired`=ADDDATE(CURDATE(),INTERVAL 7 DAY),`token`=%s WHERE `user_id`=%s",(token,user_id))
            db.commit()
        except(mysql.connector.Error,mysql.connector.Warning) as e:
            print(e)
        
def verified_token(token):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT `user_id` FROM `tb_user` WHERE `token`=%s",(token,))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    if c==None:
        return False
    else:
        return True


def update_left_time_token(token):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE `tb_user` SET `dt_last_login`=CURDATE(),`dt_expired`= ADDDATE(CURDATE(),INTERVAL 7 DAY) WHERE `token`= %s",(token,))
        db.commit()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
    

def get_date_last_login(token):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT  `dt_last_login` FROM `tb_user` WHERE `token`=%s",(token,))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    if c==None:
        return None
    else:
        return c[0]
    
def get_date_expired(token):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT  `dt_expired` FROM `tb_user` WHERE `token`=%s",(token,))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    if c==None:
        return None
    else:
        return c[0]
    
def compare_date(token):
    date_last_login = get_date_last_login(token)
    date_expired = get_date_expired(token)
    if date_last_login>=date_expired:
        return False
    else:
        return True
              
    