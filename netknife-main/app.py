from flask import Flask,request,render_template
from flask_cors import CORS
import json
from data import AppInfo
from storage import AppStorage


pub_data=AppInfo()
storage=AppStorage()



netknife=Flask(__name__)
CORS(netknife,resource=r'/*')


@netknife.route('/')
def index():
    return render_template('index.html')

@netknife.route('/commit',methods=['POST'])
def adddevice():
    if request.method=='POST':
        pub_data.login_dict=json.loads(request.get_data(as_text=True))
        if storage.add_login_info():
            return 'AddOK!!!'
        else:
            return 'AddFAULT...'
@netknife.route('/check',methods=['POST'])
def checkip():
    if request.method=='POST':
         pub_data.check_ip_dict=json.loads(request.get_data(as_text=True))
         return 'check'
    pass


if __name__ == '__main__':
    netknife.run('0.0.0.0',port=3000,debug=True)
 