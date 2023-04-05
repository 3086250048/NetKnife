import { send_get,send_post,pop_info } from "./tools";

export const  mixunitpageAbout={
    namespaced:true,
    actions:{},
    mutations:{
        GET_MIXUNIT_DATA(state,payload){
            send_post('/get_mixunit_data',{'project':payload.project},response=>{
                state.mixunit_list=response.data
                state.full_mixunit_list=response.data
            })
        },
        GET_SEARCH_DATA(state,project){
            send_post('/get_search_data',{project:project},response=>{
                state.mixunit_search_list=response.data
            })
        },
        SET_MIXUNIT_VIEW_ABLE(state,able){
            state.mixunit_view_able=able
        },
        CHOOSE_CHANGE(state,payload){
            send_post('/get_mixunit_data',{'project':payload.project,'search':payload.search},response=>{
                state.mixunit_list=response.data
            })
        },
        ROLLBACK_MIXUNIT_LIST(state){
            state.mixunit_list=state.full_mixunit_list
        },
        SET_MIXUNIT_LIST(state,list){
            state.mixunit_list=list
        }

    },
    state:{
       project:'',
       full_mixunit_list:[],
       mixunit_list:[],
       mixunit_view_able:true,
       mixunit_search_list:[]

    }
}
