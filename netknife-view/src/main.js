import Vue from 'vue'
import App from './App.vue'
//引入ElementUI组件库
import ElementUI from 'element-ui'
//引入ElementUI全部样式
import 'element-ui/lib/theme-chalk/index.css'
//应用ElementUI
Vue.use(ElementUI)
//关闭语法提示
Vue.config.productionTip = false
// //引入Vuex插件
import store from './store/index'

import router from './router/index'
new Vue({
  el:'#app',
  store:store,
  router:router,
  render: CreateElement => CreateElement(App),
  beforeCreate(){
    Vue.prototype.$bus=this
  }
})
