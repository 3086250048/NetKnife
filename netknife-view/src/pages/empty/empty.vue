<template>
    <div style="height: 100vh;">
        <el-empty description="没有代管理的项目"  :image-size="auto_size/4" style="height: 100%;">
                <el-button style="width: 20vh;height: 6vh;font-size: 2vh;line-height: 1vh;border-radius: 0.8vh;" type="primary" @click="forward_to_create">新建项目</el-button>
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
    name:'Empty',
    methods:{
        forward_to_create(){
        this.$bus.$emit('switch_activeIndex','second')
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