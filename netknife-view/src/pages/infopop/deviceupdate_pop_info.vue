<template>
    <div>
        <el-alert
        class="tag"
        v-show="pop_able"
        :title="pop_title"
        :type="pop_type">
        </el-alert>
    </div>
</template>
<script>
    export default{
            name:'DeviceUpdatePopInfo',
            computed:{
                pop_able(){
                    return this.$store.state.deviceupdateAbout.pop_info.able
                },
                pop_title(){
                    return this.$store.state.deviceupdateAbout.pop_info.title
            },
            pop_type(){
                    return this.$store.state.deviceupdateAbout.pop_info.type
            }
            },
        mounted(){
        //   test
        }
    }
</script>
<style lang="scss" scoped>
.el-alert--error.is-light {
    background-color: #fef0f0;
    color: #F56C6C;
}
.el-alert--warning.is-light {
    background-color: #fdf6ec;
    color: #E6A23C;
}
.el-alert--info.is-light {
    background-color: #f4f4f5;
    color: #909399;
}
.el-alert--success.is-light {
    background-color: #f0f9eb;
    color: #67C23A;
}
.tag ::v-deep .el-alert__closebtn {
    font-size:3vh;
    opacity: 1;
    position: absolute;
    top: 1vh;
    right:1vh;
    cursor: pointer;
}
.tag ::v-deep .el-alert {
    width: 100%;
    padding: 1.8vh 1vh;
    margin: 0;
    box-sizing: border-box;
    border-radius: 4px;
    position: relative;
    background-color: #FFF;
    overflow: hidden;
    opacity: 1;
    display: flex;
    align-items: center;
    transition: opacity .2s;
    margin-bottom: 2vh;
}

::v-deep .el-alert__title {
    font-size: 2vh;
    line-height: 3.6vh;
}
</style>
