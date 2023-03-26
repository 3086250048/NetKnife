from textfsm import TextFSM
from itertools import chain
import os,re
from ordered_set import OrderedSet
from storage import AppStorage

storage=AppStorage()


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
        # print(address_dict)
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
        # if not self.__path == self.__path+'/textfsm/data':
        #     os.chdir(self.__path+'/textfsm/data')
        # result={}
        # ex_effect_range=AppProcessing.oprate_dict(self.__file['effect'],command_data['command'])
        
        # if len(ex_effect_range)==0:
        #     full_effect_dict={'project':command_data['base_effect_range']}
        # else:
        #     ex_effect_range[0]['project']=command_data['base_effect_range']
        #     full_effect_dict=ex_effect_range[0]
        input_data = command_data['command']
        where_dict={}
        where_pattern = r"(?<=where\s)(.*?)(?=\sset|\sselect|\saction|$)"
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
                    
        result={}
        ap=AppProcessing()
        _full_connect_lis=[]
        _effect_connect_lis=[]
        for i in storage.get_effect_ip_expression_list({'project':command_data['base_effect_range']}):
            _full_connect_lis+=list(ap.processing_check_ip(i))
        for i in storage.get_effect_ip_expression_list(where_dict):
            _effect_connect_lis+=list(ap.processing_check_ip(i))
  
        result['effect_connect_percent']=int(len(_effect_connect_lis)/len(_full_connect_lis)*100)
        return result

    def processing_effect_login_data(self,command_data):
        # if not self.__path == self.__path+'/textfsm/data':
        #     os.chdir(self.__path+'/textfsm/data')
        # ex_effect_range=AppProcessing.oprate_dict(self.__file['effect'],effect_login_dict['command'])
        # if len(ex_effect_range)==0:
        #     full_effect_dict={'project':effect_login_dict['base_effect_range']}
        # else:
        #     ex_effect_range[0]['project']=effect_login_dict['base_effect_range']
        #     full_effect_dict=ex_effect_range[0]

        input_data = command_data['command']
        where_dict={}
        where_pattern = r"(?<=where\s)(.*?)(?=\sconfig|\sselect|\saction|$)"
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
            return storage.get_full_login_list(where_dict)
        else:
            where_dict['project']=command_data['base_effect_range']
            # print(where_dict)
            return storage.get_full_login_list(where_dict)
                     
    def processing_command_data(self,command_data):
        # if not self.__path == self.__path+'/textfsm/data':
        #     os.chdir(self.__path+'/textfsm/data')
        input_data = command_data['command']
        select_pattern = r"(?<=select\s)(.*?)(?=\swhere|\sset|\saction|\supload|$)"
        config_pattern = r"(?<=set\s)(.*?)(?=\swhere|\sselect|\saction|\supload|$)"
        action_pattern = r"(?<=action\s)(.*?)(?=\swhere|\sselect|\sset|\supload|$)"
        upload_pattern = r"(?<=upload\s)(.*?)(?=\swhere|\sselect|\saction|\sset|$)"
        # download_pattern = r"(?<=upload\s)(.*?)(?=\swhere|\sselect|\saction|\supload|\sset$)"

        select_match = re.search(select_pattern, input_data)
        config_match = re.search(config_pattern, input_data)
        action_match = re.search(action_pattern, input_data)
        upload_match = re.search(upload_pattern,input_data)
        # download_match = re.search(download_pattern,input_data)

        command_dict={}
        
        if select_match:
            command_dict['select']=select_match.group(1)
        else:
            command_dict['select']=None

        if config_match:
            _lis=config_match.group(1).split(',')
            command_dict['config']=_lis
        else:
            command_dict['config']=None

        if action_match:
            command_dict['action']=action_match.group(1).split(' ')
        else:
            command_dict['action']=None

        if upload_match:
            command_dict['upload']=upload_match.group(1).split(' ')
        else:
            command_dict['upload']=None
        

        if command_data['send_parameter']:
            for k,v in command_data['send_parameter'].items():
                if isinstance(v,int) and not isinstance(v,bool):
                    command_data['send_parameter'][k]=float(command_data['send_parameter'][k])
            command_dict['send_parameter']=command_data['send_parameter']
        
        if command_data['action_parameter']:
            command_dict['action_parameter']=command_data['action_parameter']

        print(command_dict)

        return command_dict

    def processing_export_data(self,export_data):
        _lis=[v['response'] for v in export_data]
        return ''.join(_lis)
    
    
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



   

