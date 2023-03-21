import asyncio

from multiping import MultiPing
from tcping import Ping

from netmiko import ConnectHandler

from storage import AppStorage
from processing import AppProcessing

storage=AppStorage()
ap=AppProcessing()

class AppNet():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance     
    def __init__(self) :
        pass
    def check_ip_icmp(self,check_ip_tuple):
        print(check_ip_tuple)
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
        device_list=[]
        device_type_map={
            'huaweissh':'huawei',
            'huaweitelnet':'huawei_telnet',
            'ruijiessh':'ruijie_os',
            'ruijietelnet':'ruijie_os_telnet',
            'h3cssh':'hp_comware',
            'h3ctelnet':'hp_comware_telnet',
            'linuxssh':'linux'
        }
        device_dict={}
        for mix_unit in login_dict:
            device_dict['device_type']=device_type_map[mix_unit[0]+mix_unit[1]]
            for ip in ap.processing_check_ip(mix_unit[3]):
                device_list+=[{'device_type':device_dict['device_type'],
                              'port':mix_unit[2],'ip':ip,'username':mix_unit[4],
                              'password':mix_unit[5],'secret':mix_unit[6]}]
            device_dict={}
        async def netmiko_send_command(device,command_data):
            try:
                with ConnectHandler(**device) as connect:
                    out=await connect.send_command(command_data)
                    return out
            except:
                    return device['ip']
        async def main():
            task_list=[]
            for device_info in device_list:
                task_list+=[ asyncio.create_task(netmiko_send_command(device_info,'display ip int brife'))]
            done,pending=await asyncio.wait(task_list,None)
            return done
        return asyncio.run(main())


if __name__ == '__main__':
    net =AppNet()
    print(net.check_ip_icmp(['192.168.123.1','192.168.123.2','192.168.123.4']*100))
    print(net.check_ip_tcp(['192.168.123.1','192.168.123.2','192.168.123.247']*6))