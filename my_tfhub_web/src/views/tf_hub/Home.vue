<template>
  <div>
    <vueCanvasNest :config="{color:'106,90,205', zIndex: -3, count: 120}" />
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      @select="handleSelect"
    >
      <el-menu-item index="1">主页</el-menu-item>
      <el-submenu index="2">
        <template slot="title">图片AI演示</template>
        <el-menu-item index="2-1">风格迁移</el-menu-item>
        <el-menu-item index="2-2">图像放大</el-menu-item>
        <el-menu-item index="2-3">风格转换</el-menu-item>
        <el-menu-item index="2-4">图片上色</el-menu-item>
        <el-menu-item index="2-5">图片清晰化</el-menu-item>
        <el-menu-item index="2-6">图像转二次元</el-menu-item>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title">其他AI演示</template>
        <el-menu-item index="3-1">文字识别</el-menu-item>
        <el-menu-item index="3-2" disabled>文字转语音</el-menu-item>
        <el-menu-item index="3-3" disabled>图像搜索</el-menu-item>
        <el-menu-item index="3-4" disabled>图像快速切割</el-menu-item>
        <el-menu-item index="3-5" disabled>图像搜索</el-menu-item>
        <el-menu-item index="3-6" disabled>图像搜索</el-menu-item>
      </el-submenu>
      <el-menu-item index="4" disabled>留言板</el-menu-item>
    </el-menu>

    <div v-if="activeIndex==1">
      <!-- 主页 -->
      <div v-html="markdown_test" />
    </div>

    <div v-if="activeIndex==2">
      <!-- 分页内容 -->
      <comp1 v-if="flags[0]==1" />
      <comp2 v-if="flags[1]==1" />
      <comp3 v-if="flags[2]==1" />
      <comp4 v-if="flags[3]==1" />
      <comp5 v-if="flags[4]==1" />
      <comp6 v-if="flags[5]==1" />
    </div>

    <div v-if="activeIndex==3">
      <!-- 主页 -->
      <div v-html="markdown_test" />
      <comp7 v-if="flags[6]==1" />
    </div>

  </div>

</template>

<script>
import comp1 from './stylization.vue'
import comp2 from './imgplus.vue'
import comp3 from './imgTranStyle.vue'
import comp4 from './imgColorful.vue'
import comp5 from './imgDefinition.vue'
import comp6 from './imgWaifu.vue'
import comp7 from './textRecognize.vue'
import {
  test_connection
} from '../../api/abilitys.js'
import vueCanvasNest from 'vue-canvas-nest'
export default {
  components: {
    vueCanvasNest,
    comp1,
    comp2,
    comp3,
    comp4,
    comp5,
    comp6,
    comp7

  },
  data() {
    return {
      activeIndex: '1',
      flags: [1, 0, 0, 0, 0, 0, 0],
      markdown_test: '<h1>Welcome to modderbug.github.io</h1>'

    }
  },
  mounted() {
    this.initData()
  },
  methods: {
    initData() {
      test_connection().then(res => {
        this.$message.success(res)
        // console.log(res)
      })
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath)
      this.activeIndex = keyPath[0]
      console.log('activeIndex:', this.activeIndex)
      this.flags = [0, 0, 0, 0, 0, 0, 0]
      if (key === '2-1') {
        this.flags[0] = 1
      }
      if (key === '2-2') {
        this.flags[1] = 1
      }
      if (key === '2-3') {
        this.flags[2] = 1
      }
      if (key === '2-4') {
        this.flags[3] = 1
      }
      if (key === '2-5') {
        this.flags[4] = 1
      }
      if (key === '2-6') {
        this.flags[5] = 1
      }

      if (key === '3-1') {
        this.flags[6] = 1
      }
    }

  }
}
</script>

<style >

  .container {
    margin: 20px 10% 10% 10%;
  }

  .upload-form {}

  .block {
    margin: 20px 20% 20px 20%;
  }

  .upload-item {
    margin: 20px 10% 20px 10%;
    display: inline-block;
  }

  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }

  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>
