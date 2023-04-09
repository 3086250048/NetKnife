import sqlite3,os,uuid
from processing import StorageProcessing
import json
sp=StorageProcessing()

class AppStorage():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance       
    def __init__(self) -> None:
        self.__path=os.path.dirname(os.path.abspath(__file__))+'/appdata.db'
        self.__add_login_info_sql='''INSERT INTO LOGININFO (ID,PROJECT,CLASS,AREA,PROTOCOL,PORT,USERNAME,PASSWORD,SECRET,IP_EXPRESSION)
                            VALUES (?,?,?,?,?,?,?,?,?,?);'''
        self.__add_filepath_info_sql='''INSERT INTO FILEPATH (ID,PROJECT,AREA,TXT_EXPORT_PATH,FTP_ROOT_PATH,FTP_UPLOAD_PATH,FTP_DOWNLOAD_PATH)
                            VALUES (?,?,?,?,?,?,?);'''
        self.__add_sendcommand_parameter_info_sql='''INSERT INTO SENDCOMMAND_PARAMETER (ID,PROJECT,AREA,DEVICE_TITLE_ABLE,COMMAND_ABLE,READ_TIMEOUT)
                            VALUES (?,?,?,?,?,?);'''
        self.__get_project_list_sql='''SELECT PROJECT FROM LOGININFO GROUP BY PROJECT ;'''
        self.__add_suid_sql='''INSERT INTO SUID (FIRST_SUID) VALUES (?);'''
        self.__add_command_history_sql='''INSERT INTO COMMAND_HISTORY (ID,PROJECT,AREA,PROTOCOL,PORT,IP_EXPRESSION,COMMAND,COMMAND_RESPONSE,DATE_TIME) VALUES (?,?,?,?,?,?,?,?,?);'''
        #初始化创建数据库和表
        if not os.path.exists(self.__path):
            try:
                con=sqlite3.connect(self.__path)
                cur=con.cursor()
                cur.execute(
                    '''CREATE TABLE  LOGININFO(
                ID             TEXT    PRIMARY KEY NOT NULL,
                PROJECT        TEXT    NOT NULL,
                CLASS          TEXT    NOT NULL,
                AREA           TEXT    NOT NULL,
                PROTOCOL       TEXT    NOT NULL,
                PORT           TEXT    NOT NULL,
                USERNAME       TEXT    NOT NULL,
                PASSWORD     TEXT      NOT NULL,
                SECRET        TEXT     NOT NULL,
                IP_EXPRESSION   TEXT    NOT NULL,
                UNIQUE(PROJECT,AREA,PORT,PROTOCOL,IP_EXPRESSION)
                );'''
                )
                print('LOGININFO')
                cur.execute(
                    '''CREATE TABLE FILEPATH (
                ID             TEXT    PRIMARY KEY NOT NULL,
                PROJECT        TEXT    NOT NULL,
                AREA           TEXT    NOT NULL,
                TXT_EXPORT_PATH TEXT   NOT NULL,
                FTP_ROOT_PATH   TEXT    NOT NULL,
                FTP_UPLOAD_PATH TEXT     NOT NULL,
                FTP_DOWNLOAD_PATH   TEXT NOT NULL,
                UNIQUE(PROJECT,AREA)
                );'''
                )
                print('FILEPATH')
                cur.execute(
                    '''CREATE TABLE SENDCOMMAND_PARAMETER (
                ID             TEXT    PRIMARY KEY NOT NULL,
                PROJECT        TEXT    NOT NULL,
                AREA           TEXT    NOT NULL,
                DEVICE_TITLE_ABLE  TEXT    NOT NULL,
                COMMAND_ABLE    TEXT    NOT NULL,
                READ_TIMEOUT    TEXT    NOT NULL,
                UNIQUE(PROJECT,AREA)
                );'''
                )
                print('SENDCOMMAND_PARAMETER')
                cur.execute(
                    '''CREATE TABLE COMMAND_HISTORY (
                ID             TEXT     PRIMARY KEY NOT NULL,
                PROJECT        TEXT     NOT NULL,
                AREA           TEXT     NOT NULL,
                PROTOCOL       TEXT     NOT NULL,
                PORT           TEXT     NOT NULL,
                IP_EXPRESSION  TEXT     NOT NULL,
                COMMAND        TEXT     NOT NULL,
                COMMAND_RESPONSE TEXT   NOT NULL,
                DATE_TIME   TEXT    NOT NULL);'''
                )
                print('COMMAND_HISTORY')
                cur.execute(
                    '''CREATE TABLE SUID (FIRST_SUID   TEXT    PRIMARY KEY NOT NULL);'''
                )
                print('SUID')
                uid =str(uuid.uuid4())
                suid=''.join(uid.split('-'))
                cur.execute(self.__add_login_info_sql,[suid]*10)
                print('INSERT-1')
                cur.execute(self.__add_filepath_info_sql,[suid]*7)
                print('INSERT-2')
                cur.execute(self.__add_sendcommand_parameter_info_sql,[suid]*6)
                print('INSERT-3')
                cur.execute(self.__add_command_history_sql,[suid]*9)
                print('INSERT-4')
                cur.execute(self.__add_suid_sql,[suid])
                print('INSERT-5')
                con.commit()
            except sqlite3.Error as e:
                print(e)
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

    #返回一个sql语句,要求附带数据
    #例子:
    #init_sql=select * from logininfo | first_sql=where | loop_sql=and
    #data_dict={'project':'a',area:'',protocol:'b'}
    #得到 select * from logininfo where project=a and protocol=b
    @classmethod
    def dynamic_sql_return (cls,init_sql,first_sql,loop_sql,data_dict):
        sql=''
        flag=True
        for k,v in data_dict.items():
            if v=='':
                continue
            if flag: 
                sql+=f'{init_sql} {first_sql} {k}=\'{v}\''
                flag=False
            else:
                sql+=f'{loop_sql} {k}=\'{v}\''
        return sql
    
    #迭代出一个sql语句
    #例子:
    #init_sql=select * from logininfo | first_sql=where | field_sql=project
    #data_list=['a','b','c']
    #迭代三次得到
    #1.select * from logininfo where project=a
    #2.select * from logininfo where project=b
    #3.select * from logininfo where project=c
    @classmethod
    def dynamic_sql_yield (cls,init_sql,first_sql,field_sql,data_list):
        sql=''
        for v in data_list:
            sql+=f'{init_sql} {first_sql} {field_sql}=\'{v}\''
            yield sql
            sql=''

    #执行sql语句,data可以传入空字典{},call_back为执行sql语句之后的回调函数
    #返回:回调函数决定,发生异常返回False
    #传入:sql语句,sql数据{}(可为空),回调函数(决定返回数值)
    def oprate_sql(self,sql,data,call_back,*args):
        try:
            con=sqlite3.connect(self.__path,check_same_thread=False)
            cur=con.cursor()
            cur.execute(sql,data)
            return call_back(cur,con) 
        except sqlite3.Error as e:
            print(e)
            con.rollback()
            return False
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    #取任意数据库任意字段
    def get_database_data(self,database_name,field_list,where_dict={},other_command=''):
        def callback(cur,con):
            return cur.fetchall()
        field_str=','.join(field_list)
        if where_dict:
            where_sql=AppStorage.dynamic_sql_return('','WHERE','AND',where_dict)
        else:
            where_sql=''
        full_sql=f"SELECT {field_str} FROM {database_name} {where_sql} {other_command}"
        print('================================90909090909090')
        print(full_sql)
        return self.oprate_sql(full_sql,{},callback)
    #删除任意数据库数据
    def del_database_data(self,database_name,where_dict={}):
        def callback(cur,con):
            con.commit()
            return True
        if where_dict:
            where_sql=AppStorage.dynamic_sql_return('','WHERE','AND',where_dict)
        else:
            where_sql=''
        full_sql=f"DELETE FROM {database_name} {where_sql}"
        return self.oprate_sql(full_sql,{},callback)
    #获取任意数据库的条目数
    def get_database_data_count(self,database_name,where_dict={}):
        def callback(cur,con):
            return cur.fetchall()
        if where_dict:
            where_sql=AppStorage.dynamic_sql_return('','WHERE','AND',where_dict)
        else:
            where_sql=''
        full_sql=f"SELECT COUNT(*) FROM {database_name} {where_sql}"
        print('===================================full_sql')
        print(full_sql)
        result= self.oprate_sql(full_sql,{},callback)
        print(type(result[0][0]))
        if result[0][0]==0:
            return True
        else:
            return False
        


    #向数据库中插入数据
    #返回:布尔值
    #传入:{'projet':'',area:'',protocol:'',port:'',ip_expression:'',username:'',password:'',secret:''} 
    def add_login_info(self,login_dict)->bool:
        uid =str(uuid.uuid4())
        suid=''.join(uid.split('-'))
        value_list=list(login_dict.values())
        value_list.insert(0,suid)
        def callback(cur,con):
            con.commit()
            return True
        return self.oprate_sql(self.__add_login_info_sql,value_list,callback)

    #检查数据库中是否存在某个最小单元
    #返回:布尔值
    #传入:{'projet':'',area:'',protocol:'',port:'',ip_expression:''} 
    def check_quads(self,check_quads_dict)->bool:
        sql=AppStorage.dynamic_sql_return('SELECT * FROM LOGININFO','WHERE','AND',check_quads_dict)
        def callback(cur,con):
            result=cur.fetchall()
            if len(result)<=0:
                return True
            else:
                return False
        return self.oprate_sql(sql,check_quads_dict,callback)    
    
    #检查数据库中是否存在某条记录
    #返回:布尔值
    #传入:{'projet':'',area:'',protocol:'',port:''....} 
    def check_where(self,where_dict)->bool:
        def callback(cur,con):
            result=cur.fetchall()
            if len(result)<=0:
                return True
            return False
        return self.oprate_sql(AppStorage.dynamic_sql_return('SELECT * FROM LOGININFO','WHERE','AND',where_dict),where_dict,callback)
