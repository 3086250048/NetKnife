<template>
    <el-container >
        <el-header height="35px">
            <el-tabs v-model="activeName" @tab-click="handleClick">
                <el-tab-pane label="设备信息" name="first"></el-tab-pane>
                <el-tab-pane label="命令行管理CLI" name="second"></el-tab-pane>
            </el-tabs>
        </el-header>
        <el-main>
            <router-view></router-view>
        </el-main>
    </el-container>
</template>
<script>

export default{
    name:'Meun',
    data(){
        return{
                activeName:'first' 
        }
    },
    methods:{
        handleClick(tab,event){
            if(this.activeName==='first'){
                this.$router.push({
                    name:'info',
                })
            }else
            {
                this.$router.push({
                    name:'cli'
                })
            }
        },
        tocrud(){
            this.$router.push({
                name:'create'
            })
        }
    },
    mounted(){
        this.handleClick()
    }
}
</script>