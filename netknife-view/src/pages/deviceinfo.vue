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
                <el-menu-item index="three">文件状态</el-menu-item>
                <el-menu-item index="four">管理文件</el-menu-item>
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
            if(key===undefined){
                this.activeIndex='first'
            }else{
                this.activeIndex=key
            }
            if(key==='second' ){
                this.$bus.$emit('init_active_name')
                this.$router.push({
                    name:'create'
                })
            }
            else if (key==='three'){
                send_get('/if_exist_netknife_file',response=>{
                    if(response.data==='NOT_EXIST'){
                        this.$router.push({
                            name:'fileempty'
                        })
                    }else{
                        this.$router.push({
                            name:'filestate'
                        })
                    }
                })
            }
            else if(key==='four'){
                if(localStorage.length===0){
                    this.$router.push({
                        name:'pageempty'
                    })
                }else{
                    this.$router.push({
                        name:'filemanage'
                    })
                }
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
        switch_handler(index,item){
            if (index==='first'){
                this.activeIndex='first'
            }
            if(index==='second'){
                this.activeIndex='second'
                this.$router.push({
                    name:'create'
                })
            }
            if(index==='three'){
                this.activeIndex='three'
                send_get('/if_exist_netknife_file',response=>{
                    if(response.data==='NOT_EXIST'){
                        this.$router.push({
                            name:'fileempty'
                        })
                    }else{
                        this.$router.push({
                            name:'filestate'
                        })
                    }
                })
            }
            if(index==='four'){
                this.activeIndex='four'
                if(localStorage.length===0){
                    this.$router.push({
                        name:'pageempty'
                    })
                }else{
                    this.$router.push({
                        name:'filemanage'
                    })
                }
            }
            if(index==='open_file'){
                this.activeIndex='four'
                this.$router.push({
                    name:'filemanage',
                    params:{
                        item:item
                    }
                })
                
              
            }
        }
    },
    mounted(){
        this.handleSelect()
        this.$bus.$on('switch_activeIndex',(index,item)=>{
            this.switch_handler(index,item)
        })
    },
    beforeDestroy(){
       this.$bus.$off('switch_activeIndex')
    }
}
</script>
