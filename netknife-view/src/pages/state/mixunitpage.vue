<template>
    <el-container  >
        <el-header v-if="mixunit_view_able" style="margin-top: -20px;" height="30px">
            <div >
                <el-button @click="goback">返回</el-button>
            </div>
            <div>
                <el-autocomplete
                prefix-icon="el-icon-search"
                class="search"
                v-model="input"
                :fetch-suggestions="querySearchAsync"
                placeholder="输入任意单位名称进行搜索"
                @select="handleSelect"
                ></el-autocomplete>
            </div>
        </el-header>
        <el-main v-if="mixunit_view_able">
            <ul>
                <li v-for="(mixunit,i) in mixunit_list" :key="i"> 
                    <el-card class="head_card">
                        <el-badge :value="0" :max="99" class="success" type="primary">
                            <el-button size="small">检测正常</el-button>
                        </el-badge>
                        <el-badge :value="0" :max="99" class="error" >
                        <el-button size="small">检测异常</el-button>
                        </el-badge>
                        <el-badge :value="0" :max="99" class="warning" type="warning">
                            <el-button size="small">检测失败</el-button>
                        </el-badge>
                        <el-button type="primary" class="head_button" @click="show_oprate_page(),set_choose_mixunit(mixunit)">操作</el-button>
                    </el-card>   
                    <el-card class="body_card">
                        <span>区域名称:{{ mixunit[3] }}</span><br>
                        <span>设备类型:{{ mixunit[2]}}</span><br>
                        <span>协议类型:{{ mixunit[4] }}</span><br> 
                        <span>端口号:{{ mixunit[5] }}</span><br>
                        <span>用户名:{{ mixunit[6] }}</span><br>
                        <span>密码:{{ mixunit[7] }}</span><br>
                        <span v-if="if_secret_able(mixunit[8])" >特权密码:{{ mixunit[8] }}</span><br v-if="if_secret_able(mixunit[8])">
                        <span>IP表达式:{{ mixunit[9] }}</span>
                    </el-card>   
                </li>
            </ul>
        </el-main>
        <router-view></router-view>
    </el-container>    
</template>

<script>
import { mapMutations } from 'vuex'
export default{
    name:'MixUnitPage',
    data(){
        return {
            secret_able:false,
            input:''
        }
    },
    methods: {
        ...mapMutations('devicestateAbout',{SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
        ...mapMutations('mixunitpageAbout',{GET_MIXUNIT_DATA:'GET_MIXUNIT_DATA',
                                        SET_MIXUNIT_VIEW_ABLE:'SET_MIXUNIT_VIEW_ABLE'}),
        ...mapMutations('projectoprateAbout',{SET_CHOOSE_MIXUNIT:'SET_CHOOSE_MIXUNIT'}),
        goback(){
            console.log("触发了")
            this.$router.push({
                name:'state',
            })
            this.SET_PROJECT_VIEW_ABLE(true)
        },
        if_secret_able(secret){
            if(secret.length){
                 return true
             }else{
                 return false
             }
        },
        show_oprate_page(){
            this.SET_MIXUNIT_VIEW_ABLE(false)
            this.SET_PROJECT_VIEW_ABLE(false)
            this.$router.push({
                name:'projectoprate',
            })
        },
        set_choose_mixunit(mixunit){
           this.SET_CHOOSE_MIXUNIT(mixunit)
        },
        querySearchAsync(queryString, cb) {
        let results=this.all_project_list
        results = queryString ? results.filter(this.createStateFilter(queryString)) : results;
        cb(results);
        },
        createStateFilter(queryString) {
        return (item) => {
          return item.value.toLowerCase().match(queryString.toLowerCase());
        };

        },
        handleSelect(item) {
            this.CHOOSE_CHANGE(item.value)
        },
    },
    beforeDestroy(){
        
        
    },
    computed:{
        mixunit_list(){
            return this.$store.state.mixunitpageAbout.mixunit_list
        },
        mixunit_view_able(){
            return this.$store.state.mixunitpageAbout.mixunit_view_able
        }
    },
    mounted(){
        this.GET_MIXUNIT_DATA({'project':this.$route.params.project})
    }
}
</script>

<style scoped>
li{
    list-style-type: none;
}
li:not(:first-child){
    margin-top: 8px;
} 
.head_button{
    float: right;
    margin-top: -14px;
    margin-left: 10px;
}
.head_card{
    height: 40px;
}
.search{
    width: 500px;
    position: absolute;
    left: 360px;
    top: 55px;

}
.success{
    float: left;
    margin-top: -10px;
    margin-left: -20px;
}
.error{
    float: left;
    margin-top: -10px;
    margin-left: 28px;
}

.warning{
    float: left;
    margin-top: -10px;
    margin-left: 28px;
}
</style>