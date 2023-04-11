<template>
    <el-container class="crud_div">
        <el-main style="margin-left: -30px;margin-top: -40px;">
            <el-tabs type="border-card" v-model="activename" @tab-click="handleClick">
            <el-tab-pane label="新建项目" name="first"></el-tab-pane>
            <el-tab-pane label="更新项目" name="second"></el-tab-pane>
            <el-tab-pane label="删除项目" name="third"></el-tab-pane>
            <router-view></router-view>
            </el-tabs>
        </el-main>
    </el-container>
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
<style scoped>
   .curd_div{
    background-color: #DCDFE6;
   }
</style>


