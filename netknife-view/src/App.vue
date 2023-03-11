<template>
  <el-container>
    <el-header id="header">
      <h1>Netknife</h1>
    </el-header>
    <el-main  id="main">
      <div></div>
      <div id='mainbox'>
          <Meun></Meun>
      </div>
    </el-main>
    <el-footer id="footer">
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
<style>
#header{
  background-color: green;
}
#footer{
  background-color: green;
}
#mainbox{
  height: 640px;
}
</style>