from concurrent.futures import ThreadPoolExecutor
from multiping import MultiPing
from tcping import Ping
from netmiko import ConnectHandler

from storage import AppStorage
from processing import AppProcessing
from action import AppAction

import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
from copy import deepcopy
from pprint import pprint

storage=AppStorage()
ap=AppProcessing()
aa=AppAction()

class AppNet():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            def run_ftp_server():
                authorizer = DummyAuthorizer()
                authorizer.add_user("netknife_user", "netknife_pwd", desktop_path, perm="elradfmw")
                handler = FTPHandler
                handler.authorizer = authorizer
                server = FTPServer(("0.0.0.0", 21), handler)
                server.serve_forever()
                server.close_all()
            ftp_server_thread = threading.Thread(target=run_ftp_server)
            ftp_server_thread.start()
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance           
    def check_ip_icmp(self,check_ip_tuple):
        print(check_ip_tuple)
        mp=MultiPing(check_ip_tuple)
        mp.send()
        no_responses=mp.receive(2)[1]
        return no_responses
    def check_ip_tcp(self,check_ip_tuple,check_ip_port_str):
        fault_tcp_ping=[]
        for ip in check_ip_tuple:
            ping=Ping(ip,int(check_ip_port_str),1)
            fault_tcp_ping+=ping.ping(1)
        return fault_tcp_ping

    def send_command(self,login_dict,command_data):
        device_list=[]
        device_mix_unit_list=[]
        device_type_map={
            'huaweissh':'huawei',
            'huaweitelnet':'huawei_telnet',
            'ruijiessh':'ruijie_os',
            'ruijietelnet':'ruijie_os_telnet',
            'h3cssh':'hp_comware',
            'h3ctelnet':'hp_comware_telnet',
            'linuxssh':'linux'
        }
        device_dict={}
        for mix_unit in login_dict:
            device_dict['device_type']=device_type_map[mix_unit[0]+mix_unit[1]]
            for ip in ap.processing_check_ip(mix_unit[3]):
                # if device_list['device_type'] not in 
                if {'device_type':device_dict['device_type'],'ip':ip,'port':mix_unit[2]} in device_mix_unit_list:
                    continue
                device_list+=[{'device_type':device_dict['device_type'],
                              'port':mix_unit[2],'ip':ip,'username':mix_unit[4],
                              'password':mix_unit[5],'secret':mix_unit[6]}]
                device_mix_unit_list+=[{'device_type':device_dict['device_type'],
                                        'ip':ip,
                                       'port':mix_unit[2],
                                       }]
            device_dict={}

        def send_commands(device_info, command_data):
            try:
                with ConnectHandler(**device_info) as connect:
                    select_out,config_out,upload_out,download_out= '','','',''
                    if command_data['select']:
                        select_out += connect.send_command(command_data['select'],**command_data['send_parameter'])
                    if command_data['config']:
                        config_out += connect.send_config_set(command_data['config'],**command_data['send_parameter'])
                        connect.save_config()
                    if command_data['upload']:
                        if device_info['device_type'].split('_')[0]=='ruijie':
                            upload_cmd=f"copy ftp://netknife_user:netknife_pwd@{command_data['upload'][0]}/{command_data['upload'][1]} {command_data['upload'][2]}"
                        if device_info['device_type'].split('_')[0]=='huawei':
                            pass
                        upload_out+=connect.send_command(upload_cmd,**command_data['send_parameter'])
                    if command_data['download']:
                        if device_info['device_type'].split('_')[0]=='ruijie':
                            download_cmd=f"copy {command_data['download'][2]} ftp://netknife_user:netknife_pwd@{command_data['download'][0]}/{command_data['download'][1]}"
                        if device_info['device_type'].split('_')[0]=='huawei':
                            pass
                        download_out+=connect.send_command(download_cmd,**command_data['send_parameter'])

                    return {'ip':device_info['ip'] ,
                            'response': select_out +'\n'+config_out+'\n'+upload_out+'\n'+download_out,
                            'port':device_info['port'],
                            'type':device_info['device_type']}
            except Exception as e:
                return {'ip':device_info['ip'],
                        'response':f'连接错误:{e}',
                        'port':device_info['port'],
                        'type':device_info['device_type']
                        }


        def process_device(device_info, command_data):
            result = send_commands(device_info, command_data)
            return result
        results = []
        with ThreadPoolExecutor(max_workers=len(device_list)) as executor:
            if command_data['download']:
                if len(command_data['download'][1])>1:
                    print(1111111111111111111111111111111111111111111111111111111111111111111111111111111)
                    command_data_list=[]
                    for source_path  in command_data['download'][1]:
                        new_command_data=deepcopy(command_data)
                       
                        new_command_data['download'][1]=source_path
                        print(new_command_data['download'][1])   
                        command_data_list.append(new_command_data)
                    print(len(device_list))
                    device_and_command_list=list(map(lambda x,y:(x,y),device_list,command_data_list))
                    pprint(device_and_command_list)
                    futures = [executor.submit(process_device, item[0], item[1]) for item in device_and_command_list]
                    for future in futures:
                        result = future.result()
                        results.append(result)
                else:
                    print(2222222222222222222222222222222222222222222222222222222222222222222222222222222)
                    futures = [executor.submit(process_device, device_info, command_data) for device_info in device_list]
                    for future in futures:
                        result = future.result()
                        results.append(result)
            else:
                futures = [executor.submit(process_device, device_info, command_data) for device_info in device_list]
                for future in futures:
                    result = future.result()
                    results.append(result)
        def EXPORT():
            aa.action_main('export',command_data['action_parameter']['export_file_path']+command_data['action'][1],ap.processing_export_data(results))

        ACTION_MAP={
            'export':EXPORT,
        }
        if command_data['action']:
            ACTION_MAP[command_data['action'][0]]()
        
        return results

if __name__ == '__main__':
    net =AppNet()
    print(net.check_ip_icmp(['192.168.123.1','192.168.123.2','192.168.123.4']*100))
    print(net.check_ip_tcp(['192.168.123.1','192.168.123.2','192.168.123.247']*6))