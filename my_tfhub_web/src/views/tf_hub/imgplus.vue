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
  img_plus
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
      countClick: 0
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
      this.$message.info('正在执行... 请稍后')
      img_plus(this.formdata).then(res => {
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
