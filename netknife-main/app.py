


__version__ = '1.0.0'

from flask import Flask,request,render_template
from flask_cors import CORS
import json
from data import AppInfo
from storage import AppStorage
from net import AppNet
from processing import AppProcessing
from processing import StorageProcessing
from server import APPserver
from action import ButtonAction


data=AppInfo()
storage=AppStorage()
net=AppNet()
ap=AppProcessing()
_as=APPserver()
ba=ButtonAction()
sp=StorageProcessing()

netknife=Flask(__name__)
CORS(netknife, resources={r"/*": {"origins": "*"}})


@netknife.route('/')
def index():
    return render_template('index.html')

@netknife.route('/select_count')
def select_count():
    return storage.select_count()

#向数据库中添加一条记录
#需要传入一个字典{'project':,'class':,'area':,'protocol':,
# 'port':,'username':,'password':,'secret':,'ip_expression':
@netknife.route('/commit',methods=['POST'])
def commit():
    data.login_dict=json.loads(request.get_data(as_text=True))
    if storage.add_login_info(data.login_dict):
        return 'ADD_SUCCESS'
    else:
        return 'ADD_FAULT'
    
#检查给定的ip列表是否会回应icmp请求，将请求失败的ip通过列表返回[1.1.1.1,2.2.2.2,...]
#需要传入一个IP表达式的字典{'ip_expression':}
@netknife.route('/checkip_icmp',methods=['POST'])
def checkip_icmp():
    data.check_ip_tuple=json.loads(request.get_data(as_text=True))
    return net.check_ip_icmp(data.check_ip_tuple)

#检查给定的ip列表的TCP端口是否开放,返回一个检测失败的端口列表[192.1.1.1,2.2.2.2,....]
#需要传入一个IP表达式和检测端口的字典{'ip_expression':,'port':}
@netknife.route('/checkip_tcp',methods=['POST'])
def checkip_tcp():
    data.check_ip_tuple=json.loads(request.get_data(as_text=True))
    data.check_ip_port_str=json.loads(request.get_data(as_text=True))
    return net.check_ip_tcp(data.check_ip_tuple,data.check_ip_port_str)

#检查最小单元在数据库中是否存在需要附带数据
# {'project':,'area':,'ip_expression':,'protocol':,'port':}
@netknife.route('/check_quads',methods=['POST'])
def checkp_quads():
    data.check_quads_dict=json.loads(request.get_data(as_text=True))
    result=storage.check_quads(data.check_quads_dict)
    if result:
        return 'NOT_USED'
    return 'USED'
#检查数据库中是否存在某条记录
# 需要一个{'project':,'class':,'area':,'protocol':,'port':,'username':,'password':,
# 'ip_expression':,'secret':,'check_protocol':}
@netknife.route('/check_where',methods=['POST'])
def check_where():
    data.where_dict=json.loads(request.get_data(as_text=True))
    result=storage.check_where(data.where_dict)
    if result:
        return 'NOT_EXIST'
    return 'EXIST'

@netknife.route('/get_project_area_data')
def get_project_area_data():
    return storage.get_project_area_data()


@netknife.route('/get_project_area')
def get_project_area():
    return storage.get_project_area()

#更新数据库中的记录
#使用时先向/check_where发送更新条件,再向这个接口发送更新请求,需要附带数据,结构如下
#{'project':,'class':,'area':,'protocol':,'port':,'username':,'password':,
#'ip_expression':,'secret':,'check_protocol':}
@netknife.route('/update_data',methods=['POST'])
def update_data():
    data.update_data_dict=json.loads(request.get_data(as_text=True))
    result=storage.update_data(data.where_dict,data.update_data_dict)
    if result:
        return 'UPDATE_SUCCESS'
    return 'UPDATE_FAULT'
#删除数据库中的记录
#使用时先向/check_where发送删除条件,再向这个接口发送删除请求无需附带数据
@netknife.route('/delete_data',methods=['POST'])
def delete_data():
    result=storage.delete_data(data.where_dict)
    if result:
        return 'DELETE_SUCCESS'
    return 'DELETE_FAULT'

#[['projetc1','area1 、area2','protocol1 ; protocol2','port1 ; port2','ip_expression'],[...]]
#不需要传入数据
@netknife.route('/get_project_unit_data',methods=['POST'])
def get_project_unit_data():
    return storage.get_project_unit_list()