#给更新参数数据库用 
    def get_project_area_data(self):
        def callback(cur,con):
            return cur.fetchall()
        return self.oprate_sql('SELECT ID,PROJECT,AREA FROM LOGININFO;',{},callback)


#给delete 参数数据库用
    def get_project_area(self):
        def callback(cur,con):
            return cur.fetchall()
        return self.oprate_sql('SELECT PROJECT,AREA FROM LOGININFO;',{},callback)
#给更新 参数数据库用 
    def get_parameter_project_area_data(self):
        def callback(cur,con):
            return cur.fetchall()
        return self.oprate_sql('SELECT PROJECT,AREA FROM FILEPATH;',{},callback)
#给更新 参数数据库用 
    def get_filepath_parameter_value(self,where_dict):
        def callback(cur,con):
            return cur.fetchall()
        sql=AppStorage.dynamic_sql_return('SELECT TXT_EXPORT_PATH,FTP_ROOT_PATH,FTP_UPLOAD_PATH,FTP_DOWNLOAD_PATH FROM FILEPATH','WHERE','AND',where_dict)
        return self.oprate_sql(sql,{},callback)
#给更新 参数数据库用 
    def get_sendcommand_parameter_value(self,where_dict):
        def callback(cur,con):
            return cur.fetchall()
        sql=AppStorage.dynamic_sql_return('SELECT DEVICE_TITLE_ABLE,COMMAND_ABLE,READ_TIMEOUT FROM SENDCOMMAND_PARAMETER','WHERE','AND',where_dict)
        return self.oprate_sql(sql,{},callback)
    #更新数据库中某条记录
    #返回:布尔值
    #传入:
    #条件数据:{'projet':'',area:'',protocol:'',port:''....} 
    #更新数据:{'projet':'',area:'',protocol:'',port:''....}
    def update_data(self,where_dict,update_data_dict)->bool:
        def callback_after(cur,con):
            con.commit()
            return True
        where_sql=AppStorage.dynamic_sql_return('','where','and',where_dict)
        update_sql=AppStorage.dynamic_sql_return('update logininfo','set',',',update_data_dict)
        sql=update_sql+where_sql
        return self.oprate_sql(sql,{},callback_after)

    #删除数据库中某条记录
    #返回:布尔值
    #传入:{'projet':'',area:'',protocol:'',port:''....}
    def delete_data(self,where_dict) -> bool:
        def callback(cur,con):
            con.commit()
            return True
        delete_sql=AppStorage.dynamic_sql_return('DELETE FROM LOGININFO','WHERE','AND',where_dict)
        return self.oprate_sql(delete_sql,where_dict,callback)
    
    #得到数据库中以project为查询条件的最小单元列表
    #返回:[['projetc1','area1 、area2','protocol1 ; protocol2','port1 ; port2','ip_expression'],[...]]
    def get_project_unit_list(self) -> list:
        def callback(cur,con):
            return cur.fetchall()
        ['ensp', 'fb5377e75c6e48f0aef672a8c9c9a008']
        project_list=[ v[0] for v in self.oprate_sql(self.__get_project_list_sql,{},callback)]
        first_suid=self.oprate_sql('SELECT * FROM SUID',{},callback)[0][0]
        project_list.remove(first_suid)
        project_sql_gen=AppStorage.dynamic_sql_yield('select project,area,protocol,port,ip_expression from logininfo','where','project',project_list)
        lis=[]
        for _ in range(len(project_list)):
            project_sql=project_sql_gen.__next__()
            lis+=[self.oprate_sql(project_sql,{},callback)]
        dic={'project':'','area':'','protocol':'','port':'',"ip_expression":''}
        result=[]
        for i in lis:
            n=0
            for j in i:    
                if n!=0:
                    if j[0] not in dic['project']:
                        dic['project']+=j[0] 
                    if j[1] not in dic['area']:
                        dic['area']+=' 、'+j[1]
                    if j[2] not in  dic['protocol']:
                        dic['protocol']+='  ； '+j[2]
                    if j[3] not in  dic['port']:
                        dic['port']+='  ； '+j[3]
                    if j[4] not in dic['ip_expression']:
                        dic['ip_expression']+='  ； '+j[4]
                else:
                    if j[0] not in dic['project']:
                        dic['project']+=j[0]
                    if j[1] not in dic['area']:
                        dic['area']+=j[1]
                    if j[2] not in dic['protocol']:
                        dic['protocol']+=j[2]
                    if j[3] not in dic['port']:
                        dic['port']+=j[3]
                    if j[4] not in dic['ip_expression']:
                        dic['ip_expression']+=j[4]
                n+=1
            result+=[list(dic.values())]
            dic={'project':'','area':'','protocol':'','port':'',"ip_expression":''}
        return result
    
    #获取数据库中所有的项目名称
    #返回:[{'value':'project1'},{'value':'project2'},{'project3':'project3'}]
    def get_all_project_list(self)-> list:
        def callback(cur,con):
            return cur.fetchall()
        _lis= self.oprate_sql('SELECT DISTINCT project FROM LOGININFO;',{},callback)[1:]
        result= [ {'value':v[0]} for v in _lis]
        return result

    #获取数据库中满足某个查询条件时的ip_expression表达式。
    #返回:[1.1.1.1,192.168.1.1-100%2,....]
    #传入:{'project':'','area':'','protocol':'','port':'','ip_expression':'',....}
    def get_effect_ip_expression_list(self,effect_range_dict) -> list:
        effect_number_sql=AppStorage.dynamic_sql_return('SELECT IP_EXPRESSION FROM LOGININFO','WHERE','AND',effect_range_dict)
        def callback(cur,con):
            return cur.fetchall()
        result_lis=[ v[0] for v in self.oprate_sql(effect_number_sql,{},callback)]
        return result_lis
       
    #获取登录设备时需要的信息。
    #返回:{'class':'','protocol':'','port':'','ip_expression':'','username':‘’,'password':'','secret':''}
    #传入:{'project':'','area':'','protocol':'','port':'','ip_expression':'',.....}
    def get_full_login_list(self,effect_range_dict):
        effect_number_sql=AppStorage.dynamic_sql_return('SELECT CLASS,PROTOCOL,PORT,IP_EXPRESSION,USERNAME,PASSWORD,SECRET FROM LOGININFO','WHERE','AND',effect_range_dict)
        def callback(cur,con):
            return cur.fetchall()
        result=self.oprate_sql(effect_number_sql,{},callback)
        return result

    def select_count(self):
        def callback(cur,con):
            return cur.fetchall()
        result=self.oprate_sql('select count(*) from logininfo',{},callback)
        return result

