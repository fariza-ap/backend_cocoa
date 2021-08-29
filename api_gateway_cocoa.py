from logging import info
from flask import Flask,request,jsonify
import hashlib
from querylib import cek_status_user, gen_id_user, get_otoritas_user, input_cocoa, input_user,get_user_id_base_username_and_password, update_last_login_base_on_token, update_status_cocoa,verified_token
from querylib import compare_date,update_left_time_token,update_token_base_user_id,input_fermentasi

app = Flask(__name__)

@app.route('/cocoa/user/regist',methods=['POST'])
def user_regist():
    try:
        json_data = request.json
    except ValueError as e:
        result = {"message":e}
        resp = jsonify(result)
        return resp,500
    
    if json_data==None:
        result = {"message":"Null Json"}
        resp = jsonify(result)
        return resp,400
    else:
        if 'username' not in json_data or 'email' not in json_data or 'no_hp' not in json_data or 'password' not in json_data or 'otoritas' not in json_data:
            result = {"message":"Request error"}
            resp = jsonify(result)
            return resp,401
        else:
            username = json_data['username']
            email = json_data['email']
            no_hp = json_data['no_hp']
            password = json_data['password']
            otoritas = int(json_data['otoritas'])
            password = hashlib.sha256(password.encode()).hexdigest()
            user_id = gen_id_user(otoritas)
            tes,res = input_user(user_id,username,email,no_hp,password,otoritas)
            if tes==False:
                result = {"message":"Regist Failed"}
                resp = jsonify(result)
                return resp,205
            else:
                result = {"message":"Regist Success"}
                resp = jsonify(result)
                return resp,202

@app.route('/cocoa/user/login',methods=['POST'])
def login_user():
    try:
        json_data = request.json
    except ValueError as e:
        result = {"message":e}
        resp = jsonify(result)
        return resp,500
    if json_data==None:
        result = {"message":"Null Json"}
        resp = jsonify(result)
        return resp,400
    else:
        if 'username' not in json_data or 'password' not in json_data:
            result = {"message":"Request error"}
            resp = jsonify(result)
            return resp,401
        else:
            username = json_data['username']
            password = json_data['password']
            password = hashlib.sha256(password.encode()).hexdigest()
            user_id = get_user_id_base_username_and_password(username,password)
            if user_id==None:
                result = {"message":"Unregisted Account"}
                resp = jsonify(result)
                return resp,203
            else:
                cek_status,status = cek_status_user(user_id)
                if cek_status==False:
                    result = {"message":"User status "+status}
                    resp = jsonify(result)
                    return resp,203
                else:
                    token = update_token_base_user_id(user_id)
                    otoritas = get_otoritas_user(user_id)
                    result = {"message":"OK",
                              "token":token,
                              "otoritas":otoritas}
                    resp = jsonify(result)
                    return resp,200


@app.route('/cocoa/user/verify',methods=['POST'])
def user_verify():
    try:
        json_data = request.headers
    except ValueError as e:
        result = {"message":e}
        resp = jsonify(result)
        return resp,500
    if 'token' not in json_data:
        result = {"message":"Request error"}
        resp = jsonify(result)
        return resp,401
    else:
        token = json_data['token']
        cek,user_id = verified_token(token)
        if cek == False:
            result = {"message":"Forbidden"}
            resp = jsonify(result)
            return resp,403
        else:
            cek_status,status = cek_status_user(user_id)
            if cek_status==False:
                result={"message":"User status "+status}
                resp = jsonify(result)
                return resp,203
            else:
                update_last_login_base_on_token(token)
                compare = compare_date(token)
                if compare==False:
                    result = {"message":"Token expired"}
                    resp = jsonify(result)
                    return resp,203
                else:
                    update_left_time_token(token)
                    otoritas = get_otoritas_user(user_id)
                    result = {"message":"Account Verified",
                              "otoritas":otoritas}
                    resp = jsonify(result)
                    return resp,200
                
@app.route('/cocoa/user/input_cocoa',methods=['POST'])
def cocoa_input():
    try:
        json_data = request.json
    except ValueError as e:
        result = {"message":e}
        resp = jsonify(result)
        return resp,500
    if 'token' not in json_data or 'berat_bersih' not in json_data or 'berat_kotor' not in json_data:
        result = {"message":"Request Error"}
        resp = jsonify(result)
        return resp,401
    else:
        token = json_data['token']
        berat_bersih = json_data['berat_bersih']
        berat_kotor = json_data['berat_kotor']
        cek,user_id = verified_token(token)
        if cek == False:
            result = {"message":"Forbidden"}
            resp = jsonify(result)
            return resp,403
        else:
            hasil = input_cocoa(berat_bersih,berat_kotor,user_id)
            if hasil == False:
                result = {"message":"Input Error"}
                resp = jsonify(result)
                return resp,205
            else:
                result = {"message":"Input Success"}
                resp = jsonify(result)
                return resp,200   

@app.route('/cocoa/user/update_cocoa',methods=['POST'])
def cocoa_update():
    try:
        json_data = request.json
    except ValueError as e:
        result = {"message":e}
        resp = jsonify(result)
        return resp,500
    if 'token' not in json_data or 'berat_bersih' not in json_data or 'berat_kotor' not in json_data or 'status' not in json_data or 'id_karung' not in json_data:
        result = {"message":"Request Error"}
        resp = jsonify(result)
        return resp,401
    else:
        token = json_data['token']
        berat_bersih = json_data['berat_bersih']
        berat_kotor = json_data['berat_kotor']
        status = json_data['status']
        id_karung = json_data['id_karung']
        cek,user_id = verified_token(token)
        if cek == False:
            result = {"message":"Forbidden"}
            resp = jsonify(result)
            return resp,403
        else:
            solo = update_status_cocoa(id_karung,berat_kotor,berat_bersih,user_id,status)
            if solo == False:
                result = {"message":"Update Error"}
                resp = jsonify(result)
                return resp,205
            else:
                result = {"message":"Update Success"}
                resp = jsonify(result)
                return resp,200

@app.route('/cocoa/user/input_fermentasi',methods=['POST'])
def fermentasi_input():
    try: #error checking, ditest dulu
        json_data = request.json
    except ValueError as e:
        result = {"message":e}
        resp = jsonify(result)
        return resp,500
    if 'token' not in json_data or 'id_kotak' not in json_data or 'id_karung' not in json_data or 'suhu' not in json_data or 'ph' not in json_data or 'kelembapan' not in json_data or 'device' not in json_data or 'kondisi' not in json_data:
        result = {"message":"Request Error"}
        resp = jsonify(result)
        return resp,401
    else:
        token = json_data['token']
        id_kotak = json_data['id_kotak']
        id_karung = json_data['id_karung']
        suhu = json_data['suhu']
        ph = json_data['ph']
        kelembapan = json_data['kelembapan']
        device = json_data['device']
        kondisi = json_data['kondisi']
        cek,user_id = verified_token(token)
        if cek == False:
            result = {"message":"Forbidden"}
            resp = jsonify(result)
            return resp,403
        else:
            fermentasi = input_fermentasi(id_kotak,id_karung,suhu,ph,kelembapan,user_id,device,kondisi)
            if fermentasi == False:
                result = {"message":"Input Fermentation Error"}
                resp = jsonify(result)
                return resp,205
            else:
                result = {"message":"Input Fermentation Success"}
                resp = jsonify(result)
                return resp,200

if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=9001)
    app.run(port=9001, debug=True)
