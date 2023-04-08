import re
class AppAction():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance           
    def export(self,parameter,content):
        with open(parameter, "w") as file:
            file.write(content)
            print('写入了')
    def action_class_map(self,action_class,parameter,content):
        action_map={
            'export':self.export  
        }
        action_map[action_class](parameter,content)
class ButtonAction():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance   
    
    def export_textarea(self,export_dict):
        try:
            print(export_dict)
            file_name_list=re.split('[<>/\|:*? ]',export_dict['command']) 
            file_name_str='_'.join(file_name_list)
            full_file_path=export_dict['txt_export_path']+file_name_str+'.txt'
            print(full_file_path)
            with open(full_file_path, "w") as file:
                file.write(export_dict['textarea'])
            return True
        except:
            return False