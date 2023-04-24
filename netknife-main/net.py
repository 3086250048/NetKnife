from concurrent.futures import ThreadPoolExecutor
from multiping import MultiPing
from tcping import Ping
from netmiko import ConnectHandler

from storage import AppStorage
from processing import AppProcessing
from processing import NetProcessing
from action import AppAction
from pprint import pprint
from jinja2 import Template

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

        print('login_dict')
        print(login_dict)
        print('command_data')
        print(command_data)
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
            print('command============================================================================')
            print(command_data)
            {'delete': None, 'select': 'dir', 'config': None, 'upload': None, 'download': None, 'action': None,
            'send_parameter': {'strip_prompt': True, 'strip_command': False, 'read_timeout': 17.0}, 
            'path_parameter': {'txt_export_path': 'C:\\Users\\30862\\Desktop\\', 'ftp_root_path': 'C:\\Users\\30862\\Desktop\\',
             'ftp_upload_path': 'C:\\Users\\30862\\Desktop\\', 'ftp_download_path': 'C:\\Users\\30862\\Desktop\\'}}
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

    def netknife_send_command(self,cmd_login_list,file_name,excute_fun_name_lis):
        try:
            DEVICE_TYPE_MAP={}
            DEVICE_TYPE_MAP['huaweissh']='huawei'
            DEVICE_TYPE_MAP['huaweitelnet']='huawei_telnet'
            DEVICE_TYPE_MAP['ruijiessh']='ruijie_os'
            DEVICE_TYPE_MAP['ruijietelnet']='ruijie_os_telnet'
            DEVICE_TYPE_MAP['h3cssh']='hp_comware'
            DEVICE_TYPE_MAP['h3ctelnet']='hp_comware_telnet'
            DEVICE_TYPE_MAP['linuxssh']='linux'

            ori_cmd_lis=[v[0] for v in cmd_login_list]
            print('=======================ORI_CMD_LIS=================================')
            print(ori_cmd_lis)

            all_cmd_login_info_lis=[v[1:][0] for v in cmd_login_list]
        
            all_full_login_info_lis=[]
            for each_login_info in all_cmd_login_info_lis:
                all_full_login_info_lis.append(np.get_device_list(each_login_info,DEVICE_TYPE_MAP))
            
            all_cmd_device_type_lis=[]
            for device_info in all_full_login_info_lis:
                all_cmd_device_type_lis.append([v['device_type'] for v in device_info ] )

            where_dict={'FILE_NAME':file_name}
            translation_result= storage.get_database_data('TRANSLATION',['TYPE','BEFORE_CMD','AFTER_CMD'],where_dict)
            print('==========================================TRANSLATION_RESULT===============================')
            MATCH_TYPE_MAP={}
            MATCH_TYPE_MAP['huawei_telnet']='huawei'
            MATCH_TYPE_MAP['huawei']='huawei'
            MATCH_TYPE_MAP['ruijie_os']='ruijie'
            MATCH_TYPE_MAP['ruijie_os_telnet']='ruijie'
            MATCH_TYPE_MAP['hp_comware']='h3c'
            MATCH_TYPE_MAP['hp_comware_telnet']='h3c'
            
            all_device_type_cmd=[]
            print(ori_cmd_lis)
            for index,cmds in enumerate(ori_cmd_lis):
                each_device_type_cmd=[]
                for each_device_type in all_cmd_device_type_lis[index]: 
                    _cmds=[v for v in cmds]
                    for _index,cmd in enumerate(_cmds): 
                        for each_translation_result in translation_result:
                            print(each_translation_result)
                            # print(each_device_type)
                            # print(cmd)
                            print('======================================TYPE=======================================')
                            print(MATCH_TYPE_MAP[each_device_type])
                            print('======================================CMD=======================================')
                            print(cmd)
                            if MATCH_TYPE_MAP[each_device_type]==each_translation_result[0] and cmd.replace(" ", "") == each_translation_result[1].replace(" ", ""):
                                print('1111111111111111111111111111111111111111111111111111111111111111111111111111111111')
                                _cmds[_index]=each_translation_result[2] 
                    each_device_type_cmd.append(_cmds)
                all_device_type_cmd.append(each_device_type_cmd)

            _all_device_type_cmd_lis=[]
            for index,device_type_cmd in enumerate(all_device_type_cmd):
                device_type_cmd_lis=[]
                for _index,cmds in enumerate(device_type_cmd):
                    _lis='$'.join(cmds).split('$')
                    device_type_cmd_lis.append(_lis)
                _all_device_type_cmd_lis.append(device_type_cmd_lis)
            print(_all_device_type_cmd_lis)

            excute_parameter_result=storage.get_database_data('EXCUTE',['PARAMETER'],where_dict,'ORDER BY SORT_ID')
            excute_parameter_lis=[ v[0].replace(" ","") for v in excute_parameter_result]

            _excute_parameter_lis=[ v.split('$') for v in excute_parameter_lis ]
        
            excute_parameter_dict_lis=[]
            for parameter_lis in _excute_parameter_lis:
                if parameter_lis[0]=='None':
                    parameter_dict={}
                else:
                    parameter_dict={ v.split('=')[0]:eval(v.split('=')[1]) for v in parameter_lis}
                excute_parameter_dict_lis.append(parameter_dict)           
        
            jinja2_all_cmds_lis=[]
            for index,cmds_lis in  enumerate(_all_device_type_cmd_lis):
                print('==================CMDS_LIST=====================')
                print(cmds_lis)
                jinja2_cmds_lis=[]
                for cmds in cmds_lis:
                    jinja2_str='\n'.join(cmds)
                    print('==================JINJA2_STR=====================')
                    print(jinja2_str)
                    template=Template(jinja2_str)
                    result=template.render(excute_parameter_dict_lis[index])
                    print('==================RESULT=====================')
                    print(result)
                    jinja2_cmds_lis.append([ v for v in result.split('\n') if v])
                jinja2_all_cmds_lis.append(jinja2_cmds_lis)
            
            
            ALL_CMDS_LIS=jinja2_all_cmds_lis
            ALL_LOGIN_INFO_LIS=all_full_login_info_lis
            pprint(ALL_CMDS_LIS)
            pprint(ALL_LOGIN_INFO_LIS)
            
            def send_commands_handler(connect,commands):
                out=''
                out += connect.send_config_set(commands)
                connect.save_config()
                return out
        
            def send_commands(device_info, commands,excute_fun_name):
                try:
                    with ConnectHandler(**device_info) as connect:
                        result=send_commands_handler(connect,commands)
                        return {
                            'ip':device_info['ip'],
                            'response':result,
                            'port':device_info['port'],
                            'type':device_info['device_type'],
                            'fun_name':excute_fun_name

                        }
                except Exception as e:
                    return {'ip':device_info['ip'],
                            'response':f'连接错误:{e}',
                            'port':device_info['port'],
                            'type':device_info['device_type'],
                            'fun_name':excute_fun_name
                            }
            
            def process_device(device_info, commands,excute_fun_name):
                result = send_commands(device_info, commands,excute_fun_name)
                return result
            
            ALL_RESULTS=[]
            for index,each_device_lis in enumerate(ALL_LOGIN_INFO_LIS):
                results = []
                with ThreadPoolExecutor(max_workers=len(each_device_lis)) as executor:
                    futures = []
                    for _index,device_info in  enumerate(each_device_lis):
                        futures.append(executor.submit(process_device, device_info, ALL_CMDS_LIS[index][_index],excute_fun_name_lis[index]))
                    for future in futures:
                        result = future.result()
                        results.append(result)
                ALL_RESULTS.append(results)
            return ALL_RESULTS
        except Exception as e:
            print(e)
            return False

if __name__ == '__main__':
    net =AppNet()
    print(net.check_ip_icmp(['192.168.123.1','192.168.123.2','192.168.123.4']*100))
    print(net.check_ip_tcp(['192.168.123.1','192.168.123.2','192.168.123.247']*6))