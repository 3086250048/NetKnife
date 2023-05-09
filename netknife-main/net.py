from concurrent.futures import ThreadPoolExecutor,as_completed
from multiping import MultiPing
from tcping import Ping
from netmiko import ConnectHandler
from paramiko import SSHClient
import telnetlib

from storage import AppStorage
from processing import AppProcessing
from processing import NetProcessing
from action import AppAction
from pprint import pprint
from jinja2 import Template
from itertools import chain


storage=AppStorage()
ap=AppProcessing()
aa=AppAction()
np=NetProcessing()




class Base_Excute_Mode():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'): 
            cls._instance=super().__new__(cls)
        return cls._instance      
    def __init__(
            self,
            parameter:dict,
            login_info:list,
            commands:list,
            excute_handler:object,
            excute_list_handler:object=None,
            max_workers:int=1,
            ) -> None:
        self._parameter_dict=parameter
        self._login_dict_list=login_info
        self._command_list=commands
        self._max_workers=max_workers
        self._excute_list=[]
        self._excute_handler=excute_handler
        if not excute_list_handler:
            if len(commands)<len(login_info):
                copy_num=len(login_info)
                self._excute_list=list(zip(login_info,commands*copy_num))
            elif len(login_info) < len(commands):
                copy_num=len(commands)
                self._excute_list=list(zip(login_info*copy_num,commands))
            else:
                self._excute_list=list(zip(login_info,commands))
        else:
            excute_list_handler(self._excute_list,login_info,commands)
    def excute(self):
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = [executor.submit(self._excute_handler, item[0], item[1]) for item in self._excute_list]
            for future in as_completed(futures):
                yield future.result()
                
    # def send_commands(login_info, commands):
    #     try:
    #         with ConnectHandler(**device_info) as connect:
    #             return SEND_COMMANDS_MAP[device_info['device_type'].split('_')[0]](connect,device_info,command_data)
    #     except Exception as e:
    #         return {'ip':device_info['ip'],
    #                 'response':f'连接错误:{e}',
    #                 'port':device_info['port'],
    #                 'type':device_info['device_type']
    #                 }
 

class Telnetlib_Excute_Mode():
    pass
class Paramiko_Excute_Mode():
    pass
