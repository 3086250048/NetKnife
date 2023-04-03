<template>
    <el-container  >
        <el-header  style="margin-top: -20px;" height="30px">
            <div >
                <el-button @click="goback">返回</el-button>
            </div>
        </el-header>
        <el-main>
            <ul>
                <li> 
                    <el-card class="head_card">
                       
                    </el-card>   
                    <el-card >
                               
                    </el-card>
                </li>
            </ul>
        </el-main>
        <router-view></router-view>
    </el-container>    
</template>

<script>
import { send_get, send_post } from '@/store/tools'
import { mapMutations } from 'vuex'
export default{
    
    name:'MixUnitPage',
    methods: {
        ...mapMutations('devicestateAbout',{SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
       
        goback(){
            console.log("触发了")
            this.$router.push({
                name:'state',
            })
        }
    },
    beforeDestroy(){

        this.SET_PROJECT_VIEW_ABLE(true)
    }
}
</script>

<style>
li{
    list-style-type: none;
}
li:not(:first-child){
    margin-top: 8px;
} 
.head_card{
    height: 40px;
}
</style>