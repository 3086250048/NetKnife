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
                        if a % int(address_dict['Astep'])==0:
                            if b % int(address_dict['Bstep'])==0:
                                if c % int(address_dict['Cstep'])==0:
                                    if d % int(address_dict['Dstep'])==0:
                                        address_list+=[f'{a}.{b}.{c}.{d}']
                                    else:
                                        continue
                            else:
                                continue       
                        else:
                            continue
        return tuple(address_list)

if __name__ == '__main__':
    ap=AppProcessing()
    print(ap.processing_check_ip('192.168.123.1-10'))
   

