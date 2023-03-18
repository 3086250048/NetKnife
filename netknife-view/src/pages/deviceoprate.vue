<template>
    <el-input
    style="width: 400px;"
    type="textarea"
    :rows="20"
    placeholder="请输入内容"
    resize="none"
    v-model="textarea"
    >
    </el-input>
    
</template>

<script>

export default{
    name:'DeviceOprate',
    data(){
        return {
            textarea:''
        }
    },methods:{
        
    },
    components:{
        
    },
    computed:{
          
    },
    watch:{
        textarea(new_value,old_value){
            new_value='>>>'+old_value
        }
    }
}

</script>

<style>
.cli_box{
    color: aliceblue;
    background-color: black;
    height: 500px;
    width: 800px;
}
</style>