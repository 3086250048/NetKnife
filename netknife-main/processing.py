from textfsm import TextFSM
import os

class AppProcessing():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance 
    def __init__(self):
        self.__path=os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.__path)
        self.__file={'processing_check_ip':'processing_check_ip'}

    @classmethod
    def oprate_dict(cls,file,value):
        temp=TextFSM(open(file))
        return temp.ParseTextToDicts(value)
    
    @classmethod
    def oprate_list(cls,file,value):
        temp=TextFSM(open(file))
        return temp.ParseText(value)

    def processing_check_ip(self,check_ip):
        print(check_ip)
        if not self.__path == self.__path+'/textfsm/data':
            os.chdir(self.__path+'/textfsm/data')
        address_dict=AppProcessing.oprate_dict(self.__file['processing_check_ip'],check_ip)[0]
        if address_dict['Aend'] == '':address_dict['Aend']=address_dict['Astart']
        if address_dict['Bend'] == '':address_dict['Bend']=address_dict['Bstart']
        if address_dict['Cend'] == '':address_dict['Cend']=address_dict['Cstart']
        if address_dict['Dend'] == '':address_dict['Dend']=address_dict['Dstart']
        if address_dict['Astep'] =='':address_dict['Astep'] = '1'
        if address_dict['Bstep'] =='':address_dict['Bstep'] = '1'
        if address_dict['Cstep'] =='':address_dict['Cstep'] = '1'
        if address_dict['Dstep'] =='':address_dict['Dstep'] = '1'
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
        return tuple(address_list)
    
    # def processing_check_update_where(self,check_update_where_dict):
    #     {'project': '', 'class': '', 'area': '', 'protocol': '', 'port': '', 'username': '', 'password': '', 'secret': '', 'ip_expression': ''}
    #     check_update_where_list=[v for v in check_update_where_dict.values() ]
    #     def callback(v):
    #         if v=='':
    #             return True
    #         return v
    #     check_update_where_tuple=tuple(map(callback,check_update_where_list ))
    #     return check_update_where_tuple
        

if __name__ == '__main__':
    ap=AppProcessing()
    ap.processing_check_update_where({'a':1,'b':'2','c':''})
   

