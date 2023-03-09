<template>
  <div>
      <button @click="get_test">点击获取测试</button>
  </div>
</template>
<script>
import axios from 'axios'
export default{
  name:'App',
  methods:{
    get_test(){
      axios({
        method:'GET',
        url:'http://127.0.0.1:3000/get'
      }).then(response=>{
        console.log(response)
      })
    },
  }
}
</script>