<template>
    <div>
        <el-row :gutter="10">
            <el-col>
                <el-menu 
                    style="display: flex;flex-flow: row nowrap;justify-content: space-around;"
                    :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
                    <div>FUN NET</div>
                    <el-menu-item  index="first">CONNECT</el-menu-item>
                    <el-menu-item index="second">CONSOL</el-menu-item>
                </el-menu>
            </el-col>
        </el-row>    
        <router-view></router-view>
    </div>
           
</template>
<script>

export default{
    name:'Meun',
    data(){
        return{
                activeIndex: 'first',
                click_able:false
        }
    },
    methods:{
        tocrud(){
            this.$router.push({
                name:'create'
            })
        },
        handleSelect(key) {
            if(key==='first' || this.activeIndex==='first' && this.click_able===false){
                if(this.click_able===true) return
                this.click_able=true
                this.$router.push({
                    name:'info',
                })
            }
            if(key==='second')
            {
                this.click_able=false
                this.$router.push({
                    name:'cli'
                })
            }
      }
    },
    computed:{
        screen_width(){
            var w= window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth 
            return w+'px'
        }
    },
    mounted(){
        this.handleSelect()
    }
}
</script>
