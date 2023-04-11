<template>
     <div>
      <codemirror
    ref="mycode"   
    v-model="curCode"       
    :options="cmOptions"  
    class="code">        
</codemirror>
  </div>
</template>

<script>
import { codemirror } from 'vue-codemirror';
import 'codemirror/theme/liquibyte.css';//导入选中的theme主题,与初始化theme配置一致
import 'codemirror/addon/hint/show-hint.css';//导入自动提示核心样式

import 'codemirror/mode/sql/sql.js';//导入使用的语言语法定义文件，初始化mode配置一致
import 'codemirror/addon/edit/matchbrackets.js';
import 'codemirror/addon/hint/show-hint.js';//导入自动提示核心文件
import 'codemirror/addon/hint/sql-hint.js';//

export default{
    name:'FileManage',
    data(){
      return {
              curCode:'',
        cmOptions:{
          value:'',//编辑器的起始值。可以是字符串，也可以是文档对象。
          mode:"text/x-hive",//第一个将模式名称映射到它们的构造函数，第二个将MIME类型映射到模式规范。
          theme: "liquibyte",//编辑器样式的主题       
          indentWithTabs: true,//在缩进时，是否tabSize 应该用N个制表符替换前N *个空格。默认值为false。       
          smartIndent: true,//是否使用模式提供的上下文相关缩进（或者只是缩进与之前的行相同）。默认为true。         
          lineNumbers: true,//是否在编辑器左侧显示行号。        
          matchBrackets : true,//括号匹配         
          autofocus: true,//可用于使CodeMirror将焦点集中在初始化上  
          extraKeys: {"Ctrl-Space": "autocomplete"},//按键配置 
          hintOptions: {tables: {          
              users: ["name", "score", "birthDate"],      
              countries: ["name", "population", "size"] 
              }
            } 
        }
      } 
    },
    components:{ 
      codemirror
    },
    methods:{
        
    },
    watch:{
      curCode(newvalue){
        console.log(newvalue)
      }
    },
    mounted(){
        this.editor = CodeMirror.fromTextArea(this.$refs.editor, {
      lineNumbers: true,
      theme: 'material',
      mode: 'javascript'
    })
    }
}

</script>
<style scoped>
.CodeMirror {
  height: 100%;
  font-size: 16px;
}
</style>