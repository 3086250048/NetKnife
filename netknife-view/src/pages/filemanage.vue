<template>
  <el-container class="crud_div">
        <el-main style="margin-left: -30px;margin-top: -40px;">
            <el-tabs v-model="activename" type="card" closable  @tab-remove="remove"  >
              <el-tab-pane
              style="width: 940px;"
                v-for="(item, index) in tabs"
                :key="item.name"
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
        // activename:"first"
        activename:'0',
        tabs:[
          // {
          //   title:'窗口 0',
          //   name:'0',
          // }
        ],
        tabindex:-1
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
    },
    push_filecreate(){
      this.$router.push({
        name:'filecreate'
      })
    }

  },
  watch:{
      tabs(new_value){
        console.log(new_value)
      }
  },
  mounted(){
      if(Object.keys(localStorage.valueOf()).length <= 0){
            let tab_obj={
              title: '窗口 0',
              name: '0',
            }
            this.tabs.push(tab_obj);
            this.activename = '0';
            this.push_filecreate()
            localStorage.setItem(this.tabs[0]['title'],JSON.stringify(this.tabs[0]))
      }else{
        let newTabName=0
        Object.entries(localStorage.valueOf()).forEach(([key,value])=>{
            if(Object.keys(localStorage.valueOf()).length >=1){
               newTabName = ++this.tabindex + '';
            }else{
               newTabName = this.tabindex+'';
            }
            let tab_obj=JSON.parse(value)
            this.tabs.push(tab_obj);
            this.activename = newTabName;
            this.push_filecreate()
        })
      }
     
      this.$bus.$on('add',()=>{
        let newTabName = ++this.tabindex + '';
        let tab_obj={
          title: `窗口 ${this.tabindex}`,
          name: newTabName,
        }
        this.tabs.push(tab_obj);
        this.activename = newTabName;
        this.push_filecreate()
        localStorage.setItem(tab_obj.title,JSON.stringify(tab_obj))
      }),
      this.$bus.$on('change',(file_name)=>{
          this.tabs.forEach(tab=>{
            if(tab.name==this.activename){
              tab.title=file_name
            }
          })
      })
  },
  beforeDestroy(){
      this.$bus.$off('add')
      this.$bus.$off('change')
  }
}
</script>