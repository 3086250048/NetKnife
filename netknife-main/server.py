import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading
from storage import AppStorage
storage=AppStorage()

class APPserver():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'): 
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance  
    def __init__(self):
         self.server=None
# root_path = os.path.join(os.path.expanduser("~"), "Desktop") and storage.get_file_path_parameter()
    def start_ftp_server(self,path_dict):
        def run_ftp_server(root_path):
            authorizer = DummyAuthorizer()
            authorizer.add_user("netknife_user", "netknife_pwd", root_path, perm="elradfmw")
            handler = FTPHandler
            handler.authorizer = authorizer
            self.server = FTPServer(("0.0.0.0", 21), handler)
            self.server.serve_forever()
        try:
            root_path=path_dict['ftp_root_path']
            print('------------------------------------------------------------------------')
            print(root_path)
            ftp_server_thread = threading.Thread(target=run_ftp_server,args=(root_path,))
            ftp_server_thread.start()
            return 'START_FTPSERVER_SUCCESS'
        except Exception as e:
            print(e)
            return 'START_FTPSERVE_FAULT'
    def stop_ftp_serve(self):
        if self.server is not None:
            self.server.close_all()
            self.server = None
            return 'STOP_FTPSERVER_SUCCESS'
        else:
            return 'FTP_SERVER_NOT_RUNNING'