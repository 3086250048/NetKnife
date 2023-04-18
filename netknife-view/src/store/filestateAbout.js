import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filestateAbout={
    namespaced:true,
    actions:{
    },
    mutations:{    
        GET_NETKNIFE_DATA(state){
            send_get('/get_netknife_file_data')   
        }
        
    },
    state:{
        netknife_data:[]
    }
}