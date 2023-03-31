import { send_post,send_get,pop_info } from './tools'
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
    }
}