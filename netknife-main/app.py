from flask import Flask,request,render_template
from flask_cors import CORS
import json

from data import AppInfo
from storage import AppStorage
from net import AppNet,net_checkip

pub_data=AppInfo()
storage=AppStorage()



netknife=Flask(__name__)
CORS(netknife,resource=r'/*')


@netknife.route('/')
def index():
    return render_template('index.html')

@netknife.route('/commit',methods=['POST'])
def adddevice():
    pub_data.login_dict=json.loads(request.get_data(as_text=True))
    if storage.add_login_info():
        return 'AddOK!!!'
    else:
        return 'AddFAULT...'
@netknife.route('/checkip',methods=['POST'])
def checkip():
    pub_data.check_ip_tuple=json.loads(request.get_data(as_text=True))
    print(pub_data.check_ip_tuple)
    return 'CheckOK!!!'
    # if net_checkip():
    #     return 'checkOk!!!'  
    # else:
    #     return 'checkFault...'

@netknife.route('/checkproject',methods=['POST'])
def checkproject():
    pass

if __name__ == '__main__':
    netknife.run('0.0.0.0',port=3000,debug=True)
 