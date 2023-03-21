<template>
    <el-container>
        <el-tabs v-model="activeName" type="card" tab-position="left" @tab-click="handleClick">
        <el-tab-pane label="设备状态" name="first"></el-tab-pane>
        <el-tab-pane label="管理设备" name="second"></el-tab-pane>
        </el-tabs>
        <router-view></router-view>
    </el-container>
</template>

<script>

export default{
    name:'DeviceInfo',
    data(){
        return {
            activeName:'first'
        }
    },
    methods:{
        handleClick(tab,event){
            if(this.activeName==='first'){
                this.$router.push({
                    name:'state'
                })
            }else{
                this.$router.push({
                    name:'create'
                })
            }
        },
    },
    mounted(){
        this.handleClick()
    }
}
</script>