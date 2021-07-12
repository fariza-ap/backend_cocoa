from flask import Flask,request,jsonify
from querylib import input_user,get_user_id_base_username_and_password,verified_token
from querylib import compare_date,update_left_time_token,update_token_base_user_id

app = Flask(__name__)



if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=9001)
    app.run(port=9001, debug=True)
