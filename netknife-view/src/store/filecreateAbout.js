import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filecreateAbout={
    namespaced:true,
    actions:{

    },
    mutations:{         
        CREATE_NETKNIFE_FILE(state,code){
            state.code=code
            console.log(state.code)
            send_post('/create_netknife_file',{
            'code':state.code
            })
            
        }
    },
    state:{
        code:''
    }
}