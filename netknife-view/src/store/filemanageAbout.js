import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filemanageAbout={
    namespaced:true,
    actions:{
    },
    mutations:{         
        SET_TITLE(state,title){
            state.title=title
        }
    },
    state:{
        title:''
    }
}