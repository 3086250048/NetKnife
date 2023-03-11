from multiping import MultiPing
from tcping import Ping

from netmiko import ConnectHandler

from storage import AppStorage

storage=AppStorage()

class AppNet():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance     
    def __init__(self) :
        pass
        # self.__login_list=[{'device_type':item[1],
        #                     'host':item[7],
        #                     'username':item[5],
        #                     'password':item[6],
        #                     'port':item[4],
        #                     'secret':item[8]
        #                     }
        #                     for item in  storage.select_login_info()]
    def check_ip_icmp(self,check_ip_tuple):
        mp=MultiPing(check_ip_tuple)
        mp.send()
        no_responses=mp.receive(2)[1]
        # fault_ip=[]
        # for ip in  check_ip_tuple:
        #     if subprocess.run(['ping','-c', '1','-w','1','-i','0.002',ip],stdout=subprocess.PIPE).returncode:
        #         fault_ip+=[ip]
        
        # print(fault_ip)
        return no_responses
    def check_ip_tcp(self,check_ip_tuple):
        fault_tcp_ping=[]
        for ip in check_ip_tuple:
            ping=Ping(ip,22,1)
            fault_tcp_ping+=ping.ping(1)
        return fault_tcp_ping


if __name__ == '__main__':
    net =AppNet()
    print(net.check_ip_icmp(['192.168.123.1','192.168.123.2','192.168.123.4']*100))
    print(net.check_ip_tcp(['192.168.123.1','192.168.123.2','192.168.123.247']*6))