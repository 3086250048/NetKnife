<template>
  <el-container class="crud_div">
        <el-main style="margin-left: -30px;margin-top: -40px;">
            <el-tabs type="border-card" v-model="activename" @tab-click="handleClick">
            <el-tab-pane label="编写文件" name="first">
            </el-tab-pane>
            <el-tab-pane label="修改文件" name="second"></el-tab-pane>
            <router-view></router-view>
            </el-tabs>
        </el-main>
    </el-container>
</template>

<script>
export default{
  name:"FileManage",
  data(){
    return {
        activename:"first"
    }
  },
  methods:{
    handleClick(){
      if(this.activename==="first"){
        this.$router.push({
          name:'filecreate'
          }).then(
        )
      }
    }
  }
}
</script>