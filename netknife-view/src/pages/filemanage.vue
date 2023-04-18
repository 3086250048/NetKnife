<template>
  <el-container class="crud_div">
        <el-main style="margin-left: -30px;margin-top: -40px;">
            <el-tabs v-model="activename" type="card" closable @tab-remove="remove" @tab-click="record_index" >
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
          // {
          //   title:'空窗口',
          //   name:'0',
          //   code:`name:\npriority:\n\n\ntranslation:{\n\n\n}\n\njinja2:{\n\n\n}\n\nexcute:{\n\n}\n\n`
          // }
        ],
        tabindex:-1,
        storage_tabs:[],
        index_list:[]
    }
  },
  methods:{
    ...mapMutations('filemanageAbout',{SET_TITLE:'SET_TITLE'}),
    record_index(){
      localStorage.setItem('last_key',this.activename)
    },
    remove(targetName){
        let tabs = this.tabs;
        console.log(this.tabs.length)
        if (tabs.length<=1){
          this.$router.push({
            name:'pageempty'
          })
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
        if(this.tabs.length===0 && typeof(localStorage['last_key'])!=='undefined'){
          delete localStorage['last_key']
        }
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
        if(parseInt(key)>=0 && parseInt(key) <=9 ){
          this.tabindex=Math.max(this.tabindex,parseInt(key))
          this.index_list.push(parseInt(key))
          this.storage_tabs.push(JSON.parse(value))
        }else{

        }
      })
      console.log(this.storage_tabs.length)
      this.index_list.sort(function(a,b){
        return b-a
      })
      this.$bus.$on('create_tabs',()=>{
        if(this.index_list.length===0){
          if(typeof(localStorage['last_key'])!=='undefined'){
          this.activename=localStorage['last_key']
          }
           return
          }
          const tab= JSON.parse(localStorage[this.index_list.pop()+''])
          let newTabName =tab['name']
          let tab_obj={
            name: newTabName,
            title:tab['title'],
            code:tab['code']
          }
          this.tabs.push(tab_obj);
          this.activename = newTabName;
      })
      setTimeout(()=>{
        this.$bus.$emit('create_tabs')
      },1)
      if(localStorage.length===0){
        this.$bus.$emit('add')
      }
      
  },
  beforeDestroy(){
      this.$bus.$off('add')
      this.$bus.$off('change')
    
  }
}
</script>