# sendcommand 参数相关
    def get_sendcommand_parameter(self,select_parameter_dict):
        print(select_parameter_dict)
        def callback(cur,con):
            result=cur.fetchall()    
            if len(result)<=0:
               return 'None'
            else:
                return result
        _where_dict={}
        if select_parameter_dict['mode']=='project':
            _where_dict['area']='None'
            _where_dict['project']=select_parameter_dict['project']
        else:
            _where_dict['area']=select_parameter_dict['area']
            _where_dict['project']=select_parameter_dict['project']
        sql=AppStorage.dynamic_sql_return('select device_title_able,command_able,read_timeout from sendcommand_parameter','where','and',_where_dict)
        return self.oprate_sql(sql,{},callback)
         
    def add_sendcommand_parameter(self,add_parameter_dict):
        print(add_parameter_dict)
        uid =str(uuid.uuid4())
        suid=''.join(uid.split('-'))
        add_parameter_list=list(add_parameter_dict.values())
        add_parameter_list.insert(0,suid)
        def callback(cur,con):
            con.commit()
            return True
        return self.oprate_sql(self.__add_sendcommand_parameter_info_sql,add_parameter_list,callback)

    def change_sendcommand_parameter(self,data_dict):
        def callback(cur,con):
            con.commit()
            return True
        _where_dict={}
        if data_dict['where']['mode']=='project':
            _where_dict['area']='None'
            _where_dict['project']=data_dict['where']['project']
        else:
            _where_dict['area']=data_dict['where']['area']
            _where_dict['project']=data_dict['where']['project']
        where_sql=AppStorage.dynamic_sql_return('','where','and',_where_dict)
        update_sql=AppStorage.dynamic_sql_return('update sendcommand_parameter','set',',',data_dict['update'])
        sql=update_sql+where_sql
        print(sql)
        return self.oprate_sql(sql,{},callback)
    
    def delete_sendcommand_parameter(self,where_dict) -> bool:
        def callback(cur,con):
            con.commit()
            return True
        delete_sql=AppStorage.dynamic_sql_return('DELETE FROM sendcommand_parameter','WHERE','AND',where_dict)
        return self.oprate_sql(delete_sql,where_dict,callback)
