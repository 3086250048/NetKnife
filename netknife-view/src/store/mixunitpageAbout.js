import { send_get,send_post,pop_info } from "./tools";

export const  mixunitpageAbout={
    namespaced:true,
    actions:{},
    mutations:{
        GET_MIXUNIT_DATA(state,payload){
            send_post('/get_mixunit_data',{'project':payload.project},response=>{
                state.mixunit_list=response.data
                console.log(state.mixunit_list)
            })
        }
    },
    state:{
       project:'',
       mixunit_list:[]
    }
}
