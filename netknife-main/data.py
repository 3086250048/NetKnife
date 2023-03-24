from processing import AppProcessing

ap=AppProcessing()

class AppInfo():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance        
    def __init__(self) -> None:
        self.__login_dict=None
        self.__check_ip_tuple=None
        self.__check_ip_port_str=None
        self.__check_quads_dict=None
        self.__where_dict=None
        self.__update_data_dict=None
        self.__effect_login_dict=None
        self.__command_str=None
    @property
    def login_dict(self):
        return self.__login_dict
    @property
    def check_ip_tuple(self):
        return self.__check_ip_tuple
    @property
    def check_ip_port_str(self):
        return self.__check_ip_port_str
    @property
    def check_quads_dict(self):
        return self.__check_quads_dict
    @property
    def where_dict(self):
        return self.__where_dict
    @property
    def update_data_dict(self):
        return self.__update_data_dict
    @property
    def effect_login_dict(self):
        return self.__effect_login_dict
    @property
    def command_str(self):
        return self.__command_str


    @login_dict.setter
    def login_dict(self,login_dict):
        self.__login_dict=login_dict
    @check_ip_tuple.setter
    def check_ip_tuple(self,ip_check_dict):
        self.__check_ip_tuple=ap.processing_check_ip(ip_check_dict['ip_expression'])
    @check_ip_port_str.setter
    def check_ip_port_str(self,ip_check_dict):
        self.__check_ip_port_str=ip_check_dict['port']
    @check_quads_dict.setter
    def check_quads_dict(self,check_quads_dict):
        self.__check_quads_dict=check_quads_dict
    @where_dict.setter
    def where_dict(self,where_dict):
        self.__where_dict=where_dict
    @update_data_dict.setter
    def update_data_dict(self,update_data_dict):
        self.__update_data_dict=update_data_dict
    @effect_login_dict.setter
    def effect_login_dict(self,effect_login_data):
        self.__effect_login_dict=ap.processing_effect_login_data(effect_login_data)
    @command_str.setter
    def command_str(self,command_data):
        self.__command_str=ap.processing_command_data(command_data)
  

if __name__ =='__main__':
    a1=AppInfo()
    a2=AppInfo()
    print(id(a1)==id(a2))