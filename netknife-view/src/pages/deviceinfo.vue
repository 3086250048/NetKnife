<template>
    <el-container>
        <el-aside width="100px">
            <el-tabs v-model="activeName" type="card" tab-position="left" @tab-click="handleClick">
            <el-tab-pane label="设备状态" name="first"></el-tab-pane>
            <el-tab-pane label="管理设备" name="second"></el-tab-pane>
            </el-tabs>
        </el-aside>
        <el-main>
            <router-view></router-view>
        </el-main>
    </el-container>
</template>

<script>
import { send_get } from '@/store/tools'
export default{
    name:'DeviceInfo',
    data(){
        return {
            activeName:'first'
        }
    },
    methods:{
        handleClick(tab,event){
            if(this.activeName==='second'){
                this.$router.push({
                    name:'create'
                })
            }else{
                send_get('/select_count',response=>{
                if (response.data[0][0]<=1){
                    this.$router.push({
                        name:'empty',
                        params:{
                            infopage:this
                        }
                    })
                }else{          
                    if(this.activeName==='first'){
                        this.$router.push({
                            name:'state'
                        })
                    }
                }
                },reason=>{
                })
            }
          
        },
    },
    mounted(){
        this.handleClick()
    }
}
</script>