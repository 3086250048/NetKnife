<template>
        <Meun></Meun>
</template>
<script>
import meun from './components/meun.vue';
export default{
    name:'App',
    components:{
      Meun:meun
    }
}
</script>
<style scoped>
#header{
  background-color: #409EFF;
  color:#303133 ;
  height:20px;
}
#footer{
  background-color: #409EFF;
  color: #303133;
}
h1{
  margin-top: 6px;
  font-size: 50px;
  font-weight:bold;
}

</style>
