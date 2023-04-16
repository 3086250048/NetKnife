<template>
    <el-container>
        <el-menu  :style="{'margin-left':'-18px',
                            // height:screen_height,
                            width:'109px',
                            display: 'flex',
                            'min-height':'100vh',
                            'flex-direction':'column',
                            'margin-left':'-20px',
                            'margin-top':'-5px' 
                            }"
                           
                            :default-active="activeIndex" class="el-menu-vertical-demo"  @select="handleSelect">
                <el-menu-item index="first">设备状态</el-menu-item>
                <el-menu-item index="second">管理设备</el-menu-item>
                <el-menu-item index="three">管理文件</el-menu-item>
        </el-menu>
        <el-main>
            <router-view></router-view>
        </el-main>
    </el-container>
</template>

<script>
import { send_get } from '@/store/tools'
import { mapMutations } from 'vuex'
export default{
    name:'DeviceInfo',
    data(){
        return {
            activeName:'first',
            activeIndex:'first',
            if_first_load:false,
            
        }
    },
    methods:{
        ...mapMutations('devicestateAbout',{SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
        ...mapMutations('projectoprateAbout',{SET_OPRATE_MODE:'SET_OPRATE_MODE'}),
        handleSelect(key){
            this.activeIndex='first'
            if(key==='second' ){
                this.$bus.$emit('init_active_name')
                this.$router.push({
                    name:'create'
                })
            }
            else if(key==='three'){
                this.$router.push({
                    name:'filemanage'
                })
            }
            else{
                send_get('/select_count',response=>{
                if (response.data[0][0]<=1){
                    this.$router.push({
                        name:'empty',
                        params:{
                            infopage:this
                        }
                    })
                }else{          
                    if(key==='first' || this.activeIndex==='first' && !this.if_first_load){
                        this.SET_OPRATE_MODE('project')
                        this.SET_PROJECT_VIEW_ABLE(true)
                        this.$router.push({
                            name:'state'
                        })
                    }
                }
                })
            }
          
        },
    },
    computed:{
        // screen_height(){
        //     var h=window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
        //     return h+'px'
        // },
        
    },
    mounted(){
        this.handleSelect()
     
    }
}
</script>
