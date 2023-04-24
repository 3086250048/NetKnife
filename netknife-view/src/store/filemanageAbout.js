import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filemanageAbout={
    namespaced:true,
    actions:{
    },
    mutations:{         
        SET_TITLE(state,title){
            state.title=title
        },
        HANDLER_RESPONSE_DATA(state,response_data){
            state.excute_response_data=[]
            for(let i=0;i<response_data.length;i++){
                for(let j=0;j<response_data[i].length;j++){
                    console.log(response_data[i][j])
                    state.excute_response_data.push(response_data[i][j])
                }
            }
            console.log(state.excute_response_data)
        },
        SET_EXCUTE_TEXT(state,check_list){
            state.excute_text=''
            let flag=true
            state.excute_response_data.forEach(element=>{
                check_list.forEach(e=>{
                    if(`${element.fun_name}${element.ip}${element.port}${element.type}`===e ){
                        if(flag){
                            state.excute_text+='===============================================================================\n'
                            state.excute_text+=`设备类型:${element.type}  设备登录IP:${element.ip}  设备登录端口:${element.port}\n`
                            state.excute_text+=`时间:${state.response_date_time} 函数名:${element.fun_name}`
                            state.excute_text+='\n===============================================================================\n'
                            state.excute_text+=element.response
                            flag=false
                        }else{
                            state.excute_text+='\n===============================================================================\n'
                            state.excute_text+=`设备类型:${element.type}  设备登录IP:${element.ip}  设备登录端口:${element.port}\n`
                            state.excute_text+=`时间:${state.response_date_time} 函数名:${element.fun_name}`
                            state.excute_text+='\n===============================================================================\n'
                            state.excute_text+=element.response
                        }
                       
                    }
                }) 
            });
        },
        SET_RESPONSE_DATE_TIME(state,time){
            state.response_date_time=time
        }
    },
    state:{
        title:'',
        excute_response_data:[],
        excute_text:'',
        response_date_time:''
    }
}