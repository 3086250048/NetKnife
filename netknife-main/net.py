from concurrent.futures import ThreadPoolExecutor
from multiping import MultiPing
from tcping import Ping
from netmiko import ConnectHandler

from storage import AppStorage
from processing import AppProcessing
from processing import NetProcessing
from action import AppAction


storage=AppStorage()
ap=AppProcessing()
aa=AppAction()
np=NetProcessing()

class AppNet():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'): 
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance           
    def check_ip_icmp(self,check_ip_tuple):
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
        SEND_COMMANDS_MAP,DEVICE_TYPE_MAP={},{}

        DEVICE_TYPE_MAP['huaweissh']='huawei'
        DEVICE_TYPE_MAP['huaweitelnet']='huawei_telnet'
        DEVICE_TYPE_MAP['ruijiessh']='ruijie_os'
        DEVICE_TYPE_MAP['ruijietelnet']='ruijie_os_telnet'
        DEVICE_TYPE_MAP['h3cssh']='hp_comware'
        DEVICE_TYPE_MAP['h3ctelnet']='hp_comware_telnet'
        DEVICE_TYPE_MAP['linuxssh']='linux'

        def h3c_send_commands(connect,device_info,command_data):
            select_out,config_out,upload_out,download_out= '','','',''
            if command_data['delete']:
                _cmd=f"delete {command_data['delete']}"
                select_out += connect.send_command_timing(_cmd,**command_data['send_parameter'])
                select_out += connect.send_command_timing('Y',**command_data['send_parameter'])
                select_out += connect.send_command_timing('reset recycle-bin ',**command_data['send_parameter'])
                select_out += connect.send_command_timing('Y',**command_data['send_parameter'])
            if command_data['upload']:
                upload_cmd_list=[f"ftp {command_data['upload'][0]}",f"netknife_user",f"netknife_pwd",f"get  {command_data['path_parameter']['ftp_upload_path']}{command_data['upload'][1]} {command_data['upload'][2]}"]
                upload_out+=connect.send_command_timing(upload_cmd_list[0],**command_data['send_parameter'])
                upload_out+=connect.send_command_timing(upload_cmd_list[1],**command_data['send_parameter'])
                upload_out+=connect.send_command_timing(upload_cmd_list[2],**command_data['send_parameter'])
                upload_out+=connect.send_command_timing(upload_cmd_list[3],**command_data['send_parameter'])
                upload_out+=connect.send_command_timing('quit',**command_data['send_parameter'])
            if command_data['download']:
                download_cmd_list=[f"ftp {command_data['download'][0]}",f"netknife_user",f"netknife_pwd",f"put {command_data['download'][2]} {command_data['path_parameter']['ftp_download_path']}{command_data['download'][1]}"]
                download_out+=connect.send_command_timing(download_cmd_list[0],**command_data['send_parameter'])
                download_out+=connect.send_command_timing(download_cmd_list[1],**command_data['send_parameter'])
                download_out+=connect.send_command_timing(download_cmd_list[2],**command_data['send_parameter'])
                download_out+=connect.send_command_timing(download_cmd_list[3],**command_data['send_parameter'])
                download_out+=connect.send_command_timing('quit',**command_data['send_parameter'])
            if command_data['select']:
                select_out += connect.send_command_timing(command_data['select'],**command_data['send_parameter'])
            if command_data['config']:
                config_out += connect.send_config_set(command_data['config'],**command_data['send_parameter'])
                connect.save_config()
            return {'ip':device_info['ip'] ,
                            'response': select_out +'\n'+config_out+'\n'+upload_out+'\n'+download_out,
                            'port':device_info['port'],
                            'type':device_info['device_type']}
        def huawei_send_commands(connect,device_info,command_data):
            select_out,config_out,upload_out,download_out= '','','',''
            if command_data['delete']:
                _cmd=f"delete {command_data['delete']}"
                select_out += connect.send_command_timing(_cmd,**command_data['send_parameter'])
                select_out += connect.send_command_timing('Y',**command_data['send_parameter'])
                select_out += connect.send_command_timing('reset recycle-bin ',**command_data['send_parameter'])
                select_out += connect.send_command_timing('Y',**command_data['send_parameter'])
            if command_data['select']:
                select_out += connect.send_command(command_data['select'],**command_data['send_parameter'])
            if command_data['config']:
                config_out += connect.send_config_set(command_data['config'],**command_data['send_parameter'])
                connect.save_config()
            if command_data['upload']:
                print(command_data['upload'][1])
                upload_cmd_list=[f"ftp {command_data['upload'][0]}",f"netknife_user",f"netknife_pwd",f"get  {command_data['path_parameter']['ftp_upload_path']}{command_data['upload'][1]} {command_data['upload'][2]}"]
                upload_out+=connect.send_command_timing(upload_cmd_list[0],**command_data['send_parameter'])
                upload_out+=connect.send_command_timing(upload_cmd_list[1],**command_data['send_parameter'])
                upload_out+=connect.send_command_timing(upload_cmd_list[2],**command_data['send_parameter'])
                upload_out+=connect.send_command_timing(upload_cmd_list[3],**command_data['send_parameter'])
                upload_out+=connect.send_command_timing('quit',**command_data['send_parameter'])
            if command_data['download']:
                download_cmd_list=[f"ftp {command_data['download'][0]}",f"netknife_user",f"netknife_pwd",f"put {command_data['download'][2]} {command_data['path_parameter']['ftp_download_path']}{command_data['download'][1]}"]
                download_out+=connect.send_command_timing(download_cmd_list[0],**command_data['send_parameter'])
                download_out+=connect.send_command_timing(download_cmd_list[1],**command_data['send_parameter'])
                download_out+=connect.send_command_timing(download_cmd_list[2],**command_data['send_parameter'])   
                download_out+=connect.send_command_timing(download_cmd_list[3],**command_data['send_parameter'])
                download_out+=connect.send_command_timing('quit',**command_data['send_parameter'])
            return {'ip':device_info['ip'] ,
                            'response': select_out +'\n'+config_out+'\n'+upload_out+'\n'+download_out,
                            'port':device_info['port'],
                            'type':device_info['device_type']}
        def ruijie_send_commands(connect,device_info,command_data):
            select_out,config_out,upload_out,download_out= '','','',''
            if command_data['select']:
                select_out += connect.send_command_timing(command_data['select'],**command_data['send_parameter'])
            if command_data['config']:
                config_out += connect.send_config_set(command_data['config'],**command_data['send_parameter'])
                connect.save_config()
            if command_data['upload']:
                upload_cmd=f"copy ftp://netknife_user:netknife_pwd@{command_data['upload'][0]}/{command_data['upload'][1]} {command_data['upload'][2]}"
                upload_out+=connect.send_command_timing(upload_cmd,**command_data['send_parameter'])
            if command_data['download']:
                
                download_cmd=f"copy {command_data['download'][2]} ftp://netknife_user:netknife_pwd@{command_data['download'][0]}/{command_data['download'][1]}"
                download_out+=connect.send_command_timing(download_cmd,**command_data['send_parameter'])
            
            return {
                    'ip':device_info['ip'] ,
                    'response': select_out +'\n'+config_out+'\n'+upload_out+'\n'+download_out,
                    'port':device_info['port'],
                    'type':device_info['device_type']
                    }

        SEND_COMMANDS_MAP['hp']=h3c_send_commands
        SEND_COMMANDS_MAP['huawei']=huawei_send_commands
        SEND_COMMANDS_MAP['ruijie']=ruijie_send_commands


        DEVICE_LIST=np.get_device_list(login_dict,DEVICE_TYPE_MAP)
       

        def send_commands(device_info, command_data):
            try:
                with ConnectHandler(**device_info) as connect:
                    return SEND_COMMANDS_MAP[device_info['device_type'].split('_')[0]](connect,device_info,command_data)
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
        with ThreadPoolExecutor(max_workers=len(DEVICE_LIST)) as executor:
            if command_data['download'] :
                if len(command_data['download'][1])>1:
                    device_and_command_list=np.get_device_and_command_list(command_data,DEVICE_LIST)
                    futures = [executor.submit(process_device, item[0], item[1]) for item in device_and_command_list]
                    for future in futures:
                        result = future.result()
                        results.append(result)
                else:
                    futures = [executor.submit(process_device, device_info, command_data) for device_info in DEVICE_LIST]
                    for future in futures:
                        result = future.result()
                        results.append(result)
            else:
                futures = [executor.submit(process_device, device_info, command_data) for device_info in DEVICE_LIST]
                for future in futures:
                    result = future.result()
                    results.append(result)

        if command_data['action'] and results:
            print('action了')
            aa.action_class_map(command_data['action'][0],command_data['path_parameter']['txt_export_path']+command_data['action'][1],np.get_export_data(results))
            
        return results

if __name__ == '__main__':
    net =AppNet()
    print(net.check_ip_icmp(['192.168.123.1','192.168.123.2','192.168.123.4']*100))
    print(net.check_ip_tcp(['192.168.123.1','192.168.123.2','192.168.123.247']*6))