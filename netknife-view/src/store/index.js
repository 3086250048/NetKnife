const deviceaddAbout={
    namespaced:true,
    actions:{

    },
    mutations:{

    },
    state:{
        device_info:{
            project:'',
            device_class:'',
            area:'',
            protocol:'',
            port:'',
            username:'',
            password:'',
            ip_expression:'',
            secret:'',
            check_protocol:'icmp'
        },
    }

}
import Vuex from 'vuex'
import Vue from 'vue'
Vue.use(Vuex)
export default new Vuex.Store({
    modules:{
        deviceaddAbout:deviceaddAbout
    }
})