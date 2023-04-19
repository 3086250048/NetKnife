<template>
  <div>
    <ul>
        <li v-for="item,index in netknife_data" :key="index">
          <el-card class="box-card card">
              <el-tag >文件名:{{ item['config'][0].length>30?item['config'][0].slice(0,30)+'...':item['config'][0] }}</el-tag>
              &nbsp;
              <el-tag type="danger" >优先级:{{ item['config'][1]}}</el-tag>
              <el-button style="float: right; padding: 3px 0" type="text">打开文件</el-button>
              <el-button-group class="button_group">
              <el-button size="small" :disabled="item['translation'].length>0?false:true"  @click="show_translation(item['translation'])"  :class="item['translation_class']">Translation</el-button>
              <el-button size="small" :disabled="item['jinja2'].length>0?false:true"  @click="show_jinja2(item['jinja2'])"  :class="item['jinja2_class']">Jinja2</el-button>
              <el-button size="small" :disabled="item['excute'].length>0?false:true"  @click="show_excute(item['excute'])"  :class="item['excute_class']">Excute</el-button>
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
        <el-table-column property="cmd" label="执行命令" width="1000"></el-table-column>
      </el-table>
    </el-dialog>
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
            file_data:[]
        }
    },
    name:'FileState',
    methods:{
        ...mapMutations('filestateAbout',{GET_NETKNIFE_DATA:'GET_NETKNIFE_DATA'}),
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
          let before_key=data[0][0]
          let after_key=''
          let value=''
          data.forEach(element => {
                console.log(element)
                after_key=element[0]
                value+=`\n${element[1]}`
                if(before_key!==after_key){
                  this.file_data.push({'fun_name':before_key,'fun_text':value})
                  value=''
                }
                before_key=element[0]
            });
        },
        show_excute(data){
          this.file_data=[]
          this.excute_pop_able=true
          data.forEach(element=>{
            this.file_data.push({'cmd':element})
          })
        }
    },
    computed:{
        netknife_data(){
          return this.$store.state.filestateAbout.netknife_data
        },
       
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
</style>