<template>
    <div>
        <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="设备信息" name="first"></el-tab-pane>
            <el-tab-pane label="命令行管理CLI" name="second"></el-tab-pane>
       
        
        </el-tabs>
        <router-view></router-view>
    </div>
</template>
<script>
// import deviceinfo from '../pages/deviceinfo.vue'
// import deviceoprate from '../pages/deviceoprate.vue'
export default{
    name:'Meun',
    // components:{
    //     DeviceInfo:deviceinfo,
    //     DeviceOprate:deviceoprate
    // },
    data(){
        return{
                activeName:'first' 
        }
    },
    methods:{
        handleClick(tab,event){
            console.log(tab,event)
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
    },
    mounted(){
        this.handleClick()
    }
}
</script>