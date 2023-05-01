<template>
    <div style="height: 100vh;">
        <el-empty description="开始创建第一个Netknife文件" :image-size="auto_size/4" style="height: 100%;">
                <el-button style="width: 20vh;height: 6vh;font-size: 2vh;line-height: 1vh;border-radius: 0.8vh;" type="primary" @click="forward_filemanage">创建文件</el-button>
        </el-empty>
    </div>
    
</template>

<script>
window.onresize = function(){
    alert(document.documentElement.clientHeight);
}
export default{
    data(){
        return {
            auto_size:`${document.documentElement.clientHeight}`
        }
    },
    name:'FileEmpty',
    methods:{
        forward_filemanage(){
            this.$bus.$emit('switch_activeIndex','four')
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