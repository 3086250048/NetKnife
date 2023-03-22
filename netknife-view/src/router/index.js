import VueRouter from "vue-router";
import Vue from 'vue'
Vue.use(VueRouter)


import deviceoprate from '../pages/deviceoprate.vue'

import deviceinfo from '../pages/deviceinfo.vue'
import devicestate from '../pages/devicestate.vue'
import devicecrud from '../pages/devicecrud.vue'
import devicecreate from '../pages/crud/devicecreate.vue'
import devicedelete from '../pages/crud/devicedelete.vue'
import deviceupdate from '../pages/crud/deviceupdate.vue'
import mixunitpage from '../pages/state/mixunitpage.vue'
import projectopratepage from '../pages/state/projectopratepage.vue'
import empty from '../pages/empty.vue'

export const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}


export default new VueRouter({
    routes:[
        {   
            name:'info',
            path:'/info',
            component:deviceinfo,
            children:[
                {
                    name:'empty',
                    path:'empty',
                    component:empty
                },
                {
                    name:'state',
                    path:'state',
                    component:devicestate,
                    children:[
                        {
                            name:'projectoprate',
                            path:'projectoprate',
                            component:projectopratepage
                        },
                        {
                            name:'mixunit',
                            path:'mixunit',
                            component:mixunitpage
                        }
                    ]
                },
                {
                    name:'crud',
                    path:'crud',
                    component:devicecrud,
                    children:[
                        {
                            name:'create',
                            path:'create',
                            component:devicecreate
                        },
                        {
                            name:'delete',
                            path:'delete',
                            component:devicedelete
                        },
                        {
                            name:'update',
                            path:'update',
                            component:deviceupdate
                        }
                    ]
                }
            ]
        },
        {
            name:'cli',
            path:'/cli',
            component:deviceoprate
        }

    ]

})