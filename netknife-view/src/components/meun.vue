<template>
    <div>
        <el-row :gutter="10">
            <el-col :span="24">
                <el-menu 
                    style="display: flex;flex-flow: row nowrap;justify-content: space-around;height: 8vh;"
                    :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
                    <div style="width: 10%;height: 8vh;font-size: 2vh;line-height: 8vh;text-align: center;">Netknife</div>
                    <el-menu-item style="width: 45%;text-align: center;height: 8vh;font-size: 2vh;line-height: 8vh;font-weight: 600;" index="first">CONNECT</el-menu-item>
                    <el-menu-item style="width: 45%;text-align: center;height: 8vh;font-size: 2vh;line-height: 8vh;font-weight:600;" index="second">CONSOL</el-menu-item>
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
<style lang="scss" scoped > 
::v-deep .el-menu--horizontal>.el-menu-item.is-active{
    border-bottom: 0.5vh solid #409EFF;
}


</style>
