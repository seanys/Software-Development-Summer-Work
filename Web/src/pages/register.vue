<template>
  <div class="fullscreen-bg login-bg">
    <div style="background-color:white;max-width:300px; border-radius: 1px;" class="login-box">
      <p></p>
      <div style="font-size:20px;font-weight:bold;margin-bottom: 0px;line-height: 30px;font-family: 'pingfang SC';">账户注册</div>
      <p></p>
      <el-form class="login-form" status-icon :rules="loginRules" ref="loginForm" :model="loginForm" label-width="65px">
        <el-form-item prop="username" label="账号">
          <el-input @keyup.enter.native="handleRegister" v-model="loginForm.username" auto-complete="off" placeholder="请输入用户名">
            <!-- <i slot="prefix" class="icon-yonghu"></i> -->
          </el-input>
        </el-form-item>
        <el-form-item prop="password" label="密码">
          <el-input @keyup.enter.native="handleRegister" :type="passwordType" v-model="loginForm.password" auto-complete="off"
            placeholder="请输入密码">
            <i class="el-icon-view el-input__icon" :style="fontstyle" slot="suffix" @click="showPassword"></i>
            <!-- <i slot="prefix" class="icon-mima"></i> -->
          </el-input>
        </el-form-item>
        <el-form-item prop="nickname" label="昵称">
          <el-input @keyup.enter.native="handleRegister" v-model="loginForm.nickname" auto-complete="off"
            placeholder="请输入昵称">
            <!-- <i slot="prefix" class="icon-mima"></i> -->
          </el-input>
        </el-form-item>
        <el-form-item prop="photo" label="头像">
          <el-upload
             class="avatar-uploader"
             :show-file-list="false"
             :action="actionPath"
             :on-success="handleAvatarSuccess"
             :data="uptoken"
             :before-upload="beforeAvatarUpload">
             <img v-if="imageUrl" :src="imageUrl" class="avatar">
             <i v-else class="el-icon-plus avatar-uploader-icon"></i>
       </el-upload>
        </el-form-item>
         <el-form-item prop="verifycode" label="验证码">
              <el-input v-model="loginForm.verifycode" placeholder="请输入验证码" class="identifyinput"></el-input>
              <div class="identifybox">
                <div @click="refreshCode">
                  <s-identify :identifyCode="identifyCode"></s-identify>
                </div>
                <el-button @click="refreshCode" type="text" class="textbtn">看不清，换一张</el-button>
              </div>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click.native="sendPost()" @keyup.enter.native="sendPost" style="float:center;width: 100%;margin-top:10px;height: 46px;">确定</el-button>
      <!-- <el-link :underline="false" type="primary" style="margin-top:40px;">切换其他方式登录</el-link>
      <el-divider></el-divider>
      <div style="width:100%;display:flex;text-align:center;margin-top:20px;font-size:15px;">
        <el-link :underline="false" style="flex:1;">立即注册</el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link :underline="false" style="flex:1;">忘记账号</el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link :underline="false" style="flex:1;">忘记密码</el-link>
      </div>-->
    </div>
  </div>
</template>





