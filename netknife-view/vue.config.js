const { defineConfig } = require('@vue/cli-service')
const path = require('path')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false,  //关闭语法检查
  assetsDir:process.env.NODE_ENV === 'production'? '../static' : 'static',
  publicPath: process.env.NODE_ENV === 'production'? './' : '/',
  outputDir: path.resolve(__dirname,'../templates'),
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "~@/assets/scss/_variable.scss";` //引入全局变量   
      }
    }
  }
})

// module.exports={
//   css: {
//     loaderOptions: {
//       sass: {
//         additionalData: `@import "~@/assets/scss/_variable.scss";` //引入全局变量   
//       }
//     }
//   }

// }

