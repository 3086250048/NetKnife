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
              <div style="margin-top: 15px;" >
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
import { send_post } from '@/store/tools'



export default{
  components:{Filecreate:filecreate},
  name:"FileManage",
  data(){
    return {
        base_code:`name:\npriority:\n\n\ntranslation:{\n\n\n}\n\njinja2:{\n\n\n}\n\nexcute:{\n\n}\n\n`,
        activename:'0',
        tabs:[
        ],
        tabindex:-1,
        storage_tabs:[],
        index_list:[],
       
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
              if((this.tabs.length>1)){
                localStorage.setItem('last_key',nextTab['name'])
              }
            } 
          });
        }
        this.activename = activeName;
        this.tabs = tabs.filter(tab => tab.name !== targetName);
        delete localStorage[targetName]
        if((this.tabs.length===0 && typeof(localStorage['last_key'])!=='undefined') || localStorage['last_key'] === targetName ){
          delete localStorage['last_key']
        }
       
    },
  }, 
  mounted(){
      // 向编辑页面添加新窗口
      this.$bus.$on('add',()=>{
        let newTabName = ++this.tabindex+ '';
        let tab_obj={
          name: newTabName,
          title: `空窗口`,
          code:this.base_code
        }
        console.log(tab_obj)
        this.tabs.push(tab_obj);
        this.activename = newTabName;
        console.log(tab_obj)
        localStorage.setItem(tab_obj['name'],JSON.stringify(tab_obj))
        localStorage['last_key']=newTabName
      }),
      //点击保存按钮或删除按钮时更改Tab的titile
      this.$bus.$on('change_title',(file_name)=>{
          this.tabs.forEach(tab=>{
            if(tab.name==this.activename){
              tab.title=file_name
              const ori_tab_obj=JSON.parse(localStorage[tab.name])
              ori_tab_obj['title']=file_name
              localStorage[tab.name]=JSON.stringify(ori_tab_obj)
            }
          })    
      })
      //点击删除按钮时,将编辑框中的代码重置为初始代码
      this.$bus.$on('change_code',(name,code)=>{
        this.tabs.forEach(tab=>{
            if(tab['name']===name){
              tab['code']=code
            }
        })
      })
      //将localStorage中的页面状态信息读入列表，用于被页面迭代创建
      Object.entries(localStorage).forEach(([key,value])=>{
        if(key!=='last_key' ){
          this.tabindex=Math.max(this.tabindex,parseInt(key))
          this.index_list.push(parseInt(key))
          this.storage_tabs.push(JSON.parse(value))
        }
      })
      //排序索引列表保证创建页面的顺序
      this.index_list.sort(function(a,b){
        return b-a
      })
      //判断是否是第一次打开页面
      let open_file_flag=true
      //迭代创建Tab
      this.$bus.$on('create_tabs',()=>{
        if(this.index_list.length===0){
            if(typeof(localStorage['last_key'])!=='undefined'){
              this.activename=localStorage['last_key']
            }
            //判断是否从文件状态的“打开文件”按钮跳转来,open_file_flag防止新建窗口时依然用打开文件时的文件名
            if(this.$route.params.item && open_file_flag){
               let item=this.$route.params.item 
                open_file_flag=false
                this.tabs.forEach(e=>{
                  if(e['name']===localStorage['last_key']){
                    e['title']=this.$route.params.item['config'][0]
                    send_post('/get_raw_code',{'file_name':e['title']},response=>{
                      e['code']=response.data
                      localStorage[e['name']]=JSON.stringify(e)
                    })
                    
                  }
                })
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
      //延迟1毫秒，防止子节点先于父节点加载
      setTimeout(()=>{
        this.$bus.$emit('create_tabs')
      },1)
      //当localstorage中没有数据时，删除last_key
      if(localStorage.length===0){
        this.$bus.$emit('add')
      }
  
  },
  beforeDestroy(){
      this.$bus.$off('add')
      this.$bus.$off('change_title')
      this.$bus.$off('change_code')
  }
}
</script>