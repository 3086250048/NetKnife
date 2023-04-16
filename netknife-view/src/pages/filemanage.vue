<template>
  <el-container class="crud_div">
        <el-main style="margin-left: -30px;margin-top: -40px;">
            <el-tabs v-model="activename" type="card" closable  @tab-remove="remove"  >
              <el-tab-pane
              style="width: 940px;"
                v-for="(item, index) in tabs"
                :key=index
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
export default{
  name:"FileManage",
  data(){
    return {
        activename:'0',
        tabs:[
          {
            title:'窗口 0',
            name:'0',
          }
        ],
        load_tabs:[],
        tabindex:0,
        code:''
    }
  },
  methods:{
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
        // localStorage['tabs_obj']=JSON.stringify(this.tabs)
    },
    push_filecreate(){
      this.$router.push({
        name:'filecreate',
       
      })
    }
  },
  watch:{
      tabs(new_value){
        console.log(new_value)
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
        // localStorage['tabs_obj']=JSON.stringify(this.tabs)
        this.activename = newTabName;
        this.push_filecreate()
      }),
      this.$bus.$on('change',(file_name)=>{
          this.tabs.forEach(tab=>{
            if(tab.name==this.activename){
              tab.title=file_name
            }
          })
          // localStorage['tabs_obj']=JSON.stringify(this.tabs)
      })
     this.push_filecreate()
  },
  beforeDestroy(){
      this.$bus.$off('add')
      this.$bus.$off('change')
    
  }
}
</script>