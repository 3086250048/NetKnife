from textfsm import TextFSM
from itertools import chain
import os,re
from ordered_set import OrderedSet
from copy import deepcopy
from pprint import pprint


class AppProcessing():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance 
    def __init__(self):
        self.__path=os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.__path)
        self.__file={'check_ip':'processing_check_ip',
                     'effect':'processing_effect_command',
                     'command':'processing_command'}
        from storage import AppStorage
        self.__storage=AppStorage()        
    @classmethod
    def oprate_dict(cls,file,value):
        temp=TextFSM(open(file))
        return temp.ParseTextToDicts(value)
    
    @classmethod
    def oprate_list(cls,file,value):
        temp=TextFSM(open(file))
        return temp.ParseText(value)
    
    def processing_check_ip(self,check_ip):
        if not self.__path == self.__path+'/textfsm/data':
            os.chdir(self.__path+'/textfsm/data')
        address_dict=AppProcessing.oprate_dict(self.__file['check_ip'],check_ip)[0]
        if address_dict['Aend'] == '':address_dict['Aend']=address_dict['Astart']
        if address_dict['Bend'] == '':address_dict['Bend']=address_dict['Bstart']
        if address_dict['Cend'] == '':address_dict['Cend']=address_dict['Cstart']
        if address_dict['Dend'] == '':address_dict['Dend']=address_dict['Dstart']
        if address_dict['Astep'] =='':address_dict['Astep'] = '1'
        if address_dict['Bstep'] =='':address_dict['Bstep'] = '1'
        if address_dict['Cstep'] =='':address_dict['Cstep'] = '1'
        if address_dict['Dstep'] =='':address_dict['Dstep'] = '1'
        if int(address_dict['Aend'])-int(address_dict['Astart']) <0:return False
        if int(address_dict['Bend'])-int(address_dict['Bstart']) <0:return False
        if int(address_dict['Cend'])-int(address_dict['Cstart']) <0:return False
        if int(address_dict['Dend'])-int(address_dict['Dstart']) <0:return False
        address_list=[]
        for a in range(int(address_dict['Astart']),int(address_dict['Aend'])+1):
            for b in range(int(address_dict['Bstart']),int(address_dict['Bend'])+1):
                for c in range(int(address_dict['Cstart']),int(address_dict['Cend'])+1):
                    for d in range(int(address_dict['Dstart']),int(address_dict['Dend'])+1):
                        if not a % int(address_dict['Astep'])==0:continue
                        if not b % int(address_dict['Bstep'])==0:continue
                        if not c % int(address_dict['Cstep'])==0:continue
                        if not d % int(address_dict['Dstep'])==0:continue
                        address_list+=[f'{a}.{b}.{c}.{d}']

        result=''
        single_address_list=list(chain(list(address_dict['BeforeAddress'])[0:-1],list(address_dict['AfterAddress'])))
        for v in single_address_list+[',']:
            if '0'<= v <='9' or v=='.':
                result+=v
            if v==',':
                address_list+=[result]
                result=''
        return tuple([ v for v in address_list if v!=''])

    def processing_project_unit_data(self,project_unit_data):
        result=[]
        return_result=[]
        for i in project_unit_data:
            for j in i:
                for k in j:
                    result+=[k]
            return_result+=[[v for v in OrderedSet(result) if v!='']]
            result=[]  
        return return_result
                
    def processing_effect_command(self,command_data):
        input_data = command_data['command']
        where_dict={}
        if command_data['mode'] =='project':
            where_pattern = r"(?<=where\s)(.*?)(?=\sset|\sselect|\saction|\supload|\sdownload|$)"
            where_match = re.search(where_pattern,input_data)
            if where_match:
                where_key_value_list=where_match.group(1).split(',')
                for item in where_key_value_list:
                    if item !='':
                        _kv=item.split('=')
                        if _kv[0]=='project':continue
                        if len(_kv)<=1:continue
                        if _kv[0]=='ip':
                            where_dict['ip_expression']=_kv[1]
                        else:
                            where_dict[_kv[0]]=_kv[1]
            
                where_dict['project']=command_data['base_effect_range']
            else:
                where_dict['project']=command_data['base_effect_range']  
        else:
            where_dict['project']=command_data['base_effect_range']    
            where_dict['area']=command_data['extra_effect_range'][3]
            where_dict['protocol']=command_data['extra_effect_range'][4]
            where_dict['port']=command_data['extra_effect_range'][5]
            where_dict['ip_expression']=command_data['extra_effect_range'][9]     

        result={}
        _full_connect_lis=[]
        _effect_connect_lis=[]
        for i in self.__storage.get_effect_ip_expression_list({'project':command_data['base_effect_range']}):
            _full_connect_lis+=list(self.processing_check_ip(i))
        for i in self.__storage.get_effect_ip_expression_list(where_dict):
            _effect_connect_lis+=list(self.processing_check_ip(i))
        result['effect_connect_percent']=round(len(_effect_connect_lis)/len(_full_connect_lis)*100,1)
        return result

    def processing_effect_login_data(self,command_data):
        input_data = command_data['command']
        where_dict={}
        if command_data['mode']=='project':
            where_pattern = r"(?<=where\s)(.*?)(?=\sset|\sselect|\saction|\supload|\sdownload|$)"
            where_match = re.search(where_pattern,input_data)
            if where_match:
                where_key_value_list=where_match.group(1).split(',')
                for item in where_key_value_list:
                    if item !='':
                        _kv=item.split('=')
                        if _kv[0]=='project':continue
                        if len(_kv)<=1:continue
                        if _kv[0]=='ip':
                            where_dict['ip_expression']=_kv[1]
                        else:
                            where_dict[_kv[0]]=_kv[1]
            
                where_dict['project']=command_data['base_effect_range']
                # print(where_dict)
                return self.__storage.get_full_login_list(where_dict)
            else:
                where_dict['project']=command_data['base_effect_range']
                # print(where_dict)
                return self.__storage.get_full_login_list(where_dict)
        else:
            where_dict['project']=command_data['base_effect_range']
            where_dict['area']=command_data['mixunit'][3]
            where_dict['protocol']=command_data['mixunit'][4]
            where_dict['port']=command_data['mixunit'][5]
            where_dict['ip_expression']=command_data['mixunit'][9]
            return self.__storage.get_full_login_list(where_dict)
        
    def processing_command_data(self,command_data):

        input_data = command_data['command']
        select_pattern = r"(?<=select\s)(.*?)(?=\swhere|\sset|\saction|\supload|\sdownload|delete|$)"
        config_pattern = r"(?<=set\s)(.*?)(?=\swhere|\sselect|\saction|\supload|\sdownload|delete|$)"
        action_pattern = r"(?<=action\s)(.*?)(?=\swhere|\sselect|\sset|\supload|\sdownload|delete|$)"
        upload_pattern = r"(?<=upload\s)(.*?)(?=\swhere|\sselect|\sset|\saction|\sdownload|delete|$)"
        download_pattern = r"(?<=download\s)(.*?)(?=\swhere|\sselect|\sset|\saction|\supload|delete|$)"
        delete_pattern = r"(?<=delete\s)(.*?)(?=\swhere|\sselect|\sset|\saction|\supload|download|$)"

        select_match = re.search(select_pattern, input_data)
        config_match = re.search(config_pattern, input_data)
        action_match = re.search(action_pattern, input_data)
        upload_match = re.search(upload_pattern,input_data)
        download_match = re.search(download_pattern,input_data)
        delete_match= re.search(delete_pattern,input_data)

        command_dict={}
        
        if delete_match:
            command_dict['delete']=delete_match.group(1)
        else:
            command_dict['delete']=None

        if select_match:
            command_dict['select']=select_match.group(1)
        else:
            command_dict['select']=None

        if config_match:
            _lis=config_match.group(1).split(',')
            command_dict['config']=_lis
        else:
            command_dict['config']=None

        if upload_match:
            _lis=upload_match.group(1).split(',')
            command_dict['upload']=_lis
        else:
            command_dict['upload']=None

        if download_match:
            _lis=download_match.group(1).split(',')
            pattern = r"\[.+\]"
            matches = re.search(pattern,_lis[1])
            if matches:
                _tup=matches.span()
                _lis2=matches.group(0).split('[')
                _lis3=_lis2[1].split(']')
                _lis4=_lis3[0].split('-')
                _lis5=[  f'{_lis[1][:_tup[0]]}{i}{_lis[1][_tup[1]:]}'  for i in range(int(_lis4[0]),int(_lis4[1])+1)]
                command_dict['download']=_lis
                command_dict['download'][1]=_lis5
            else:
                command_dict['download']=_lis
        else:
            command_dict['download']=None

        if action_match:
            command_dict['action']=action_match.group(1).split(' ')
        else:
            command_dict['action']=None
        
        if command_data['send_parameter']:
            read_timeout=command_data['send_parameter']['read_timeout']
            command_data['send_parameter']['read_timeout']=float(read_timeout)
            command_dict['send_parameter']=command_data['send_parameter']
        
        if command_data['path_parameter']:
            command_dict['path_parameter']=command_data['path_parameter']
        return command_dict

    def processing_command_history_where_dict(self,where_dict):
        _where_dict={}
        if where_dict['mode']=='project':   
            _where_dict['area']='None'
            _where_dict['project']=where_dict['project']
           
        else:
            _where_dict['area']=where_dict['area']
            _where_dict['project']=where_dict['project']
            _where_dict['protocol']=where_dict['protocol']
            _where_dict['port']=where_dict['port']
            _where_dict['ip_expression']=where_dict['ip_expression']
        if 'id' in where_dict:
             _where_dict['id']=where_dict['id']
        if 'search' in where_dict:
            _lis=where_dict['search'].split('|')
            __lis=[ v.strip(' ')  for v in _lis]
            _where_dict['command']=__lis[0]
            _where_dict['date_time']=__lis[1]
        if 'command' in where_dict :
            _where_dict['command']=where_dict['command']
        if 'date_time' in where_dict:
            _where_dict['date_time']=where_dict['date_time']
        return _where_dict

    def processing_command_history_result(self,result):
        _result=[]
        for v in result:
            _result.append([v[0],v[1],v[2]])  
        __result=[{'value':v} for v in _result ]
        return __result

