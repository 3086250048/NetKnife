<template>
  <el-container class="crud_div">
        <el-main style="margin-left: -30px;margin-top: -40px;">
            <el-tabs v-model="activename" type="card" editable  @tab-remove="remove" >
              <el-tab-pane
              style="width: 940px;"
                v-for="(item, index) in tabs"
                :key='item.name'
                :label="item.title"
                :name="item.name"
                
              >
              <div style="margin-top: 15px;">
                  <Filecreate :title="item.title" :name="item.name" :code="item.code" ></Filecreate>
              </div>
              </el-tab-pane>
            </el-tabs>
        </el-main>
    </el-container>
</template>

<script>

import { mapMutations} from 'vuex'
import filecreate from '@/pages/filecreate.vue'
export default{
  components:{Filecreate:filecreate},
  name:"FileManage",
  data(){
    return {
        base_code:`name:\npriority:\n\n\ntranslation:{\n\n\n}\n\njinja2:{\n\n\n}\n\nexcute:{\n\n}\n\n`,
        activename:'0',
        tabs:[
          {
            title:'空窗口',
            name:'0',
            code:`name:\npriority:\n\n\ntranslation:{\n\n\n}\n\njinja2:{\n\n\n}\n\nexcute:{\n\n}\n\n`
          }
        ],
        tabindex:0,
        storage_tabs:[]
    }
  },
  methods:{
    ...mapMutations('filemanageAbout',{SET_TITLE:'SET_TITLE'}),
    cons(){
      console.log(this.activename)
    },
    remove(targetName){
      console.log('=====targetName')
      console.log(targetName)
        let tabs = this.tabs;
        if (tabs.length===1){
          this.$message({
            showClose: true,
            message: '已经是最后一个页面',
            type: 'warning'
          });
          return
        }
        let activeName = this.activename;
        if (activeName === targetName) {
          tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
              let nextTab = tabs[index + 1] || tabs[index - 1];
              if (nextTab) {
                activeName = nextTab.name;
              }
            }
          });
        }
        this.activename = activeName;
        this.tabs = tabs.filter(tab => tab.name !== targetName);
        delete localStorage[targetName]
    },
  }, 
  mounted(){
      this.$bus.$on('add',()=>{
        let newTabName = ++this.tabindex+ '';
        let tab_obj={
          name: newTabName,
          title: `空窗口`,
          code:this.base_code
        }
        this.tabs.push(tab_obj);
        this.activename = newTabName;
        localStorage.setItem(tab_obj['name'],JSON.stringify(tab_obj))
      }),
      this.$bus.$on('change',(file_name)=>{
          this.tabs.forEach(tab=>{
            if(tab.name==this.activename){
              tab.title=file_name
              const ori_tab_obj=JSON.parse(localStorage[tab.name])
              ori_tab_obj['title']=file_name
              localStorage[tab.name]=JSON.stringify(ori_tab_obj)
            }
          })    
      })
      Object.entries(localStorage).forEach(([key,value])=>{
        this.tabindex=Math.max(this.tabindex,parseInt(key))
        if(JSON.parse(value)['name']==='0'){
          this.tabs=[]
        }
        this.storage_tabs.push(JSON.parse(value))
      })
      this.$bus.$on('create_tabs',()=>{
        if(this.storage_tabs.length>=1){
          const tab= this.storage_tabs.pop()
          console.log(tab)
          let newTabName =tab['name']
          let tab_obj={
            name: newTabName,
            title:tab['title'],
            code:tab['code']
          }
          this.tabs.push(tab_obj);
          this.activename = newTabName;
        }
       
      })
      
      this.$bus.$emit('create_tabs')
  },
  beforeDestroy(){
      this.$bus.$off('add')
      this.$bus.$off('change')
    
  }
}
</script>