from logging import info
from flask import Flask,request,jsonify
import hashlib
from querylib import gen_id_user, input_user,get_user_id_base_username_and_password,verified_token
from querylib import compare_date,update_left_time_token,update_token_base_user_id

app = Flask(__name__)

@app.route('/cocoa/regist/user',methods=['POST'])
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
            
            
        
if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=9001)
    app.run(port=9001, debug=True)