#获取数据库中所有项目(去重)(由于element-ui组建要求只能返回这种格式的列表) 
# [ {'value':默认项目},{'value':默认项目2}]
#不需要传入数据
@netknife.route('/get_all_project_data',methods=['POST'])
def get_all_project_data(): 
    return storage.get_all_project_list()


# 获取影响连接的百分比,{'effect_connect_percent':'xxx'}
# 需要传入一个字典{'base_effect_range':'项目名称','command':'where 语句'}
@netknife.route('/get_effect_data',methods=['POST'])
def get_effect_data():
    result=ap.processing_effect_command(json.loads(request.get_data(as_text=True)))
    return result

#获取批量执行命令的回显
@netknife.route('/commit_command',methods=['POST'])
def commit_command():
    data.effect_login_dict=json.loads(request.get_data(as_text=True))
    data.command_str=json.loads(request.get_data(as_text=True))
    result=net.send_command(data.effect_login_dict,data.command_str)
    return result

@netknife.route('/add_filepath_parameter',methods=['POST'])
def add_filepath_parameter():
    result=storage.add_filepath_parameter(json.loads(request.get_data(as_text=True)))
    if result:
        return 'ADD_SUCCESS'
    else:
        return 'ADD_FAULT'
    
@netknife.route('/change_filepath_parameter',methods=['POST'])
def change_filepath_parameter():
    result=storage.change_filepath_parameter(json.loads(request.get_data(as_text=True)))
    if result:
        return 'CHANGE_SUCCESS'
    else:
        return 'CHANGE_FAULT'
@netknife.route('/get_filepath_parameter',methods=['POST'])
def get_filepath_parameter():
    result=storage.get_filepath_parameter(json.loads(request.get_data(as_text=True)))
    if result:
        print(result)
        return result

    
@netknife.route('/delete_filepath_parameter',methods=['POST'])
def delete_filepath_parameter():
    result=storage.delete_filepath_parameter(json.loads(request.get_data(as_text=True)))
    if result:
        return 'DELETE_SUCCESS'
    else:
        return 'DELETE_FAULT'


@netknife.route('/add_sendcommand_parameter',methods=['POST'])
def add_sendcommand_parameter():
    result=storage.add_sendcommand_parameter(json.loads(request.get_data(as_text=True)))
    if result:
        return 'ADD_SUCCESS'
    else:
        return 'ADD_FAULT'
    
@netknife.route('/change_sendcommand_parameter',methods=['POST'])
def change_sendcommand_parameter():
    result=storage.change_sendcommand_parameter(json.loads(request.get_data(as_text=True)))
    if result:
        return 'CHANGE_SUCCESS'
    else:
        return 'CHANGE_FAULT'
    
@netknife.route('/get_sendcommand_parameter',methods=['POST'])
def get_sendcommand_parameter():

    print('get_sendcommand_parameter')  

    result=storage.get_sendcommand_parameter(json.loads(request.get_data(as_text=True)))
    
    if result:
        print(result)
        return result

@netknife.route('/delete_sendcommand_parameter',methods=['POST'])
def delete_sendcommand_parameter():
    result=storage.delete_sendcommand_parameter(json.loads(request.get_data(as_text=True)))
    if result:
        return 'DELETE_SUCCESS'
    else:
        return 'DELETE_FAULT'

@netknife.route('/start_ftp_server',methods=['POST'])
def start_ftp_serve():
    result=_as.start_ftp_server(json.loads(request.get_data(as_text=True)))
    return result
@netknife.route('/stop_ftp_serve')
def stop_ftp_serve():
   result= _as.stop_ftp_serve()
   return result

@netknife.route('/update_parameter_database',methods=['POST'])
def update_parameter_database():
    result= storage.update_parameter_database(json.loads(request.get_data(as_text=True)))
    return result

@netknife.route('/get_mixunit_data',methods=['POST'])
def get_mixunit_data():
    result= storage.get_mixunit_data(json.loads(request.get_data(as_text=True)))
    return result
@netknife.route('/get_search_data',methods=['POST'])
def get_search_data():
    result=storage.get_search_data(json.loads(request.get_data(as_text=True)))
    return result
@netknife.route('/add_command_history',methods=['POST'])
def add_command_history():
    result=storage.add_command_history(json.loads(request.get_data(as_text=True)))
    if result=='LIMIT':
        return result
    if result:
        return 'ADD_SUCCESS'
    else:
        return 'ADD_FAULT'
@netknife.route('/get_command_history',methods=['POST'])
def get_command_history():
    result=storage.get_command_history(json.loads(request.get_data(as_text=True)))
    return result
