import axios from 'axios'
export let cancel=null
export function send_post(url,data,success_fun,fault_fun){
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

export function send_get(url,success_fun,fault_fun){
    const axios_get=axios.create({
        baseURL:'http://127.0.0.1:3000'
    })
    if( cancel !== null ) cancel()
    axios_get.get(url,{cancelToken: new axios.CancelToken(c=>{cancel=c})}).then(
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

export function pop_info(state,title,type){
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

export function get_time(){
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false,
        timeZone: 'Asia/Shanghai'
      };
      
      const date = new Date();
      const formatter = new Intl.DateTimeFormat('zh-CN', options);
      const formattedDate = formatter.format(date);
      return formattedDate
}