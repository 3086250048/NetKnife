import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filestateAbout={
    namespaced:true,
    actions:{
    },
    mutations:{    
        GET_NETKNIFE_DATA(state){
            send_get('/get_netknife_file_data',response=>{
                if (response.data==='NOT_EXIST'){return}
                state.netknife_data=response.data
                state.full_netknife_data=response.data
                state.netknife_data.forEach(e=>{
                    if(e['translation'].length<=0){
                        e['translation_class']='el-icon-circle-close'
                    }else{
                      e['translation_class']='el-icon-success'
                    }
                    if(e['jinja2'].length<=0){
                        e['jinja2_class']='el-icon-circle-close'
                    }else{
                      e['jinja2_class']='el-icon-success'
                    }
                    if(e['excute'].length<=0){
                        e['excute_class']='el-icon-circle-close'
                    }else{
                      e['excute_class']='el-icon-success'
                    } 
                    if(e['config'].length<=0){
                        e['config_class']='el-icon-circle-close'
                    }else{
                        e['config_class']='el-icon-success'
                    }
                })
            })   
        },
        CHOOSE_CHANGE(state,file_name){
            state.netknife_data=[]
            for(let i =0;i<state.full_netknife_data.length;i++){
                if (state.full_netknife_data[i]['netknife'][0]===file_name){
                    state.netknife_data.push(state.full_netknife_data[i])
                }
            }
        },
        ROLLBACK_NETKNIFE_DATA(state){
            state.netknife_data=state.full_netknife_data
        }
    },
    state:{
        netknife_data:[],
        full_netknife_data:[]
    }
}