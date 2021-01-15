<template>

  <div class="container">

    <div class="upload-item">
      <el-upload
        ref="upload02"
        class="avatar-uploader"
        :http-request="uploadFile"
        :action="base_api+'/post_style'"
        :show-file-list="false"
        :auto-upload="true"
        :multiple="false"
        :before-upload="beforeStyleUpload"
        :on-change="handleStyleAccept"
      >
        <img v-if="post_style" :src="post_style" class="avatar">
        <i v-else class="el-icon-plus avatar-uploader-icon" />
      </el-upload>
    </div>

    <div>
      <el-button type="danger" @click="cleanAll">清空</el-button>
      <el-button type="primary" @click="submitImg">转换</el-button>
    </div>

    <div style="padding: 10px 10px 10px 10px;">

      <el-tooltip class="item" effect="dark" content="请选择风格" placement="right">
        <el-radio-group v-model="style_option">
          <!--
           cartoon：卡通画风格
           pencil：铅笔风格
           color_pencil：彩色铅笔画风格
           warm：彩色糖块油画风格
           wave：神奈川冲浪里油画风格
           lavender：薰衣草油画风格
           mononoke：奇异油画风格
           scream：呐喊油画风格
           gothic：哥特油画风格
           -->
          <el-radio-button label="cartoon">卡通画</el-radio-button>
          <el-radio-button label="pencil">铅笔画</el-radio-button>
          <el-radio-button label="color_pencil">彩色铅笔画</el-radio-button>
          <el-radio-button label="warm">彩色糖块油画</el-radio-button>
          <el-radio-button label="wave">神奈川冲浪里油画</el-radio-button>
        </el-radio-group>
      </el-tooltip>

      <el-tooltip class="item" effect="dark" content="请选择风格" placement="right">
        <el-radio-group v-model="style_option">
          <el-radio-button label="lavender">薰衣草油画</el-radio-button>
          <el-radio-button label="mononoke">奇异油</el-radio-button>
          <el-radio-button label="scream">呐喊油画</el-radio-button>
          <el-radio-button label="gothic">哥特油画</el-radio-button>
        </el-radio-group>
      </el-tooltip>

    </div>

    <div class="block">
      <el-image :src="src?src:base_api+'/img_test'">
        <div slot="placeholder" class="image-slot">
          加载中<span class="dot">...</span>
        </div>
      </el-image>
    </div>

    <!-- <el-button type="danger" id="ceshi" @click="okClickHnadle">测试</el-button> -->

  </div>

</template>

<script>
// import imageConversion from 'image-conversion'
import {
  compress,
  compressAccurately
} from 'image-conversion'
import {
  imgTest,
  img_transtyle
} from '../../api/abilitys.js'
export default {

  data() {
    return {
      base_api: process.env.VUE_APP_BASE_API,
      src: process.env.VUE_APP_BASE_API + '/img_test',
      imageUrl: '',
      post_style: '',
      post_content: '',
      filelist: '',
      formdata: '',
      countClick: 0,
      style_option: 'cartoon'
    }
  },
  mounted() {
    this.formdata = new FormData()
  },
  created() {

  },
  methods: {
    compressAccurately,
    compress,

    execFun() {
      setInterval(() => {
        // this.execFun()
        this.countClick += 1
        console.log(this.countClick)
      }, 1000)
    },

    cleanAll() {
      this.$router.go(0)
    },
    initData() {
      imgTest().then(res => {
        this.src = URL.createObjectURL(res)
        console.log(URL.createObjectURL(res))
      })
    },
    uploadFile(file) {
      this.formdata.append('file', file.file)
    },
    handleContentAccept(file, filelist) {
      this.post_content = URL.createObjectURL(file.raw)
    },
    handleStyleAccept(file, filelist) {
      this.post_style = URL.createObjectURL(file.raw)
    },
    submitImg() {
      const param = this.style_option
      this.$message.info('正在执行... 请稍后')
      img_transtyle(this.formdata, param).then(res => {
        this.src = 'data:image/jpeg;base64,' + res

        this.$message.success('生成完成')
      }).catch(err => {
        this.$message.error('服务器内存溢出了。估计你的图片太大了')
        console.log(err)
      })
    },
    beforeStyleUpload(file) {
      console.log(file)
      console.log(file.size)
      new Promise((resolve, reject) => {
        const isLt2M = file.size / 1024 / 1024 < 0.2 // 判定图片大小是否小于4MB
        if (isLt2M) {
          resolve(file)
        }
        const old = file.size
        compressAccurately(file, 100).then(res => { // console.log(res)
          console.log(old, res.size)
          resolve(res)
        })
      })
    },

    beforeContentUpload(file) {
      console.log(file)
      console.log(file.size)
      new Promise((resolve, reject) => {
        const isLt2M = file.size / 1024 / 1024 < 0.5 // 判定图片大小是否小于4MB
        if (isLt2M) {
          resolve(file)
        }
        const old = file.size // 压缩到400KB,这里的400就是要压缩的大小,可自定义
        compressAccurately(file, 500).then(res => { // console.log(res)
          console.log(old, res.size)
          resolve(res)
        })
      })
    }

  }
}
</script>

<style>
  .container {
    margin: 20px 10% 10% 10%;
    text-align: center;
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
