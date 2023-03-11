import axios from 'axios'



const deviceaddAbout={
    namespaced:true,
    actions:{
            /*弹窗类型:success\info\warning\error*/
        commit(context){
            if(context.state.device_info.project !== ''){
                
                context.commit('COMMIT')

            }else{
               context.commit('POP_INFO')
            }
        },
        checkip(context){
            if(context.state.device_info.check_protocol=='icmp'){
               context.commit('CHECKIP_ICMP')
            }else{
               context.commit('CHECKIP_TCP')
            }
            
        }
    },
    mutations:{
        COMMIT(state){
            axios({
                method:'POST',
                url:'http://127.0.0.1:3000/commit',
                data:{
                    project:state.project,
                    class:state.device_class,
                    area:state.area,
                    protocol:state.protocol,
                    port:state.port,
                    username:state.username,
                    password:state.password,
                    secret:state.secret,
                    ip:state.ip_expression
                }
            }).then(response=>console.log(response.data))
            .catch(reason=>{console.log(reason)})
        },
        CHECKIP_ICMP(state){
            axios({
                method:'POST',
                url:'http://127.0.0.1:3000/checkip_icmp',
                data:{
                    ip:state.device_info.ip_expression
                }
            }).then(response=>{
                if(response.data.length>0){
                    console.log(response.data)
                    state.pop_info.able=true
                    if(this.time_id == null){
                        this.time_id=setTimeout(()=>{
                            state.pop_info.able=false
                            this.time_id=null
                        },3000)
                    }
                    state.pop_info.type='warning'
                    let result=''
                    response.data.forEach(element => {
                        result+=element+' ； '
                    });
                    if(result.length>=100){
                        result=result.slice(0,97)+'...'
                    }
                    state.pop_info.title='ICMP检测失败:'+result
                }else{
                    state.pop_info.able=true
                    if(this.time_id == null){
                        this.time_id=setTimeout(()=>{
                            state.pop_info.able=false
                            this.time_id=null
                        },3000)
                    }
                    state.pop_info.type='success'
                    state.pop_info.title='ICMP检测成功!!!'
                }
               

            })
            .catch(reason=>{console.log(reason)})
        },
        CHECKIP_TCP(state){
           
            axios({
                method:'POST',
                url:'http://127.0.0.1:3000/checkip_tcp',
                data:{
                    ip:state.device_info.ip_expression
                }
                }).then(response=>{
                    if(response.data.length>0){
                        console.log(response.data)
                        state.pop_info.able=true
                        if(this.time_id == null){
                            this.time_id=setTimeout(()=>{
                                state.pop_info.able=false
                                this.time_id=null
                            },3000)
                        }
                        state.pop_info.type='warning'
                        let result=''
                        response.data.forEach(element => {
                            result+=element['ip']+element['port']+' ； '
                        });
                        if(result.length>=100){
                            result=result.slice(0,97)+'...'
                        }
                        state.pop_info.title='TCP检测失败:'+result
                    }else{
                        state.pop_info.able=true
                        if(this.time_id == null){
                            this.time_id=setTimeout(()=>{
                                state.pop_info.able=false
                                this.time_id=null
                            },3000)
                        }
                        state.pop_info.type='success'
                        state.pop_info.title='TCP检测成功！！！'

                    }
                })
                .catch(reason=>{console.log(reason)})
        },
        POP_INFO(state){
            state.pop_info.able=true
            state.pop_info.title='项目名称不能为空'
            state.pop_info.type='error'
            
            if(this.time_id == null){
                this.time_id=setTimeout(()=>{
                    state.pop_info.able=false
                    this.time_id=null
                },3000)
            }
        }

    },
    state:{
        device_info:{
            project:'',
            device_class:'',
            area:'',
            protocol:'',
            port:'',
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
        }
    }

}
import Vuex from 'vuex'
import Vue from 'vue'
Vue.use(Vuex)
export default new Vuex.Store({
    modules:{
        deviceaddAbout:deviceaddAbout
    }
})