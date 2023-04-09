import { send_post,pop_info,send_get,areListsEqual } from './tools'
import { devicestateAbout } from './devicestateAbout'

export const devicedeleteAbout={
    namespaced:true,
    actions:{
        remove(context){
            send_post('/check_where',{ 
                'project':context.state.delete_info.project,
                'class':context.state.delete_info.device_class,
                'area':context.state.delete_info.area,
                'protocol':context.state.delete_info.protocol ,
                'port': context.state.delete_info.port,
                'username':context.state.delete_info.username,
                'password':context.state.delete_info.password,
                'ip_expression':context.state.delete_info.ip_expression,
                'secret':context.state.delete_info.secret,
                'check_protocol':context.state.delete_info.check_protocol
            },response=>{
                if(response.data=='EXIST'){
                    context.commit('DELETE')
                }
                else{
                    pop_info(context.state,'数据不存在','warning')
                }
            },reason=>{
                pop_info(context.state,'请勿重复发送请求','warning')
            })
        }
    },
    mutations:{
        DELETE(state){
            send_get('/get_project_area',response=>{
                state.delete_before_proeject_area_list=response.data
            },reason=>{})
            // 获取被删除的最小单元的项目名称列表
            send_post('/get_delete_project_list',{
                'project':state.delete_info.project,
                'area':state.delete_info.area,
                'protocol':state.delete_info.protocol,
                'port':state.delete_info.port,
                'ip_expression':state.delete_info.ip_expression,
            },response=>{
                state.delte_project_list=response.data
            })
            // 删除
            send_post('/delete_data',{
                'project':state.delete_info.project,
                'device_class':state.delete_info.device_class,
                'area':state.delete_info.area,
                'protocol':state.delete_info.protocol ,
                'port': state.delete_info.port,
                'username':state.delete_info.username,
                'password':state.delete_info.password,
                'ip_expression':state.delete_info.ip_expression,
                'secret':state.delete_info.secret,
                'check_protocol':state.delete_info.check_protocol
            },response=>{
                if(response.data=='DELETE_SUCCESS'){
                    pop_info(state,'数据删除成功','success')
                    devicestateAbout.mutations.GET_PROJECT_UNIT_LIST(devicestateAbout.state)  
                    //删除历史命令数据库删
                    send_post('/delete_history_command',{
                        'mode':'mixunit',
                        'project':state.delete_info.project,
                        'area':state.delete_info.area,
                        'protocol':state.delete_info.protocol,
                        'port':state.delete_info.port,
                        'ip_expression':state.delete_info.ip_expression,
                    },response=>{
                        console.log(state.delte_project_list)
                        state.delte_project_list.forEach(e=>{
                            send_post('/get_logininfo_project_count',{
                                'project':e[0],
                            },response=>{
                                console.log(response.data)
                                if(response.data==='DELETE_NEXT'){
                                    send_post('/delete_history_command',{
                                        'mode':'project',
                                        'project':state.delete_info.project,
                                    })
                                }
                            })
                        })                       
                    })
                    // 删除参数数据库相关
                    send_get('/get_project_area',response=>{
                        state.delete_after_project_area_list=response.data
                        send_post('/delete_parameter_database',{
                            'before':state.delete_before_proeject_area_list,
                            'after':state.delete_after_project_area_list
                        }) 
                    })
                  
                }else{
                    pop_info(state,'数据删除失败','warning')
                }
            },reason=>{
                pop_info(state,'请勿重复发送删除请求','warning')           
            })
        }
    },
    state:{
        delete_info:{
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
        delete_before_proeject_area_list:[],
        delete_after_project_area_list:[],
        diff_list:[],
        delte_project_list:[]
    }
}