<template>
    <el-tabs type="border-card" v-model="activename" @tab-click="handleClick">
            <el-tab-pane label="新建项目" name="first"></el-tab-pane>
            <el-tab-pane label="更新项目" name="second"></el-tab-pane>
            <el-tab-pane label="删除项目" name="third"></el-tab-pane> 
        <router-view></router-view>
    </el-tabs>
</template>

<script>
export default{
    name:'DeviceCrud',
    data(){
        return{
            activename:'first'
        }
    },
    methods:{
        handleClick(){
            if(this.activename==='first'){
                this.$router.push({
                    name:'create'
                }).then(

                )
            }
            if(this.activename==='second'){
                this.$router.push({
                    name:'update'
                })

            }
            if(this.activename==='third'){
                this.$router.push({
                    name:'delete'
                })
            }
            
        }
    },
    mounted(){
        this.handleClick()
        this.$bus.$on('init_active_name',()=>{
            this.activename='first'
        })
    },
    beforeDestroy(){
        this.$bus.$off('init_active_name')
    }
}
</script>
<style lang="scss" scoped>
    ::v-deep .el-tabs__item {
    padding: 0 20px;
    height: 5vh;
    width: 57vh;
    box-sizing: border-box;
    text-align: center;
    line-height: 5vh;
    display: inline-block;
    list-style: none;
    font-size: 2vh;
    font-weight: 900;
    color: #303133;
    position: relative;
  
}
</style>