class Netmiko_Excute_Mode():
    pass



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

    
    # def send_commands(connect,device_info,excute_type,command):
    #     if excute_type=='send_command':
    #     response=connect.send_command_timing(,**command_data['send_parameter'])
    #     return {'ip':device_info['ip'] ,
    #             'response':response ,
    #             'port':device_info['port'],
    #             'type':device_info['device_type']}


    # def send_command(self,login_dict,command_data):
        
        

       
       

     
        DEVICE_LIST=np.get_device_list(login_dict,device_type)
       

  
        
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
            # 将管理设备中的设备类型转为netmiko中的设备类型
            DEVICE_TYPE_MAP={}
            DEVICE_TYPE_MAP['huaweissh']='huawei'
            DEVICE_TYPE_MAP['huaweitelnet']='huawei_telnet'
            DEVICE_TYPE_MAP['ruijiessh']='ruijie_os'
            DEVICE_TYPE_MAP['ruijietelnet']='ruijie_os_telnet'
            DEVICE_TYPE_MAP['h3cssh']='hp_comware'
            DEVICE_TYPE_MAP['h3ctelnet']='hp_comware_telnet'
            DEVICE_TYPE_MAP['linuxssh']='linux'
            ####################################################################

            ori_cmd_lis=[v[0] for v in cmd_login_list]
            all_cmd_login_info_lis=[v[1:][0] for v in cmd_login_list]
            all_full_login_info_lis=[]
            for each_login_info in all_cmd_login_info_lis:
                all_full_login_info_lis.append(np.get_device_list(each_login_info,DEVICE_TYPE_MAP))
            all_cmd_device_type_lis=[]
            for device_info in all_full_login_info_lis:
                all_cmd_device_type_lis.append([v['device_type'] for v in device_info ] )
            where_dict={'FILE_NAME':file_name}
           
        #  待提取到processing############################################################
            use_file_name_list=[]
            def chain_translation_result(where_dict):
                translation_result=[]
                if where_dict['FILE_NAME'] in use_file_name_list:
                    return ['REPEAT']
                else:
                    use_file_name_list.append(where_dict['FILE_NAME'])
                for v in storage.get_database_data('TRANSLATION',['TYPE','BEFORE_CMD','AFTER_CMD'],where_dict):
                    if '.' in  v[1]:
                        translation_result+=chain_translation_result({'FILE_NAME':v[1].split('.')[0],'TYPE':v[1].split('.')[1]})
                    else:
                        translation_result+=[v]
                return translation_result
            chain_translation_result_list=chain_translation_result(where_dict)
            if  'REPEAT' in chain_translation_result_list:
                 return 'TRANSLATION_REPEAT_IMPORT'
            print('==========================translation_result========================')
            print(chain_translation_result_list)
        ##################################################################################
           
        #    获取发送命令的参数
            send_parameter_result=storage.get_database_data('CONFIG',['PARAMETER_KEY','PARAMETER_VALUE'],
            {'FILE_NAME':file_name,'PARAMETER_CLASS':'send'})
            print(send_parameter_result)
           
            send_parameter_dict={}
            for v in send_parameter_result:
                print(type(eval(v[1])))
                send_parameter_dict[v[0]]=eval(v[1])
            print(send_parameter_dict)
        # 将login_info中的设备类型字符串转换为translation的设备类型
            MATCH_TYPE_MAP={}
            MATCH_TYPE_MAP['huawei_telnet']='huawei'
            MATCH_TYPE_MAP['huawei']='huawei'
            MATCH_TYPE_MAP['ruijie_os']='ruijie'
            MATCH_TYPE_MAP['ruijie_os_telnet']='ruijie'
            MATCH_TYPE_MAP['hp_comware']='h3c'
            MATCH_TYPE_MAP['hp_comware_telnet']='h3c'
            
            # 获取每个设备的登录列表和每个设备需要执行的命令
            all_device_type_cmd=[]
            for index,cmds in enumerate(ori_cmd_lis):
                each_device_type_cmd=[]
                for each_device_type in all_cmd_device_type_lis[index]: 
                    _cmds=[v for v in cmds]
                    for _index,cmd in enumerate(_cmds): 
                        for each_translation_result in chain_translation_result_list:   
                            if MATCH_TYPE_MAP[each_device_type]==each_translation_result[0] and cmd.replace(" ", "") == each_translation_result[1].replace(" ", ""):
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
                jinja2_cmds_lis=[]
                for cmds in cmds_lis:
                    jinja2_str='\n'.join(cmds)
                    template=Template(jinja2_str)
                    result=template.render(excute_parameter_dict_lis[index])
                    jinja2_cmds_lis.append([ v for v in result.split('\n') if v])
                jinja2_all_cmds_lis.append(jinja2_cmds_lis)
            
            
            ALL_CMDS_LIS=jinja2_all_cmds_lis
            ALL_LOGIN_INFO_LIS=all_full_login_info_lis
            pprint(ALL_CMDS_LIS)
            pprint(ALL_LOGIN_INFO_LIS)
            # ###########################################################################################

            # 获取每个设备执行的函数列表
            multipilication_lis=[len(v) for v in ALL_CMDS_LIS]
            full_excute_fun_name_lis=[]
            for index,fun_name in enumerate(excute_fun_name_lis):
                full_excute_fun_name_lis+=[fun_name]*multipilication_lis[index]
            ############################################################################################

            ########向每个设备发送命令
            def send_commands_handler(connect,commands):
                out=''
                out += connect.send_config_set(commands,**send_parameter_dict)
                out += connect.save_config()
                return out
        
            def send_commands(device_info, commands,excute_fun_name):
                try:
                    with ConnectHandler(**device_info) as connect:
                        connect.send_config_set()
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
            CHAIN_ALL_LOGIN_LIS=list(chain.from_iterable(ALL_LOGIN_INFO_LIS))
            CHAIN_ALL_CMDS_LIS=list(chain.from_iterable(ALL_CMDS_LIS))

            with ThreadPoolExecutor(max_workers=len(CHAIN_ALL_LOGIN_LIS)) as executor:
                futures = []
                for index,device_info in  enumerate(CHAIN_ALL_LOGIN_LIS):
                    futures.append(executor.submit(process_device, device_info, CHAIN_ALL_CMDS_LIS[index],full_excute_fun_name_lis[index]))
                for future in futures:
                    result = future.result()
                    ALL_RESULTS.append(result)
                return ALL_RESULTS
            ##############################################################################################
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    net =AppNet()
    print(net.check_ip_icmp(['192.168.123.1','192.168.123.2','192.168.123.4']*100))
    print(net.check_ip_tcp(['192.168.123.1','192.168.123.2','192.168.123.247']*6))