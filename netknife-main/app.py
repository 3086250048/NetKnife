from flask import Flask,request,render_template
from flask_cors import CORS
import json

from data import AppInfo
from storage import AppStorage
from net import AppNet
from processing import AppProcessing

data=AppInfo()
storage=AppStorage()
net=AppNet()
ap=AppProcessing()


netknife=Flask(__name__)
CORS(netknife,resource=r'/*')


@netknife.route('/')
def index():
    return render_template('index.html')

@netknife.route('/commit',methods=['POST'])
def commit():
    data.login_dict=json.loads(request.get_data(as_text=True))
    if storage.add_login_info(data.login_dict):
        return 'ADD_SUCCESS'
    else:
        return 'ADD_FAULT'
@netknife.route('/checkip_icmp',methods=['POST'])
def checkip_icmp():
    data.check_ip_tuple=json.loads(request.get_data(as_text=True))
    return net.check_ip_icmp(data.check_ip_tuple)

@netknife.route('/checkip_tcp',methods=['POST'])
def checkip_tcp():
    data.check_ip_tuple=json.loads(request.get_data(as_text=True))
    data.check_ip_port_str=json.loads(request.get_data(as_text=True))
    return net.check_ip_tcp(data.check_ip_tuple,data.check_ip_port_str)

@netknife.route('/check_quads',methods=['POST'])
def checkp_quads():
    data.check_quads_dict=json.loads(request.get_data(as_text=True))
    result=storage.check_quads(data.check_quads_dict)
    print(result)
    if result:
        return 'NOT_USED'
    return 'USED'
    
@netknife.route('/check_where',methods=['POST'])
def check_where():
    data.where_dict=json.loads(request.get_data(as_text=True))
    result=storage.check_where(data.where_dict)
    if result:
        return 'NOT_EXIST'
    return 'EXIST'
@netknife.route('/update_data',methods=['POST'])
def update_data():
    data.update_data_dict=json.loads(request.get_data(as_text=True))
    result=storage.update_data(data.where_dict,data.update_data_dict)
    if result:
        return 'UPDATE_SUCCESS'
    return 'UPDATE_FAULT'
@netknife.route('/delete_data',methods=['POST'])
def delete_data():
    result=storage.delete_data(data.where_dict)
    if result:
        return 'DELETE_SUCCESS'
    return 'DELETE_FAULT'

@netknife.route('/get_project_unit_data',methods=['POST'])
def get_project_unit_data():
    return storage.get_project_unit_list()
    

if __name__ == '__main__':
    netknife.run('0.0.0.0',port=3000,debug=True)
 