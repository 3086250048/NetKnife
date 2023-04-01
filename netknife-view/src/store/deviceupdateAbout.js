import { send_post,pop_info, send_get,areListsEqual } from './tools'
import { devicestateAbout } from './devicestateAbout'

export const deviceupdateAbout={
    namespaced:true,
    actions:{
        update(context){
            send_post('/check_where',{ 
            'project':context.state.where_info.project,
            'class':context.state.where_info.device_class,
            'area':context.state.where_info.area,
            'protocol':context.state.where_info.protocol,
            'port':context.state.where_info.port,
            'username':context.state.where_info.username,
            'password':context.state.where_info.password,
            'secret':context.state.where_info.secret,
            'ip_expression':context.state.where_info.ip_expression},response=>{
                console.log(response)
                if(response.data==='EXIST'){
                    context.commit('UPDATE')
                }else{
                    pop_info(context.state,'数据不存在','warning')
                }
              
               
            },reason=>{
                pop_info(context.state,'请不要重复发送更新请求','warning')
            })
        }
    },
    mutations:{
        UPDATE(state){
            if(!state.ip_expression_flag && state.update_info.ip_expression){
                pop_info(state,'IP表达式错误','warning')
                return
            }
            if(!state.port_flag && state.update_info.port){
                pop_info(state,'端口范围应在:0~65535之内','warning')
                return
            }

            send_get('/get_project_area_data',response=>{
                state.update_before_project_area_list=response.data
            },reason=>{})
            send_post('/update_data',{ 
                'project': state.update_info.project,
                'class': state.update_info.device_class,
                'area': state.update_info.area,
                'protocol': state.update_info.protocol,
                'port': state.update_info.port,
                'username': state.update_info.username,
                'password': state.update_info.password,
                'secret': state.update_info.secret,
                'ip_expression': state.update_info.ip_expression},response=>{
                    console.log(response)
                    if(response.data==='UPDATE_SUCCESS'){
                        pop_info(state,'数据更新成功','success')
                        devicestateAbout.mutations.GET_PROJECT_UNIT_LIST(devicestateAbout.state)
                        send_get('/get_project_area_data',response=>{
                            state.update_after_project_area_list=response.data
                            console.log(state.update_before_project_area_list)
                            console.log('-------------------------之前')
                            console.log(state.update_after_project_area_list)
                            console.log('-------------------------之后')
                            const before_len=state.update_before_project_area_list.length
                            const after_len=state.update_after_project_area_list.length
                            const _before_lis=state.update_before_project_area_list
                            const _after_lis=state.update_after_project_area_list
                            let merge_list=[]
                            let diff_list=[]
                            if(before_len===after_len){
                                for (let i = 0; i < before_len; i++) {
                                    merge_list.push([_before_lis[i], _after_lis[i]]);
                                }
                                merge_list.forEach(e=>{
                                    if(!areListsEqual(e[0],e[1])){
                                        send_post('/change_filepath_parameter',{
                                            'where':{
                                                'project':e[0][0],
                                                'area':e[0][1]
                                            },
                                            'update':{
                                                'project':e[1][0],
                                                'area':e[1][1]
                                            }
                                        },response=>{
                                            send_post('/get_filepath_parameter',{'project':e[0][0]},response=>{
                                                if(response.data.length==1){
                                                    send_post('/change_filepath_parameter',{
                                                        where:{
                                                            'project':e[0][0]
                                                        },
                                                        update:{
                                                            'project':e[1][0]
                                                        }
                                                    })
                                                }  
                                            })
                                        })
                                        send_post('/change_sendcommand_parameter',{
                                            'where':{
                                                'project':e[0][0],
                                                'area':e[0][1]
                                            },
                                            'update':{
                                                'project':e[1][0],
                                                'area':e[1][1]
                                            }
                                        },response=>{
                                            send_post('/get_sendcommand_parameter',{'project':e[0][0]},response=>{
                                                if(response.data.length==1){
                                                    send_post('/change_sendcommand_parameter',{
                                                        where:{
                                                            'project':e[0][0]
                                                        },
                                                        update:{
                                                            'project':e[1][0]
                                                        }
                                                    })
                                                }  
                                            })
                                        })
                                       
                                    }
                                })
                            }
                            if(before_len>after_len){
                                _before_lis.forEach(element => {
                                    if(! _after_lis.some(item => JSON.stringify(item) === JSON.stringify(element))){
                                        diff_list.push(element)
                                    }
                                });
                                diff_list.forEach(e=>{
                                    send_post('/delete_filepath_parameter',{'project':e[0],'area':e[1]},response=>{
                                        send_post('/get_filepath_parameter',{'project':e[0]},response=>{
                                                if(response.data.length==1){
                                                    send_post('/delete_filepath_parameter',{'project':e[0]})
                                                }
                                        })
                                    })
                                    send_post('/delete_sendcommand_parameter',{'project':e[0],'area':e[1]},response=>{
                                        send_post('/get_sendcommand_parameter',{'project':e[0]},response=>{
                                            if(response.data.length==1){
                                                send_post('/delete_sendcommand_parameter',{'project':e[0]})
                                            }  
                                        })
                                    })
                                })  
                            }   
                            if(before_len<after_len){
                                _after_lis.forEach(element => {
                                    if(! _before_lis.some(item => JSON.stringify(item) === JSON.stringify(element))){
                                        diff_list.push(element)
                                    }
                                });
                                diff_list.forEach(e=>{
                                    send_post('/get_filepath_parameter',
                                    {
                                        'project':e[0]
                                    },response=>{
                                        if(response.data==='None'){
                                            send_post('/add_filepath_parameter',{
                                                'project':e[0],
                                                'area':'None',
                                                'text_export_path': 'default',
                                                'ftp_root_path':'default',  
                                                'ftp_upload_path':'default',
                                                'ftp_download_path':'default',
                                            })
                                            send_post('/add_filepath_parameter',{
                                                'project':e[0],
                                                'area':e[1],
                                                'text_export_path': 'default',
                                                'ftp_root_path':'default',  
                                                'ftp_upload_path':'default',
                                                'ftp_download_path':'default',
                                            })
                                            send_post('/add_sendcommand_parameter',{
                                                'project':e[0],
                                                'area':'None',
                                                'device_title_able':'False',
                                                'command_able':'False',
                                                'read_timeout':10  
                                            })
                                            send_post('/add_sendcommand_parameter',{
                                                'project':e[0],
                                                'area':e[1],
                                                'device_title_able':'False',
                                                'command_able':'False',
                                                'read_timeout':10  
                                            })        
                                        }else{
                                            send_post('/add_filepath_parameter',{
                                                'project':e[0],
                                                'area':e[1],
                                                'text_export_path': 'default',
                                                'ftp_root_path':'default',  
                                                'ftp_upload_path':'default',
                                                'ftp_download_path':'default',
                                            })
                                            send_post('/add_sendcommand_parameter',{
                                                'project':e[0],
                                                'area':e[1],
                                                'device_title_able':'False',
                                                'command_able':'False',
                                                'read_timeout':10  
                                            })        
                                        }
                                    })
                                })
                            }
                        }) 
                    }else{
                        pop_info(state,'更新后最小数据单元存在重复','error')
                    }},reason=>{
                        pop_info(state,'请不要重复发送更新请求','warning')
                })
            },
            IP_EXPRESSION_POP_INFO(state){
                let result=/^((2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d),)*(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)(-(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(%(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)(-(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(%(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)(-(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(%(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)(-(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(%(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(,(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d))*$/.test(state.update_info.ip_expression)
                if(result){
                    state.ip_expression_flag=true
                    pop_info(state,'IP表达式正确','success')
                }else{
                    state.ip_expression_flag=false
                    pop_info(state,'IP表达式错误','error')
                }
            },
            PORT_POP_INFO(state){
                let result=/^\d+$/.test(state.update_info.port)
                if(result && parseInt(state.update_info.port) >= 0 && parseInt(state.update_info.port) <=65535 ){
                    state.port_flag=true
                    pop_info(state,'端口范围正确！！！','success')
                }else{
                    state.port_flag=false
                    pop_info(state,'端口范围应在:0~65535之内','warning')
                }
            }

         
    },
    state:{
        where_info:{
            project:'',
            device_class:'',
            area:'',
            protocol:'',
            port:'',
            username:'',
            password:'',
            ip_expression:'',
            secret:'',

        },
        update_info:{
            project:'',
            device_class:'',
            area:'',
            protocol:'',
            port:'',
            username:'',
            password:'',
            ip_expression:'',
            secret:'',
     
        },
        pop_info:{
            able:false,
            title:'',
            type:''
        },
        ip_expression_flag:false,
        port_flag:false,
        update_before_project_area_list:[],
        update_after_project_area_list:[]
    }

}