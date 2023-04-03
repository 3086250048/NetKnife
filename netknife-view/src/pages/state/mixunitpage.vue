<template>
    <el-container  >
        <el-header  style="margin-top: -20px;" height="30px">
            <div >
                <el-button @click="goback">返回</el-button>
            </div>
        </el-header>
        <el-main>
            <ul>
                <li v-for="(mixunit,i) in mixunit_list" :key="i"> 
                    <el-card class="head_card">
                        <span>区域名称:{{ mixunit[3] }}</span><br>
                        <span>设备类型:{{ mixunit[2]}}</span><br>
                        <span>协议类型:{{ mixunit[4] }}</span><br> 
                        <span>端口号:{{ mixunit[5] }}</span><br>
                        <span>用户名:{{ mixunit[6] }}</span><br>
                        <span>密码:{{ mixunit[7] }}</span><br>
                        <span v-if="if_secret_able(mixunit[8])" >特权密码:{{ mixunit[8] }}</span><br v-if="if_secret_able(mixunit[8])">
                        <span>IP表达式:{{ mixunit[9] }}</span>
                    </el-card>   
                </li>
            </ul>
        </el-main>
        <router-view></router-view>
    </el-container>    
</template>

<script>
import { mapMutations } from 'vuex'
export default{
    name:'MixUnitPage',
    data(){
        return {
            secret_able:false
        }
    },
    methods: {
        ...mapMutations('devicestateAbout',{SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
        ...mapMutations('mixunitpageAbout',{GET_MIXUNIT_DATA:'GET_MIXUNIT_DATA'}),
        goback(){
            console.log("触发了")
            this.$router.push({
                name:'state',
            })
        },
        if_secret_able(secret){
            if(secret.length){
                 return true
             }else{
                 return false
             }
        }
    },
    beforeDestroy(){
        this.SET_PROJECT_VIEW_ABLE(true)
    },
    computed:{
        mixunit_list(){
            return this.$store.state.mixunitpageAbout.mixunit_list
        }
    },
    mounted(){
        this.GET_MIXUNIT_DATA({'project':this.$route.params.project})
        this.if_secret_able()
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

</style>