<template>
    <el-card class="box-card">
  <div slot="header" class="clearfix">
    <el-tag>Ruijie翻译文件</el-tag>
    <el-tag type="danger" >100</el-tag>
    <el-button style="float: right; padding: 3px 0" type="text">打开文件</el-button>
  </div>
  <!-- <el-collapse class="collapse" v-model="activeNames" @change="handleChange">
  <el-collapse-item title="Translation" name="1" >
    <div >与现实生活一致：与现实生活的流程、逻辑保持一致，遵循用户习惯的语言和概念；</div>
  </el-collapse-item>
  <el-collapse-item title="Jinja2" name="2"   >
    <div>控制反馈：通过界面样式和交互动效让用户可以清晰的感知自己的操作；</div>
  </el-collapse-item>
</el-collapse> -->
</el-card>
    
</template>

<script>
import { mapMutations} from 'vuex'
export default{
    data(){
        return{
            activeNames: []
        }
    },
    name:'FileState',
    methods:{
        ...mapMutations('filestateAbout',{GET_NETKNIFE_DATA:'GET_NETKNIFE_DATA'}),
        handleChange(val) {
        console.log(val);
      }
    },
    mounted(){
        this.GET_NETKNIFE_DATA()
    }
}

</script>

<style>
.collapse{
    position: relative;
    top: -20px;
}

</style>