class NetProcessing():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance 
    def get_device_and_command_list(self,command_data,device_list):
        command_data_list=[]
        for source_path  in command_data['download'][1]:
            new_command_data=deepcopy(command_data)
            new_command_data['download'][1]=source_path  
            command_data_list.append(new_command_data)
        return list(map(lambda x,y:(x,y),device_list,command_data_list))
    def get_device_list(self,login_dict,DEVICE_TYPE_MAP):
        ap=AppProcessing()
        device_list, device_mix_unit_list,device_dict=[],[],{}
        for mix_unit in login_dict:
            device_dict['device_type']=DEVICE_TYPE_MAP[mix_unit[0]+mix_unit[1]]
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
        return device_list
    def get_export_data(self,export_data):
        _lis=[v['response'] for v in export_data]
        return ''.join(_lis)

class StorageProcessing():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance 
    def get_add_parameter_list(self,add_parameter_list):
        _add_parameter_list=[]
        for v in add_parameter_list:
            if v=='default':
                _add_parameter_list.append(os.path.join(os.path.expanduser("~"), "Desktop")+'\\')
            else:
                _add_parameter_list.append(v)
        return _add_parameter_list
    def processing_netknife_file(self,data):
        code=data['code']
        file_data_config={}
        file_data_config['name'] = re.search(r'name\s*:\s*([^:\n]+)', code).group(1).replace(" ","")
        file_data_config['priority'] = re.search(r'priority\s*:\s*(\d+)', code).group(1).replace(" ","")

        def get_inner_str(flag_str):
            search_start = code.find(flag_str)
            if search_start != -1:
                search_start += len(flag_str)
                search_end = search_start
                brace_count = 1
                while brace_count > 0 and search_end < len(code):
                    if code[search_end] == "{":
                        brace_count += 1
                    elif code[search_end] == "}":
                        brace_count -= 1
                    search_end += 1
                search_str = code[search_start:search_end-1].strip()
            return search_str
        def inner_parse(inner_str):
            inner_dict = {}
            lines = inner_str.strip().split("\n")
            current_key = None
            current_value = ""
            for line in lines:
                line = line.strip()
                if line.endswith("{"):
                    current_key = line[:-1].strip()
                    current_value = ""
                elif line == "}":
                    key=current_key.replace(":", "")
                    inner_dict[key] = current_value
                    current_key = None
                    current_value = ""
                elif current_key is not None:
                    current_value += line + "\n"
            return inner_dict
        
        file_data_translation={}
        if 'translation:{' in code:
            for k,v in inner_parse(get_inner_str('translation:{')).items():
                _v=v.split('\n')
                before_lis=[]
                after_lis=[]
                import_lis=[]
                _before_lis=[]
                _after_lis=[]
                for v in [ v.strip() for v in _v if v !='' ]:
                    if len(v.split('=>')) <=1:
                        import_lis.append(v.split('=>')[0])
                    else:
                        before_lis.append(v.split('=>')[0])
                        after_lis.append(v.split('=>')[1])
                for v in after_lis:
                    if '$' in v:
                        lis=[]
                        for v in v.split('$'):
                            lis.append(v.strip())
                        _after_lis.append(lis)
                    else:
                        _after_lis.append(v.strip())
                for v in before_lis:
                    if '$' in v:
                        lis=[]
                        for v in v.split('$'):
                            lis.append(v.strip())
                        _before_lis.append(lis)
                    else:
                        _before_lis.append(v.strip())
                
                file_data_translation[k]={'before_lis':_before_lis,'after_lis':_after_lis,'import_lis':import_lis}
        file_data_jinja2={}
        if 'jinja2:{' in code:
            for k,v in inner_parse(get_inner_str('jinja2:{')).items():
                _v=[ v.strip() for v in  v.split('\n') if v !='' ]
                lis=[]
                cmd_lis=[]
                flag=False
                for v in _v:
                    if v.strip()[0] == '$' :
                        lis.append(v[1:].strip())
                        flag=True
                        continue
                    if flag and v.strip()[-1]!='$':
                        lis.append(v.strip())
                        continue
                    if v.strip()[-1]== '$':
                        lis.append(v[:-1].strip())
                        cmd_lis.append(lis)
                        lis=[]
                        flag=False
                        continue
                    if v.strip()[0] != '$' and v.strip()[-1]!='$' and not flag:
                        cmd_lis.append(v)
                
                file_data_jinja2[k]=cmd_lis
        file_data_excute=[]
        if 'excute:{' in code:
            a=get_inner_str('excute:{')
            file_data_excute=[ v.strip() for v in a.split('\n') if v !='']
        netknife_file_data={}
        if file_data_config:
            netknife_file_data['config']=file_data_config
        if file_data_translation:
            netknife_file_data['translation']=file_data_translation
        if file_data_jinja2:
            netknife_file_data['jinja2']=file_data_jinja2
        if file_data_excute:
            netknife_file_data['excute']=file_data_excute
        return netknife_file_data

       

        
