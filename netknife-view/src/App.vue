<template>
  <el-container id="app">
    <el-header id="header">
      <h1>Netknife</h1>
    </el-header>
    <el-main  id="main">
          <Meun></Meun>
    </el-main>
    <el-footer id="footer" >
      <h1>Footer</h1>
    </el-footer>
  </el-container>
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
  height:50px;
}
#footer{
  background-color: #409EFF;
  color: #303133;
}
#main{
  height: 620px;
  
}
</style>