import axios from 'axios'

let cancel=null
function send_post(url,data,success_fun,fault_fun){
    const axios_post=axios.create({
        baseURL:'http://127.0.0.1:3000'
    })
    if( cancel !== null ) cancel()
    axios_post.post(url,data,{cancelToken: new axios.CancelToken(c=>{cancel=c})}).then(
        response=>{
            success_fun(response)
            cancel=null
        }
    ).catch(
        reason=>{
             fault_fun(reason)
        }
    )
}

function pop_info(state,title,type){
    state.pop_info.able=true
    state.pop_info.title=title
    state.pop_info.type=type

    if(state.time_id == null){
        state.time_id=setTimeout(()=>{
            state.pop_info.able=false
            state.time_id=null
        },3000)
    }
}

const deviceaddAbout={
    namespaced:true,
    actions:{
            /*弹窗类型:success\info\warning\error*/
        commit(context){
            if(context.state.device_info.project == ''){
                context.commit('PROJECT_POP_INFO')
                return
            } 
            if(context.state.device_info.device_class ==''){
                context.commit('DEVICE_CLASS_POP_INFO')
                return
            }
            
            if(context.state.device_info.area==''){
                context.commit('AREA_POP_INFO')
                return
            }
            if(context.state.device_info.protocol ==''){
                context.commit('PROTOCOL_POP_INFO')
                return
            } 
            if(context.state.device_info.port ==''){
                context.commit('PORT_POP_INFO')
                return
            }
            if(context.state.device_info.ip_expression == ''){
                context.commit('IP_EXPRESSION_POP_INFO')
                return
            }
            if(context.state.device_info.username ==''){
                context.commit('USERNAME_POP_INFO')
                return
            } 
            if(context.state.device_info.password ==''){ 
                context.commit('PASSWORD_POP_INFO')
                return
            } 
            context.commit('COMMIT')
        },
        checkip(context){
            if(context.state.device_info.check_protocol=='icmp'){
               context.commit('CHECKIP_ICMP')
            }else{
               context.commit('CHECKIP_TCP')
            }
        },
        

    },
    mutations:{
        COMMIT(state){
            console.log(state.ip_expression_check_flag,1)
            console.log(state.port_range_check_flag)
            if(state.ip_expression_check_flag && state.port_range_check_flag && state.project_check_flag){
                send_post('/commit',{
                    'project':state.device_info.project,
                    'class':state.device_info.device_class,
                    'area':state.device_info.area,
                    'protocol':state.device_info.protocol,
                    'port':state.device_info.port,
                    'username':state.device_info.username,
                    'password':state.device_info.password,
                    'secret':state.device_info.secret,
                    'ip_expression':state.device_info.ip_expression}
                    ,(response)=>{
                        console.log(response)
                        pop_info(state,'设备信息提交成功','success')
                    },(reason)=>{
                        pop_info(state,'请不要重复提交设备信息','warning')
                    })
            }else{
                pop_info(state,'请检查填写表项是否存在错误','error')
            }
           
        },
        CHECK_PROJECT_POP_INFO(state){
            send_post('/check_project',{'project':state.device_info.project},response=>{
                console.log(response.data)
                 if(response.data === 'NOT_USED'){
                    state.project_check_flag=true
                    pop_info(state,'项目名未被使用','success')
                 }else{
                    state.project_check_flag=false
                    pop_info(state,'项目名称被使用','info')
                 }
            },
            reason=>{
                 pop_info(state,'项目名检测失败','error')
            }
            )
        },
        CHECKIP_ICMP(state){
            send_post('/checkip_icmp',{'ip_expression':state.device_info.ip_expression},response=>{
                if(response.data.length>0){ 
                    let result=''
                    response.data.forEach(element => {
                        result+=element+' ； '
                    });
                    if(result.length>=100){
                        result=result.slice(0,97)+'...'
                    }
                    result='ICMP检测失败:'+result
                    pop_info(state,result,'warning')
                }else{
                    pop_info(state,'ICMP检测成功！！！','success')
                }
            },reason=>{
                pop_info(state,'请不要重复发送ICMP检测','warning')
                })
        },
        CHECKIP_TCP(state){
            send_post('/checkip_tcp',{'ip_expression':state.device_info.ip_expression,'port':state.device_info.port},response=>{
                if(response.data.length>0){
                    let result=''
                    response.data.forEach(element => {
                        result+=element['ip']+':'+element['port']+' ； '
                    });
                    if(result.length>=100){
                        result=result.slice(0,97)+'...'
                    }
                    result='TCP检测失败:'+result
                    pop_info(state,result,'warning')
                }else{
                    pop_info(state,'TCP检测成功!!!','success')
                }
            },reason=>{
                pop_info(state,'请不要重复发送TCP检测','warning')
            })
        },
        PROJECT_POP_INFO(state){
            pop_info(state,'项目名称不能为空','error')
        },
        DEVICE_CLASS_POP_INFO(state){
            pop_info(state,'设备类型不能为空','error')
        },
        AREA_POP_INFO(state){
            pop_info(state,'设备区域不能为空','error')
        },
        PROTOCOL_POP_INFO(state){
            pop_info(state,'设备登录协议不能为空','error')
        },
        PORT_POP_INFO(state){
            pop_info(state,'设备登录端口不能为空','error')
        },
        CHECK_PORT_RANGE_POP_INFO(state){
            let result=/^\d+$/.test(state.device_info.port)
            if(result && parseInt(state.device_info.port) >= 0 && parseInt(state.device_info.port) <=65535 ){
                state.port_range_check_flag=true
                pop_info(state,'端口范围正确！！！','success')
            }else{
                state.port_range_check_flag=false
                pop_info(state,'端口范围应在:0~65535之内','error')
            }
        },
        IP_EXPRESSION_POP_INFO(state){
            pop_info(state,'设备IP表达式不能为空','error')
        },
        CHECK_IP_EXPRESSION_POP_INFO(state){
            let result=/^((2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d),)*(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)(-(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(%(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)(-(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(%(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)(-(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(%(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)(-(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(%(2[0-4][0-9]|[1-2][0-5][0-5]|[1-9]?\d))?(,(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d)\.(2[0-4][0-9]|2[0-5][0-5]|1[0-9][0-9]|[1-9]?\d))*$/.test(state.device_info.ip_expression)
            if(result){
                pop_info(state,'IP表达式正确','success')    
                state.ip_expression_check_flag=true        
            }else{
                pop_info(state,'IP表达式错误','error')
                state.ip_expression_check_flag=false
            }
        },
        USERNAME_POP_INFO(state){
            pop_info(state,'设备用户名不能为空','error')
        },
        PASSWORD_POP_INFO(state){
            pop_info(state,'设备密码不能为空','error')
        },
       

    },
    state:{
        device_info:{
            project:'默认项目',
            device_class:'huawei',
            area:'默认区域',
            protocol:'telnet',
            port:'23',
            username:'',
            password:'',
            ip_expression:'',
            secret:'',
            check_protocol:'icmp'
        },
        pop_info:{
            able:false,
            title:'',
            type:''
        },
        ip_expression_check_flag:false,
        port_range_check_flag:true,
        project_check_flag:true
    }

}

const deviceupdateAbout={
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
                    }else{
                        pop_info(state,'数据更新失败','error')
                    }},reason=>{
                        pop_info(state,'请不要重复发送更新请求','warning')
                })
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
        
    }

}

const devicedeleteAbout={
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


import Vuex from 'vuex'
import Vue from 'vue'



Vue.use(Vuex)
export default new Vuex.Store({
    modules:{
        deviceaddAbout:deviceaddAbout,
        deviceupdateAbout:deviceupdateAbout,
        devicedeleteAbout:devicedeleteAbout
    }
})