if __name__ == '__main__':
    ap=AppProcessing()
    # lis=[[('Myproject', '默认区域', 'telnet', '23', 'admin', 'admin@123', '', '100.100.100.100')], [('默认项目', '默认区域', 'telnet', '23', 'admin', '11', '', '192.168.123.1'), ('默认项目', '默认区域', 'telnet', '23', 'admin', 'admin@123', '', '2.1.1.1')], [('默认项目1', '默认区域', 'telnet', '23', 'admin', 'admin@123', '', '1.1.1.2'), ('默认项目1', '默认区域', 'telnet', '23', 'admin', 'admin@123', '', '1.1.1.3')], [('默认项目11', '默认区域', 'telnet', '23', '1', '1', '', '2.2.2.2')], [('默认项目2', '默认区域', 'telnet', '23', 'admin', 'admin@123', '', '1.1.1.2')], [('默认项目3', '默认区域', 'telnet', '23', 'admin', 'admin@123', '', '1.1.1.2')], [('默认项目4', '默认区域', 'telnet', '23', 'admin', 'admin@123', '', '1.1.1.2'), ('默认项目4', '默认区域', 'telnet', '23', 'admin', 'admin@123', '', '1.1.1.3')]]
    # ap.processing_effect_command({'base_effect_range':'Myproject','command':'where area=默认区域,protocol=ssh,port=1000,ip=172.168.1.1'})
    # print(ap.processing_command_data({'base_effect_range':'默认项目','command':''}))
    _lis=[{'ip':'1.1.1.1' ,
        'response':'aaaaaaaaaa' +'\n'+'bbbbbb',
        'port':'65532',
        'type':'ruijie_telnet_os'
        }]
    print(ap.processing_export_data(_lis))


   

