<template>
  <div>
      <div>
        <el-header  style="margin-top: -20px;" height="30px">
          <el-autocomplete
          prefix-icon="el-icon-search"
          style="width: 500px;margin-left: 200px;"
          v-model="input"
          :fetch-suggestions="querySearchAsync"
          placeholder="输入文件名称进行搜索"
          @select="handleSelect"
          ></el-autocomplete>
        </el-header>
      </div>
      <div class="netknife_ul">
        <ul>
            <li v-for="item,index in netknife_data" :key="index">
              <el-card class="box-card card">
                  <el-tag style="position: relative;top:-20px;left: -20px;height: 60px;font-size: 20px;fon" > <div style="line-height: 60px;">{{ item['netknife'][0].length>20?item['netknife'][0].slice(0,20)+'...':item['netknife'][0] }}</div></el-tag>
                  &nbsp;
                  <el-tag style="position: relative;top:-20px;left: -35px;height: 60px;font-size: 20px;" type="danger" ><div style="line-height: 60px;">{{ item['netknife'][1]}}</div></el-tag>
                  <el-button style="float: right; padding: 3px 0" type="text" @click="open_file(item)">打开文件</el-button>
                  <el-button-group class="button_group">
                  <el-button  style="height: 60PX;margin-top: -20px;" :disabled="!item['config'].length>0"  @click="show_config(item['config'])"  :class="item['config_class']">配置</el-button>
                  <el-button style="height: 60PX;margin-top: -20px;" :disabled="!item['translation'].length>0"  @click="show_translation(item['translation'])"  :class="item['translation_class']">转换</el-button>
                  <el-button style="height: 60PX;margin-top: -20px;" :disabled="!item['jinja2'].length>0"  @click="show_jinja2(item['jinja2'])"  :class="item['jinja2_class']">函数</el-button>
                  <el-button style="height: 60PX;margin-top: -20px;" :disabled="!item['excute'].length>0"  @click="show_excute(item['excute'])"  :class="item['excute_class']">执行</el-button>
                  </el-button-group>
              </el-card>
            </li>
        </ul>
        <el-dialog title="Translation" :visible.sync="translation_pop_able" width="1000px">
          <el-table :data="file_data" height="500"  stripe>
            <el-table-column property="type" label="类型" width="80"></el-table-column>
            <el-table-column property="before" label="转换前" width="460"></el-table-column>
            <el-table-column property="after" label="转换后" width="460"></el-table-column>
          </el-table>
        </el-dialog>
        <el-dialog title="Jinja2" :visible.sync="jinja2_pop_able" width="1000px">
          <el-table :data="file_data" height="500"  stripe>
            <el-table-column property="fun_name" label="函数名" width="200"></el-table-column>
            <el-table-column property="fun_text" label="函数体" width="800"></el-table-column>
          </el-table>
        </el-dialog>
        <el-dialog title="Excute" :visible.sync="excute_pop_able" width="1000px">
          <el-table :data="file_data" height="500"  stripe>
            <el-table-column property="cmd" label="执行命令" width="333"></el-table-column>
            <el-table-column property="parameter" label="参数" width="333"></el-table-column>
            <el-table-column property="condition" label="执行条件" width="333"></el-table-column>
          </el-table>
        </el-dialog>
        <el-dialog title="Config" :visible.sync="config_pop_able" width="1000px">
          <el-table :data="file_data" height="500"  stripe>
            <el-table-column property="parameter_class" label="参数类型" width="333"></el-table-column>
            <el-table-column property="parameter_key" label="参数键" width="333"></el-table-column>
            <el-table-column property="parameter_value" label="参数值" width="333"></el-table-column>
          </el-table>
        </el-dialog>
      </div>
  </div>
</template>

<script>
import { mapMutations} from 'vuex'
export default{
    data(){
        return{
            activeNames: [],
            translation_pop_able:false,
            jinja2_pop_able:false,
            excute_pop_able:false,
            config_pop_able:false,
            file_data:[],
            input:''
        }
    },
    name:'FileState',
    methods:{
        ...mapMutations('filestateAbout',{
          GET_NETKNIFE_DATA:'GET_NETKNIFE_DATA',
          CHOOSE_CHANGE:'CHOOSE_CHANGE',
          ROLLBACK_NETKNIFE_DATA:'ROLLBACK_NETKNIFE_DATA'
        }),
        handleChange(val) {
        console.log(val);
        },
        show_translation(data){
            this.file_data=[]
            this.translation_pop_able=true
            data.forEach(element => {
                this.file_data.push({'type':element[0],'before':element[1],'after':element[2]})
            });
        },
        show_jinja2(data){
          this.file_data=[]
          this.jinja2_pop_able=true
          let fun_dict={}
          for(let i=0;i<data.length;i++){
            if(!fun_dict.hasOwnProperty(data[i][0])){
                fun_dict[data[i][0]]=data[i][1]
              }else{
                fun_dict[data[i][0]]+=`;${data[i][1]}`
              }
          }
          Object.entries(fun_dict).forEach((item,index)=>{
            this.file_data.push({'fun_name':item[0],'fun_text':item[1]})
          })
        },
        show_excute(data){
          this.file_data=[]
          this.excute_pop_able=true
          data.forEach(element=>{
            this.file_data.push({'cmd':element[0],'parameter':element[1],'condition':element[2]})
          })
        },
        open_file(item){
          this.$bus.$emit('switch_activeIndex','open_file',item)
        },
        show_config(data){
          this.file_data=[]
          this.config_pop_able=true
          data.forEach(element => {
              this.file_data.push({'parameter_class':element[0],'parameter_key':element[1],'parameter_value':element[2]})
          });
        },
        querySearchAsync(queryString, cb) {
        let search_data=[]
        for(let i=0;i<this.netknife_data.length;i++){
          search_data.push({'value':this.netknife_data[i]['netknife'][0]})
        }
        let results=search_data
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
    computed:{
        netknife_data(){
          return this.$store.state.filestateAbout.netknife_data
        },
       
    },
    watch:{
      input(new_value,old_value){
        if(old_value!=='' && new_value===''){
            this.ROLLBACK_NETKNIFE_DATA()
        }
      }
    },
    mounted(){
      this.GET_NETKNIFE_DATA()
    }
}

</script>

<style>

li{
  list-style-type: none;
}
li:not(:first-child){
    margin-top: 8px;
} 
.button_group{
  float: right;
  margin-right: 20px;

}
.card{
  height: 60px;
}
.netknife_ul{
  margin-top: 20px;
}
</style>