import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading
from storage import AppStorage
storage=AppStorage()

root_path = os.path.join(os.path.expanduser("~"), "Desktop") and storage.get_file_path_parameter()

def run_ftp_server(root_path=root_path):
    authorizer = DummyAuthorizer()
    authorizer.add_user("netknife_user", "netknife_pwd", root_path, perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()
    server.close_all()
ftp_server_thread = threading.Thread(target=run_ftp_server,args=(root_path,))
ftp_server_thread.start()
