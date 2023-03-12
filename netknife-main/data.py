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
        self.__check_project_str=None
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
    def check_project_str(self):
        return self.__check_project_str

    @login_dict.setter
    def login_dict(self,login_dict):
        self.__login_dict=login_dict
    @check_ip_tuple.setter
    def check_ip_tuple(self,ip_check_dict):
        self.__check_ip_tuple=ap.processing_check_ip(ip_check_dict['ip_expression'])
    @check_ip_port_str.setter
    def check_ip_port_str(self,ip_check_dict):
        self.__check_ip_port_str=ip_check_dict['port']
    @check_project_str.setter
    def check_project_str(self,project_dict):
        self.__check_project_str=project_dict['project']
    
if __name__ =='__main__':
    a1=AppInfo()
    a2=AppInfo()
    print(id(a1)==id(a2))