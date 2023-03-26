from concurrent.futures import ThreadPoolExecutor


from multiping import MultiPing
from tcping import Ping

from netmiko import ConnectHandler,file_transfer

from storage import AppStorage
from processing import AppProcessing
from action import AppAction

storage=AppStorage()
ap=AppProcessing()
aa=AppAction()

class AppNet():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance     
    def __init__(self) :
        pass
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
                    select_out,config_out,upload_out,download_out = '','','',''
                    if command_data['select']:
                        select_out += connect.send_command(command_data['select'],**command_data['send_parameter'])
                         
                    if command_data['config']:
                        config_out += connect.send_config_set(command_data['config'],**command_data['send_parameter'])
                        connect.save_config()
                    '''
                    upload 命令支持设备类型
                    arista_eos
                    arista_eos_ssh
                    ciena_saos
                    ciena_saos_ssh
                    cisco_asa
                    cisco_asa_ssh
                    cisco_ios
                    cisco_ios_ssh
                    cisco_nxos
                    cisco_nxos_ssh
                    cisco_xe
                    cisco_xe_ssh
                    cisco_xr
                    cisco_xr_ssh
                    dell_os10
                    dell_os10_ssh
                    extreme_exos
                    extreme_exos_ssh
                    juniper_junos
                    juniper_junos_ssh
                    linux
                    linux_ssh
                    mikrotik_routeros
                    mikrotik_routeros_ssh
                    nokia_sros
                    nokia_sros_ssh
                    '''
                    if command_data['upload']:
                        upload_out+=file_transfer(connect,
                        source_file=command_data['action_parameter']['upload_src_file_path']+command_data['upload'][0],
                        dest_file=command_data['action_parameter']['upload_des_file_path']+command_data['upload'][1],
                        file_system=command_data['action_parameter']['file_system'],
                        direction="put",
                        overwrite_file=command_data['action_parameter']['overwrite_file']
                        )

                    return {'ip':device_info['ip'] ,
                            'response': select_out +'\n'+config_out,
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