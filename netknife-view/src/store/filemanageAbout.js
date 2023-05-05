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
                console.log(response_data[i])
                state.excute_response_data.push(response_data[i])
            }
            console.log(state.excute_response_data)
        },
        SET_EXCUTE_TEXT(state,check_list){
            state.excute_text=''
            state.excute_response_data.forEach(element=>{
                check_list.forEach(e=>{
                    if(`${element.fun_name}${element.ip}${element.port}${element.type}`===e ){
                        
                        state.excute_text+=`设备类型:${element.type}  设备登录IP:${element.ip}  设备登录端口:${element.port}\n`
                        state.excute_text+=`时间:${state.response_date_time} 函数名:${element.fun_name}\n`
                        state.excute_text+=element.response+'\n\n'                   
                    }
                }) 
            });
        },
        SET_RESPONSE_DATE_TIME(state,time){
            state.response_date_time=time
        },
        SET_EXCUTE_RESPONSE_DATA(state,data){
            state.excute_response_data=data
        }
    },
    state:{
        title:'',
        excute_response_data:[],
        excute_text:'',
        response_date_time:''
    }
}