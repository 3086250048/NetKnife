import axios from 'axios'

  export function create_post_request() {
    const requests = {};
    return function send_post(url, data, success_fun, fault_fun) {
      const axios_post = axios.create({
        baseURL: 'http://127.0.0.1:3000'
      });
  
      const requestKey = JSON.stringify({ url, data });
  
      // 如果已经有相同的请求，则取消旧的请求
      if (requests[requestKey]) {
        requests[requestKey]();
      }
  
      axios_post.post(url, data, {
        cancelToken: new axios.CancelToken(c => {
          requests[requestKey] = c;
        })
      }).then(response => {
        if(typeof success_fun === 'function'){
          success_fun(response);
        }
        delete requests[requestKey];
      }).catch(reason => {
        if(typeof fault_fun ==='function'){
          fault_fun(reason);
        }
        delete requests[requestKey];
      });
    }
  }
  export const send_post = create_post_request();
    
  export function create_get_request() {
    const requests = {};
  
    return function send_get(url, success_fun, fault_fun) {
      const axios_get = axios.create({
        baseURL: 'http://127.0.0.1:3000'
      });
  
      const requestKey = url;
  
      // 如果已经有相同的请求，则取消旧的请求
      if (requests[requestKey]) {
        requests[requestKey]();
      }
  
      axios_get.get(url, {cancelToken: new axios.CancelToken(c => {
        requests[requestKey] = c;
      })}).then(response => {
        if(typeof success_fun === 'function'){
          success_fun(response);
        }
        delete requests[requestKey];
      }).catch(reason => {
        if(typeof fault_fun === 'function'){
          fault_fun(reason);
        }
        delete requests[requestKey];
      });
    }
  }
  export const send_get = create_get_request();

  export function areListsEqual(list1, list2) {
    if (list1.length !== list2.length) {
      return false;
    }
    
    for (let i = 0; i < list1.length; i++) {
      const item1 = list1[i];
      const item2 = list2[i];
      
      if (Array.isArray(item1) && Array.isArray(item2)) {
        if (!areListsEqual(item1, item2)) {
          return false;
        }
      } else if (item1 !== item2) {
        return false;
      }
    }
    
    return true;
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