import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'
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
            // 给更新参数数据库用
            send_get('/get_project_area_data',response=>{
                state.update_before_project_area_list=response.data
            })
            //给更新历史命令数据库用
            send_get('/get_id_mixunit_data',response=>{
                state.update_before_id_mixunit_list=response.data
            })

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
                    if(response.data==='UPDATE_SUCCESS'){
                        pop_info(state,'数据更新成功','success')
                        devicestateAbout.mutations.GET_PROJECT_UNIT_LIST(devicestateAbout.state)
                        
                        // 给更新参数数据库用的
                        send_get('/get_project_area_data',response=>{
                            state.update_after_project_area_list=response.data
                            send_post('/update_parameter_database',{
                                'before':state.update_before_project_area_list,
                                'after':state.update_after_project_area_list
                            })
                        }) 

                        // 给更新历史命令数据库用的
                        send_get('/get_id_mixunit_data',response=>{
                            state.update_after_id_mixunit_list=response.data
                            send_post('/update_command_history_database',{
                                'before':state.update_before_id_mixunit_list,
                                'after':state.update_after_id_mixunit_list
                            })
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
        update_after_project_area_list:[],
        update_item_list:[],
        diff_item_list:[],
        update_before_id_mixunit_list:[],
        update_after_id_mixunit_list:[]
    }

}