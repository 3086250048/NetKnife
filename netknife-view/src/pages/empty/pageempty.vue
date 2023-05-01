<template>
    <div style="height: 100vh;">
        <el-empty description="新键窗口或打开文件开始编辑" :image-size="auto_size/4" style="height: 100%;" >
                <el-button style="width: 20vh;height: 6vh;font-size: 2vh;line-height: 1vh;border-radius: 0.8vh;" type="primary" @click="create_page">新建窗口</el-button>
                <el-button style="width: 20vh;height: 6vh;font-size: 2vh;line-height: 1vh;border-radius: 0.8vh;" type="primary" @click="open_page">打开文件</el-button>
        </el-empty>
    </div>
    
</template>

<script>

export default{
    data(){
        return {
            auto_size:`${document.documentElement.clientHeight}`
        }
    },
    name:'PageEmpty',
    methods:{
        create_page(){
            this.$router.push({
                name:'filemanage'
            })
        },
        open_page(){
            this.$bus.$emit('switch_activeIndex','three')
        }
    },
    mounted(){
        const _this = this;
        window.onresize = ()=>{
            return (() => {
            _this.auto_size = `${document.documentElement.clientHeight}`;
            })();
        };
    }
}

</script>
<style lang="scss">
    .el-empty__description p {
    margin: 0;
    font-size: 2vh;
    color: #909399;
}

</style>