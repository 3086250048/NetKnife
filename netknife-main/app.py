from flask import Flask,request,render_template
from flask_cors import CORS
import json

from data import AppInfo
from storage import AppStorage
from net import AppNet

data=AppInfo()
storage=AppStorage()
net=AppNet()



netknife=Flask(__name__)
CORS(netknife,resource=r'/*')


@netknife.route('/')
def index():
    return render_template('index.html')

@netknife.route('/commit',methods=['POST'])
def commit():
    data.login_dict=json.loads(request.get_data(as_text=True))
    if storage.add_login_info(data.login_dict):
        return 'AddOK!!!'
    else:
        return 'AddFAULT...'
@netknife.route('/checkip_icmp',methods=['POST'])
def checkip_icmp():
    data.check_ip_tuple=json.loads(request.get_data(as_text=True))
    return net.check_ip_icmp(data.check_ip_tuple)

@netknife.route('/checkip_tcp',methods=['POST'])
def checkip_tcp():
    data.check_ip_tuple=json.loads(request.get_data(as_text=True))
    data.check_ip_port_str=json.loads(request.get_data(as_text=True))
    return net.check_ip_tcp(data.check_ip_tuple,data.check_ip_port_str)

@netknife.route('/check_project',methods=['POST'])
def checkproject():
    data.check_project_str=json.loads(request.get_data(as_text=True))
    result=storage.check_project(data.check_project_str)
    print(result)
    return True
    


if __name__ == '__main__':
    netknife.run('0.0.0.0',port=3000,debug=True)
 