
import {deviceaddAbout} from './deviceaddAbout'
import {deviceupdateAbout} from './deviceupdateAbout'
import { devicedeleteAbout } from './devicedeleteAbout'
import { devicestateAbout } from './devicestateAbout'
import { routingAbout } from './routingAbout'



import Vuex from 'vuex'
import Vue from 'vue'


Vue.use(Vuex)
export default new Vuex.Store({
    modules:{
        deviceaddAbout:deviceaddAbout,
        deviceupdateAbout:deviceupdateAbout,
        devicedeleteAbout:devicedeleteAbout,
        devicestateAbout:devicestateAbout,
        routingAbout:routingAbout
    }
})