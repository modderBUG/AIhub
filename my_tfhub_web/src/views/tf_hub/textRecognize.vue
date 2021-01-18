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

      <el-tooltip class="item" effect="dark" content="请选择图像类别" placement="right">
        <el-radio-group v-model="type_label">
          <el-radio-button label="normal">普通识别</el-radio-button>
          <el-radio-button label="written">手写体识别</el-radio-button>
          <el-radio-button label="plus">特殊识别</el-radio-button>
        </el-radio-group>
      </el-tooltip>

    </div>

    <div class="block">
      <!-- <el-image :src="src?src:base_api+'/img_test'">
        <div slot="placeholder" class="image-slot">
          加载中<span class="dot">...</span>
        </div>
      </el-image> -->

      <el-input
        type="textarea"
        :autosize="{ minRows: 5, maxRows: 10}"
        placeholder="请输入内容"
        v-model="target_data">
      </el-input>


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
  txt_recognize
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
      type_label: 'normal',
      target_data:''
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
      const param = this.type_label
      this.$message.info('正在执行... 请稍后')
      txt_recognize(this.formdata, param).then(res => {
        let token_list =  res.words_result
        for (var i = 0; i < token_list.length; i++) {
         this.target_data = this.target_data +"\n" +token_list[i].words
        }
        this.$message.success('识别成功！')
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