@netknife.route('/get_command_history_count',methods=['POST'])
def get_command_history_count():
    result=storage.get_command_history_count(json.loads(request.get_data(as_text=True)))
    return result

@netknife.route('/get_id_mixunit_data')
def get_id_mixunit_data():
    result=storage.get_database_data('LOGININFO',['ID','PROJECT','AREA','PROTOCOL','PORT','IP_EXPRESSION'])
    return result

@netknife.route('/update_command_history_database',methods=['POST'])
def update_command_history_database():
    result=storage.update_command_history_database(json.loads(request.get_data(as_text=True)))
    if result:
        return 'UPDATE_SUCCESS'
    else:
        return 'UPDATE_FAULT'

@netknife.route('/export_textarea',methods=['POST'])
def export_textarea():
    result=ba.export_textarea(json.loads(request.get_data(as_text=True)))
    if result:
        return 'EXPORT_SUCCESS'
    else:
        return 'EXPORT_FAULT'
@netknife.route('/get_all_command_time',methods=['POST'])
def get_all_command_time():
    where_dict=ap.processing_command_history_where_dict(json.loads(request.get_data(as_text=True)))
    result=storage.get_database_data('COMMAND_HISTORY',['COMMAND','DATE_TIME','ID'],where_dict,'ORDER BY DATE_TIME DESC')
    _result=ap.processing_command_history_result(result)
    print(_result)
    return _result
@netknife.route('/delete_history_command',methods=['POST'])
def delete_history_command():
    where_dict=ap.processing_command_history_where_dict(json.loads(request.get_data(as_text=True)))
    result=storage.del_database_data('COMMAND_HISTORY',where_dict)
    if result:
        return 'DELETE_SUCCESS'
    else:
        return 'DELETE_FAULT'

@netknife.route('/get_delete_project_list',methods=['POST'])
def get_delete_project_list():
    where_dict=json.loads(request.get_data(as_text=True))
    result=storage.get_database_data('LOGININFO',['PROJECT'],where_dict)
    print('====================get_delete_project_list********************************************')
    print(result)
    return result

@netknife.route('/get_logininfo_project_count',methods=['POST'])
def get_history_command_count():
    where_dict=json.loads(request.get_data(as_text=True))
    print('=====================================where_dict')
    print(where_dict)
    result=storage.get_database_data_count('LOGININFO',where_dict)
    print('==============================================================')
    print(result)
    if result:
        return 'DELETE_NEXT'
    else:
        return 'DELETE_STOP'

@netknife.route('/delete_parameter_database',methods=['POST'])
def delete_parameter_database():
    result= storage.delete_parameter_database(json.loads(request.get_data(as_text=True)))
    if result:
        return 'DELETE_SUCCESS'
    else:
        return 'DELETE_FAULT'
    
@netknife.route('/create_netknife_file',methods=['POST'])
def create_file():
    file_dict=sp.processing_netknife_file(json.loads(request.get_data(as_text=True)))
    if not file_dict: return 'SYNTAX_ERROR'
    result=storage.add_netknife_file(file_dict)
    if result:
        return file_dict['config']['name']
    else:
        return 'ADD_FAULT'

@netknife.route('/delete_netknife_file',methods=['POST'])
def delete_file():
    file_name=sp.processing_file_name_netknife_file(json.loads(request.get_data(as_text=True)))
    print(file_name)
    if not file_name: return 'SYNTAX_ERROR'
    result=storage.delete_netknife_file(file_name)
    if result:
        return 'DELETE_SUCCESS'
    else:
        return 'DELETE_FAULT' 

@netknife.route('/change_netknife_file',methods=['POST'])
def change_file():
    file_dict=sp.processing_netknife_file(json.loads(request.get_data(as_text=True)))
    file_name=sp.processing_file_name_netknife_file(json.loads(request.get_data(as_text=True)))
    print(file_dict)
    if not file_dict : return 'SYNTAX_ERROR'
    result=storage.change_netknife_file(file_name,file_dict)
    if result:
        return 'CHANGE_SUCCESS'
    else:
        return 'CHANGE_FAULT'
@netknife.route('/check_netknife_file_if_exist',methods=['POST'])
def check_file_if_exist():
    file_name=sp.processing_file_name_netknife_file(json.loads(request.get_data(as_text=True)))
    if not file_name: return 'SYNTAX_ERROR'
    result=storage.check_netknife_file_if_exist(file_name)
    if result:
        return 'EXIST'
    else:
        return 'NOT_EXIST'


if __name__ == '__main__':
    netknife.run('0.0.0.0',port=3000,debug=True)