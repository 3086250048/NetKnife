<template>
  <el-container class="crud_div">
        <el-main style="margin-left: -30px;margin-top: -40px;">
            <el-tabs v-model="activename" type="card" closable  @tab-remove="remove"  >
              <el-tab-pane
              style="width: 940px;"
                v-for="(item, index) in tabs"
                :key='item.name'
                :label="item.title"
                :name="item.name"
              >
              <div style="margin-top: 15px;">
                <router-view></router-view>
              </div>
              </el-tab-pane>
            </el-tabs>
        </el-main>
    </el-container>
</template>

<script>

import { mapMutations,mapActions } from 'vuex'
export default{
  name:"FileManage",
  data(){
    return {
        activename:'0',
        tabs:[
          {
            title:'窗口 0',
            name:'0',
            // component:'filecreate'
          }
        ],
        load_tabs:[],
        tabindex:0,
        code:''
    }
  },
  methods:{
    ...mapMutations('filemanageAbout',{SET_TITLE:'SET_TITLE'}),
    remove(targetName){
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
    },
    push_filecreate(name,title){
      this.$router.push({
        name:`filecreate${name}`,
        params:{
          title:title
        }
      })
    }
  }, 
  mounted(){
      this.$bus.$on('add',()=>{
        let newTabName = ++this.tabindex + '';
        let tab_obj={
          title: `窗口 ${this.tabindex}`,
          name: newTabName,
        }
        this.tabs.push(tab_obj);
        this.activename = newTabName;
        console.log('=============')
        console.log(tab_obj['title'])
        this.push_filecreate(tab_obj['name'],tab_obj['title'])
      }),
      this.$bus.$on('change',(file_name)=>{
          this.tabs.forEach(tab=>{
            if(tab.name==this.activename){
              tab.title=file_name
            }
          })
          this.$bus.$emit('change_title',file_name)

      })
      this.tabs.forEach(item=>{//动态添加路由的方法找到了，明天这里开始
        this.$router.addRoute('filemanage',{path:`filecreate0`,component:()=>import(`@/pages/filecreate.vue`),name:'filecreate0'});
      })
    console.log(this.$router)
      this.push_filecreate(this.tabs[0]['name'],'filecreate0')
  },
  beforeDestroy(){
      this.$bus.$off('add')
      this.$bus.$off('change')
    
  }
}
</script>