<script>
  import SIdentify from "@/pages/Login/identity.vue";
  import axios from "axios";
  export default {
    name: "userlogin",
    data() {
      // 用户名自定义验证规则
      const validateUsername = (rule, value, callback) => {
        if (2<value.length&& value.length<7) {
          console.log('user', value)
          callback()
        } else {
          callback(new Error("用户名长度必须在3~6位之间"))
        }
      };
      const validatePassword = (rule, value, callback) => {
        if (2<value.length && value.length<7) {
          console.log('password', value)
          callback()
        } else {
          callback(new Error("密码长度必须在3~6之间"))
        }
      };
      // 验证码自定义验证规则
      const validateVerifycode = (rule, value, callback) => {
        if (value === "") {
          callback(new Error("请输入验证码"));
        } else if (value !== this.identifyCode) {
          console.log("validateVerifycode:", value);
          callback(new Error("验证码不正确!"));
        } else {
          callback();
        }
      };
      return {
        uptoken: {
          token: '',
          key: ""
        },
        actionPath:'https://upload.qiniup.com',
        fontstyle: {},
        imageUrl: '',
        loginForm: {
          username: "",
          password: "",
          verifycode: ""
        },
        checked: false,
        logged: true,
        identifyCodes: "1234567890",
        identifyCode: "",
        loginRules: {
          // 绑定在form表单中的验证规则
          username: [{
            required: true,
            trigger: "blur",
            validator: validateUsername
          }],
          password: [{
              required: true,
              trigger: "blur",
              validator: validatePassword
            }
            // { min: 6, message: "密码长度最少为6位", trigger: "blur" }
          ],
          nickname:[{
              required: true,
              trigger: "blur",
          }],
          verifycode: [{
            required: true,
            trigger: "blur",
            validator: validateVerifycode
          }]
        },
        passwordType: "password"
      };
    },
    components: {
      SIdentify
    },
    created() {
      this.keyupSubmit()
      let that=this;
      axios.post(
					'https://ly.inftime.cn/weapp/uploadfile')
					 .then(function(response) {
						console.log(response.data)
            that.uptoken.token = response.data
            console.log(that.uptoken.token)
      })
    },
    mounted() {
      // 验证码初始化
      this.identifyCode = "";
      this.makeCode(this.identifyCodes, 4);
      this.scroll = new Bscroll(this.$refs.wrapper, {
        mouseWheel: true,
        click: true,
        tap: true
      });

    },
    props:{
    },
    methods: {
      keyupSubmit() {
        document.onkeydown = e => {
          let _key = window.event.keyCode;
          if (_key === 13) {
            this.sendPost()
          }
        }
      },
       handleAvatarSuccess(res, file) {
         this.imageUrl = 'http://pw5w2wzrm.bkt.clouddn.com/'+res.key;
         console.log(this.imageUrl)
      },
      beforeAvatarUpload(file) {
        this.uptoken.key = file.name;
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;
        if (!isJPG) {
          that.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          that.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      // 通过改变input的type使密码可见
      showPassword() {
        this.fontstyle === "" ?
          (this.fontstyle = "color: red") :
          (this.fontstyle = ""); // 改变密码可见按钮颜色
        this.passwordType === "" ?
          (this.passwordType = "password") :
          (this.passwordType = "");
      },
      // 点击登录按钮
      handleRegister() {
        this.$router.push("/");
        this.$store.dispatch("userLogin", true);
        localStorage.setItem("Flag", "isLogin");
        //登录成功后跳转到指定页面
      },
      // 生成随机数
      randomNum(min, max) {
        return Math.floor(Math.random() * (max - min) + min);
      },
      // 切换验证码
      refreshCode() {
        this.identifyCode = "";
        this.makeCode(this.identifyCodes, 4);
      },
      // 生成四位随机验证码
      makeCode(o, l) {
        for (let i = 0; i < l; i++) {
          this.identifyCode += this.identifyCodes[
            this.randomNum(0, this.identifyCodes.length)
          ];
        }
        console.log(this.identifyCode);
      },
      sendPost() {
        let that=this;
        var obj;
        var params = new URLSearchParams();
        params.append("user_id", that.loginForm.username);
        params.append("password", that.loginForm.password);
        params.append("nickname", that.loginForm.nickname);
        params.append("imageurl", that.imageUrl);
        axios
          .post("https://ly.inftime.cn/weapp/register", params, {})
          .then(function(response) {
            obj = response.data;
            console.log(obj)
            if (obj == "success") {
              that.$notify({
                title: '注册成功',
                message: '即将跳转到登录界面',
                type: 'success',
                position: 'top-right',
                offset: 80
              });
              that.$router.push({
                path: "/login"
              });
            }
            else {
               that.$notify({
                title: '账号已存在',
                message: '请您重新填写',
                type: 'error',
                position: 'top-right',
                offset: 80
              });
            }
          })
          .catch(function(error) {
            console.log(error);
          });
      }
    }
  };
</script>

<style scoped>
  .identifybox {
    display: flex;
    justify-content: space-between;
    margin-top: 7px;
  }

  .iconstyle {
    color: #e9eef3;
  }

  .fullscreen-bg {
    background-position: 50% 50%;
    background-size: cover;
    bottom: 0;
    right: 0;
    position: fixed;
    position: absolute\9;
    width: 100%\9;
    height: 100%\9;
    overflow: hidden;
    left: 0;
    top: 0;
  }
  .el-main {
    background-color: rgb(255, 255, 255);
    text-align: center;
    line-height: 50px;
    margin-top: 100px;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar {
    width: 50px;
    height: 50px;
  }

   .login-bg {
      background-image: url("https://ly.inftime.cn/login.png");
      overflow: auto;
    }


      .login-box{
       margin: auto;margin-top: 170px;
       padding: 40px 60px;
    }



  @media screen and (max-width: 768px) {
    .login-bg {
      background-image: none;
      overflow: auto;
    }
    .login-box{
       margin: auto;margin-top: 80px;
       padding: 40px 30px;
    }
    }
</style>
