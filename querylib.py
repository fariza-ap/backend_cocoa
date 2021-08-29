import mysql.connector #creating connection to database
import json #import data jason to database
import secrets #manage sensitive data with docker (?)
from uuid import uuid4 #store uuid4 to mysql 

def sql_connection(): #create database name sql_connection
    sql = mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="",
                                  database="db_cocoa") #use host, username, pw from sql database db_cocoa
    return sql #terminate procedure

#insert a record in the "tb_user" table:
def input_user(user_id,username,email,no_hp,password,otoritas):
    db = sql_connection() 
    cursor = db.cursor() #cursor untuk mengeksekusi perintah SQL
    #"try" block will generate an exception if it's not defined
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

def token_generator(): #define token generator
    return secrets.token_hex(256) #generate secure random numbers for managing secrets


def get_user_id_base_username_and_password(username,password):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT `user_id` FROM `tb_user` WHERE `username`=%s AND password = %s",(username,password))
        c = cursor.fetchone() #Ini mengambil baris berikut dari kumpulan hasil query. Set hasil adalah objek yang dikembalikan saat objek kursor digunakan untuk query tabel.
        set = True
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = e
        set = False
    if set==False:
        return None
    else:
        if c==None:
            return None
        else:
            return c[0]
    #kalau username pw salah, akan muncul exception

def update_token_base_user_id(user_id):
    db = sql_connection() 
    cursor = db.cursor()
    token = token_generator()
    try:
        cursor.execute("UPDATE `tb_user` SET `dt_last_login`=CURDATE(),`dt_expired`=ADDDATE(CURDATE(),INTERVAL 7 DAY),`token`=%s WHERE `user_id`=%s",(token,user_id))
        db.commit() #committ changes (menyimpan data)
        set = True
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e) #print exception-nya
        set = False
    if set==False:
        token = token_generator()
        try:
            cursor.execute("UPDATE `tb_user` SET `dt_last_login`=CURDATE(),`dt_expired`=ADDDATE(CURDATE(),INTERVAL 7 DAY),`token`=%s WHERE `user_id`=%s",(token,user_id))
            db.commit() #committ changes (nyimpen update data)
        except(mysql.connector.Error,mysql.connector.Warning) as e:
            print(e)
    return token
        
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
        #cek session apakah membutuhkan false atau true


def update_left_time_token(token):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE `tb_user` SET `dt_last_login`=CURDATE(),`dt_expired`= ADDDATE(CURDATE(),INTERVAL 7 DAY) WHERE `token`= %s",(token,))
        db.commit() #commit changes (simpan data)
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
    #try "block" will generate exception if it's not define

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
        return None #ga ada return value(?)
    else:
        return c[0]
    
def get_date_expired(token):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT  `dt_expired` FROM `tb_user` WHERE `token`=%s",(token,))
        c = cursor.fetchone() #Ini mengambil baris berikut dari kumpulan hasil query. Set hasil adalah objek yang dikembalikan saat objek kursor digunakan untuk query tabel.
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    if c==None:
        return None
    else:
        return c[0]
    
def compare_date(token): #membandingkan data (tanggal)
    date_last_login = get_date_last_login(token)
    date_expired = get_date_expired(token)
    if date_last_login>=date_expired: #tgl last login lebih lama dari data expired
        return False #muncul exception
    else:
        return True

def gen_id_user(otoritas):
    oto = ''
    if otoritas==0:
        oto = 'ADM' #admin
    elif otoritas==1:
        oto = 'FAM' #farmer
    else:
        oto = "CUS" #customer
    data = str(uuid4().hex)
    result = oto+"-"+data
    return result

def get_otoritas_user(user_id):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT `otoritas` FROM `tb_user` WHERE `user_id`=%s",(user_id,))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    if c==None:
        return None
    else:
        return c[0]


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
        set = False
        return set,None
    else:
        return True,c[0]

def update_last_login_base_on_token(token):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE `tb_user` SET `dt_last_login`=now() WHERE `token`=%s",(token,))
        db.commit()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        
def cek_status_user(user_id):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT tb_user.`status`,tb_status_user.status FROM `tb_user` INNER JOIN tb_status_user ON tb_user.status=tb_status_user.id WHERE user_id=%s",(user_id,))
        c = cursor.fetchone()
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        c = None
    if c == None:
        set = False
        result = "No-Status"
    else:
        status = int(c[0])
        result = c[1]
        if status==0 or status ==2:
            set = False
        else:
            set = True
    return set,result 


def gen_id_karung():
    karung = "KRG"
    data = str(uuid4().hex)
    result = karung+"-"+data
    return result

def input_cocoa(berat_bersih, berat_kotor,agent):    
    db = sql_connection()
    cursor = db.cursor() #execute SQL querry
    input = gen_id_karung()
    try:
        cursor.execute("INSERT INTO `tb_panen`(`id_karung`, `berat_kotor`, `berat_bersih`, `add_by`, `update_by`, `dt_add`, `dt_update`, `status`) VALUES (%s,%s,%s,%s,%s,now(),now(),0)",(input,berat_bersih,berat_kotor,agent,agent))
        db.commit() #menyimpan data
        set = True #prosesnya benar
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e) #print exceptionnya jika tidak terdefine
        set = False
    if set==False:
        return False
    else:
        return True

def input_fermentasi(id_kotak,id_karung,suhu,ph,kelembapan,agent,device,kondisi):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO `tb_fermentasi`(`id_kotak`, `id_karung`, `suhu`, `ph`, `kelembapan`, `add_by`, `update_by`, `dt_add`, `dt_update`, `device`, `kondisi`) VALUES (%s,%s,%s,%s,%s,%s,%s,now(),now(),%s,%s)",(id_kotak,id_karung,suhu,ph,kelembapan,agent,agent,device,kondisi))        
        db.commit()
        set = True
    except(mysql.connector.Error,mysql.connector.Warning) as e:
           print(e)
           set = False
    if set==False:
        return False
    else:
        return True 

def update_status_cocoa(id,berat_kotor,berat_bersih,update_by,status):
    db = sql_connection()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE `tb_panen` SET `berat_kotor`=%s,`berat_bersih`=%s,`update_by`=%s,`dt_update`=now(),`status`=%s WHERE `id_karung`=%s",(berat_kotor,berat_bersih,update_by,status,id))
        db.commit()
        set = True #jika berhasil, tambahin biar tau kalau error (sangat recommended)
    except(mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        set = False #untuk di API, response code
    if set==False:
        return False
    else:
        return True
