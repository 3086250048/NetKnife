<template>
    <el-container >
        <el-header height="45px">
            <el-menu style="margin-left: -20px;" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
                <el-menu-item index="first">CONNECT</el-menu-item>
                <el-menu-item index="second">CONSOL</el-menu-item>
            </el-menu>
        </el-header>
        <el-main >
            <router-view></router-view>
        </el-main>
    </el-container>
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
    mounted(){
        this.handleSelect()
    }
}
</script>