# filepath 参数相关

    def get_filepath_parameter(self,select_parameter_dict):
        print(select_parameter_dict)
        def callback(cur,con):
            result=cur.fetchall()    
            if len(result)<=0:
                return 'None'
            else:
                return result
        _where_dict={}
        if select_parameter_dict['mode']=='project':
            _where_dict['area']='None'
            _where_dict['project']=select_parameter_dict['project']
        else:
            _where_dict['area']=select_parameter_dict['area']
            _where_dict['project']=select_parameter_dict['project']
        sql=AppStorage.dynamic_sql_return('select TXT_EXPORT_PATH,FTP_ROOT_PATH ,FTP_UPLOAD_PATH ,FTP_DOWNLOAD_PATH from filepath','where','and',_where_dict)
        return self.oprate_sql(sql,{},callback)
         
    def add_filepath_parameter(self,add_parameter_dict):
        uid =str(uuid.uuid4())
        suid=''.join(uid.split('-'))
        add_parameter_list=list(add_parameter_dict.values())
        add_parameter_list.insert(0,suid)
        _add_parameter_list=sp.get_add_parameter_list(add_parameter_list)
        def callback(cur,con):
            con.commit()
            return True
        return self.oprate_sql(self.__add_filepath_info_sql,_add_parameter_list,callback)

    def change_filepath_parameter(self,data_dict):
        def callback(cur,con):
            con.commit()
            return True
        _where_dict={}
        if data_dict['where']['mode']=='project':
            _where_dict['area']='None'
            _where_dict['project']=data_dict['where']['project']
        else:
            _where_dict['area']=data_dict['where']['area']
            _where_dict['project']=data_dict['where']['project']
        where_sql=AppStorage.dynamic_sql_return('','where','and',_where_dict)
        update_sql=AppStorage.dynamic_sql_return('update filepath','set',',',data_dict['update'])
        sql=update_sql+where_sql
        return self.oprate_sql(sql,{},callback)

    def delete_filepath_parameter(self,where_dict) -> bool:
        def callback(cur,con):
            con.commit()
            return True
        delete_sql=AppStorage.dynamic_sql_return('DELETE FROM FILEPATH','WHERE','AND',where_dict)
        return self.oprate_sql(delete_sql,where_dict,callback)

    # 参数数据库
    def update_parameter_database(self,dict):
        try:
            before_list=dict['before']
            after_list=dict['after']
            project_after_list = [ v[1] for v in after_list]
            project_area_after_list = [v[1:] for v in after_list]
            project_before_list=[ v[1] for v in before_list]
            update_base_area_list=[]

            add_base_area_list=[]
            add_base_area_file_parameter_list=[]
            add_base_area_send_parameter_list=[]

            add_none_area_list=[]

            for i in before_list:
                for j in after_list:
                    if i[0]==j[0] and i[1:]!=j[1:]:
                        if i[1:] not in project_area_after_list:
                            update_base_area_list.append([i[1:],j[1:]])
                        else:
                            add_base_area_list.append(j[1:])
                            add_base_area_file_parameter_list.append(self.get_filepath_parameter_value({
                                'project':i[1],
                                'area':i[2],
                                }))
                            add_base_area_send_parameter_list.append(self.get_sendcommand_parameter_value
                            ({
                                'project':i[1],
                                'area':i[2],
                                }))
                        if j[1] not in project_before_list:
                            add_none_area_list.append([j[1],'None'])
                            add_none_area_file_parameter_list=self.get_filepath_parameter({
                                'project':i[1],
                                'area':i[2],
                                'mode':'project'
                            })
                            add_none_area_send_parameter_list=self.get_sendcommand_parameter({
                                'project':i[1],
                                'area':i[2],
                                'mode':'project'
                            })
            delete_base_area_list=[ v[1:]  for v in before_list if v[1:] not in project_area_after_list]
            delete_none_area_list=[ [v[1],'None'] for v in before_list if v[1] not in project_after_list ]
            # 待增加add是原有项目的数据
            # add_none_area_list=[ [v[1],'None'] for v in after_list if v[1] not in project_before_list ]
            for e in update_base_area_list:
                self.change_filepath_parameter(
                    {
                        'where':{
                            'project':e[0][0],
                            'area':e[0][1],
                            'mode':'area'
                        },
                        'update':{
                            'project':e[1][0],
                            'area':e[1][1]
                        }
                    }
                )
                self.change_sendcommand_parameter(
                     {
                        'where':{
                            'project':e[0][0],
                            'area':e[0][1],
                            'mode':'area'
                        },
                        'update':{
                            'project':e[1][0],
                            'area':e[1][1]
                        }
                    }
                )
            for e in delete_base_area_list:
                self.delete_filepath_parameter({'project':e[0],'area':e[1]})
                self.delete_sendcommand_parameter({'project':e[0],'area':e[1]})
            for e in delete_none_area_list:
                self.delete_filepath_parameter({'project':e[0],'area':'None'})
                self.delete_sendcommand_parameter({'project':e[0],'area':'None'})
            for i,e in enumerate(add_base_area_list):
                self.add_filepath_parameter({
                    'project':e[0],
                    'area':e[1],
                    'txt_export_path':add_base_area_file_parameter_list[i][0][0],
                    'ftp_root_path':add_base_area_file_parameter_list[i][0][1],
                    'ftp_upload_path':add_base_area_file_parameter_list[i][0][2],
                    'ftp_download_path:':add_base_area_file_parameter_list[i][0][3],
                })
                self.add_sendcommand_parameter({
                    'project':e[0],
                    'area':e[1],
                    'device_title_able':add_base_area_send_parameter_list[i][0][0],
                    'command_able': add_base_area_send_parameter_list[i][0][1],
                    'read_timeout': add_base_area_send_parameter_list[i][0][2],
                })
            for e in add_none_area_list:
                [('C:\\Users\\30862\\Desktop\\', 'C:\\Users\\30862\\Desktop\\', 'C:\\Users\\30862\\Desktop\\', 'C:\\Users\\30862\\Desktop\\')]
                [('False', 'False', '10')]
                print('**********************************************************')
                print(add_none_area_file_parameter_list)
                print(add_none_area_send_parameter_list)
                self.add_filepath_parameter({
                    'project':e[0],
                    'area':e[1],
                    'txt_export_path':add_none_area_file_parameter_list[0][0],
                    'ftp_root_path':add_none_area_file_parameter_list[0][1],
                    'ftp_upload_path':add_none_area_file_parameter_list[0][2],
                    'ftp_download_path:':add_none_area_file_parameter_list[0][3],
                })
                self.add_sendcommand_parameter({
                    'project':e[0],
                    'area':e[1],
                    'device_title_able':add_none_area_send_parameter_list[0][0],
                    'command_able':add_none_area_send_parameter_list[0][1],
                    'read_timeout':add_none_area_send_parameter_list[0][2] 
                })
            
            return 'True'
        except Exception as e:
            return str(e)
    #mixunitpage的搜索数据
    def get_mixunit_data(self,where_dict):
        def callback(cur,con):
            return cur.fetchall()
        _where_dict={}
        if 'search' in  where_dict.keys():
            search_str=where_dict['search']
            search_lis=search_str.split(':')
            _where_dict['project']=where_dict['project']
            SEARCH_MAP={}
            SEARCH_MAP['设备类型']='CLASS'
            SEARCH_MAP['区域']='AREA'
            SEARCH_MAP['协议']='PROTOCOL'
            SEARCH_MAP['端口号']='PORT'
            SEARCH_MAP['用户名']='USERNAME'
            SEARCH_MAP['密码']='PASSWORD'
            SEARCH_MAP['特权密码']='SECRET'
            SEARCH_MAP['IP表达式']='IP_EXPRESSION'
            _where_dict[SEARCH_MAP[search_lis[0]]]=search_lis[1]
        else:
            _where_dict=where_dict
        sql=AppStorage.dynamic_sql_return('SELECT * FROM LOGININFO','WHERE','AND',_where_dict)
        return self.oprate_sql(sql,{},callback)

    def get_search_data(self,where_dict):
        def callback(cur,con):
            return cur.fetchall()
        sql=AppStorage.dynamic_sql_return('SELECT * FROM LOGININFO','WHERE','AND',where_dict)
        result=self.oprate_sql(sql,{},callback)
        search_data_list=[]
        value_class=['设备类型:','区域:','协议:','端口号:','用户名:','密码:','特权密码:','IP表达式:']
        for item in result:
           search_data_list+=(list(map(lambda x,y:x+y,value_class,item[2:])))
        search_item_list=[{'value':v} for v in list(set(search_data_list)) if v !='特权密码:']
        return search_item_list
    
    #历史命令数据库相关
    def get_command_history(self,where_dict):
        def callback(cur,con):
            return cur.fetchall()
        _where_dict={}
        if where_dict['mode']=='project':   
            _where_dict['area']='None'
            _where_dict['project']=where_dict['project']
        else:
            _where_dict['area']=where_dict['area']
            _where_dict['project']=where_dict['project']
            _where_dict['protocol']=where_dict['protocol']
            _where_dict['port']=where_dict['port']
            _where_dict['ip_expression']=where_dict['ip_expression']
        if 'command' in where_dict and 'date_time' in where_dict:
            _where_dict['command']=where_dict['command']
            _where_dict['date_time']=where_dict['date_time']
        select_sql=AppStorage.dynamic_sql_return('SELECT * FROM COMMAND_HISTORY','WHERE','AND',_where_dict)
        if 'index' in where_dict:
            limit_sql=f" ORDER BY DATE_TIME DESC limit {where_dict['index']},1"
        else:
            limit_sql=""
        
        full_sql=select_sql+limit_sql
        result=self.oprate_sql(full_sql,{},callback)
        print(result)
        command_history_dict={}
        command_history_dict['command']=result[0][6]
        command_history_dict['response']=json.loads(result[0][7])
        command_history_dict['date_time']=result[0][8]
        print(command_history_dict['date_time'])
        return command_history_dict
    def add_command_history(self,command_history_dict):
        print(command_history_dict)
       
        _command_history_dict={}
        _command_history_dict['project']=command_history_dict['project']
        if command_history_dict['mode']=='project':   
            _command_history_dict['area']='None'
            _command_history_dict['protocol']='None'
            _command_history_dict['port']='None'
            _command_history_dict['ip_expression']='None'
            _command_history_dict['command']=command_history_dict['command']
            _command_history_dict['command_response']=json.dumps(command_history_dict['response'], ensure_ascii=False, indent=2)
            _command_history_dict['date_time']=command_history_dict['date_time']
        else:
            _command_history_dict['area']=command_history_dict['area']
            _command_history_dict['protocol']=command_history_dict['protocol']
            _command_history_dict['port']=command_history_dict['port']
            _command_history_dict['ip_expression']=command_history_dict['ip_expression']
            _command_history_dict['command']=command_history_dict['command']
            _command_history_dict['command_response']=json.dumps(command_history_dict['response'], ensure_ascii=False, indent=2)
            _command_history_dict['date_time']=command_history_dict['date_time']
        
           
        uid =str(uuid.uuid4())
        suid=''.join(uid.split('-'))
        add_parameter_list=list(_command_history_dict.values())
        add_parameter_list.insert(0,suid)
        print(add_parameter_list)
        def callback(cur,con):
            con.commit()
            return True
        return self.oprate_sql(self.__add_command_history_sql,add_parameter_list,callback)
    
    def del_command_history(self,where_dict):
        def callback(cur,con):
            con.commit()
            return True
        delete_sql=AppStorage.dynamic_sql_return('DELETE FROM COMMAND_HISTORY','WHERE','AND',where_dict)
        return self.oprate_sql(delete_sql,where_dict,callback)

    def update_command_history_database(self,dict):
        def callback(cur,con):
            con.commit()
            return True
        before_list=dict['before']
        after_list=dict['after']
        project_after_list = [v[1] for v in after_list]
        project_before_list = [v[1] for v in before_list]
        print('===========================before_list===============================')
        print(before_list)
        print('===========================after_list================================')
        print(after_list)
        for i in before_list:
            for j in after_list:
                if i[0]==j[0] and i[1:]!=j[1:]:
                    print('UPDATE-1')
                    if i[1] not in project_after_list :
                            print('UPDATE-2')
                            where_dict={}
                            update_dict={}
                            where_dict['project']=i[1]
                            where_dict['area']=i[2]
                            where_dict['protocol']=i[3]
                            where_dict['port']=i[4]
                            where_dict['ip_expression']=i[5]
                            update_dict['project']=j[1]
                            update_dict['area']=j[2]
                            update_dict['protocol']=j[3]
                            update_dict['port']=j[4]
                            update_dict['ip_expression']=j[5]
                            where_sql=AppStorage.dynamic_sql_return('','WHERE','AND',where_dict)
                            update_sql=AppStorage.dynamic_sql_return('UPDATE COMMAND_HISTORY','SET',',',update_dict)
                            full_sql=update_sql+where_sql
                            self.oprate_sql(full_sql,{},callback)
                            where_dict['project']=i[1]
                            where_dict['area']='None'
                            where_dict['protocol']='None'
                            where_dict['port']='None'
                            where_dict['ip_expression']='None'
                            update_dict['project']=j[1]
                            update_dict['area']='None'
                            update_dict['protocol']='None'
                            update_dict['port']='None'
                            update_dict['ip_expression']='None'
                            where_sql=AppStorage.dynamic_sql_return('','WHERE','AND',where_dict)
                            update_sql=AppStorage.dynamic_sql_return('UPDATE COMMAND_HISTORY','SET',',',update_dict)
                            full_sql=update_sql+where_sql
                            self.oprate_sql(full_sql,{},callback)
                    else:
                            print('UPDATE-3')
                            where_dict={}
                            update_dict={}
                            where_dict['project']=i[1]
                            where_dict['area']=i[2]
                            where_dict['protocol']=i[3]
                            where_dict['port']=i[4]
                            where_dict['ip_expression']=i[5]
                            update_dict['project']=j[1]
                            update_dict['area']=j[2]
                            update_dict['protocol']=j[3]
                            update_dict['port']=j[4]
                            update_dict['ip_expression']=j[5]
                            where_sql=AppStorage.dynamic_sql_return('','WHERE','AND',where_dict)
                            update_sql=AppStorage.dynamic_sql_return('UPDATE COMMAND_HISTORY','SET',',',update_dict)
                            full_sql=update_sql+where_sql
                            self.oprate_sql(full_sql,{},callback)
                       
                    
                        
    #获取历史命令总条数
    def get_command_history_count(self,where_dict):
        def callback(cur,con):
            return cur.fetchall()
        _where_dict={}
        if where_dict['mode']=='project':   
            _where_dict['project']=where_dict['project']
            _where_dict['area']='None'
        else:
            _where_dict['area']=where_dict['area']
            _where_dict['project']=where_dict['project']
            _where_dict['protocol']=where_dict['protocol']
            _where_dict['port']=where_dict['port']
            _where_dict['ip_expression']=where_dict['ip_expression']
        sql=AppStorage.dynamic_sql_return('SELECT COUNT(*) FROM COMMAND_HISTORY','WHERE','AND',_where_dict)
        result=self.oprate_sql(sql,{},callback)
        return str(result[0][0])
    
    def delete_parameter_database(self,data_dict):
        try:
            print('before and after=========================================')
            print(data_dict['before'])
            print(data_dict['after'])
            tuple_before=(tuple(v) for v in data_dict['before'])
            tuple_after=(tuple(v) for v in data_dict['after'])
            delete_list=list(set(tuple_before)-set(tuple_after))
            for e in delete_list:
                self.delete_filepath_parameter({
                    'project':e[0],
                    'area':e[1]
                                            })
                self.delete_sendcommand_parameter({
                    'project':e[0],
                    'area':e[1]
                                            })
                if self.get_database_data_count('LOGININFO',{'PROJECT':e[0]}):
                    self.delete_filepath_parameter({
                    'project':e[0],
                    'area':'None'
                                            })
                    self.delete_sendcommand_parameter({
                    'project':e[0],
                    'area':'None'
                                            })
            return True
        except:
            return False

         
        [['152e0b8d526147469141e9c0ca416958', '152e0b8d526147469141e9c0ca416958'], ['默认项目', '默认区域'], ['默认项目', '默认区域1'], ['默认项目', '默认区域12']]
        [['152e0b8d526147469141e9c0ca416958', '152e0b8d526147469141e9c0ca416958'], ['默认项目', '默认区域1'], ['默认项目', '默认区域12']]

if __name__ == '__main__':
    ap=AppStorage()
    # s1.add_login_info()
    # dic={'project': '212121212', 'class': '22', 'area': '22', 'protocol': '', 'port': '2', 'username': '2', 'password': '2', 'secret': '', 'ip_expression': ''}
    # where_sql=AppStorage.dynamic_sql('','where','and',dic)
    # update_sql=AppStorage.dynamic_sql('update logininfo','set',',',dic)
    # print(update_sql+where_sql)
    # project_list=ap.get_project_unit_tuple()
    # list1=[ v[0] for v in list]
    print(ap.get_parameter_project_area_data())