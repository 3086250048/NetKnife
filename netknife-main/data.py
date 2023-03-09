class AppInfo():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance        
    def __init__(self) -> None:
        self.__login_dict=None
        self.__check_ip_dict=None
    @property
    def login_dict(self):
        return self.__login_dict
    @property
    def check_ip_dict(self):
        return self.__check_ip_dict
    @login_dict.setter
    def login_dict(self,login_dict):
        self.__login_dict=login_dict
        return self.__login_dict
    @check_ip_dict.setter
    def check_ip_dict(self,ip_check_dict):
        self.__check_ip_dict=ip_check_dict
        return self.check_ip_dict
if __name__ =='__main__':
    a1=AppInfo()
    a2=AppInfo()
    print(id(a1)==id(a2))