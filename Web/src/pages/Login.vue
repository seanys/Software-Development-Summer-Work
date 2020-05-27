<template>
  <div class="fullscreen-bg login-bg">
    <div style="background-color:white;max-width:300px;border-radius: 1px;padding: 40px 60px;" class="login-box">
      <p></p>
      <div style="font-size:28px;font-weight:bold;margin-bottom: 25px;line-height: 40px;font-family: 'pingfang SC';">账户登录</div>
      <p></p>
      <el-form class="login-form" status-icon :rules="loginRules" ref="loginForm" :model="loginForm">
        <el-form-item prop="username">
          <el-input @keyup.enter.native="handleLogin" v-model="loginForm.username" auto-complete="off" placeholder="请输入用户名-2018">
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input @keyup.enter.native="handleLogin" :type="passwordType" v-model="loginForm.password" auto-complete="off"
            placeholder="请输入密码-test">
            <i class="el-icon-view el-input__icon" :style="fontstyle" slot="suffix" @click="showPassword"></i>
          </el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click.native="sendPost()" @keyup.enter.native="sendPost" style="float:center;width: 100%;margin-top:10px;height: 46px;">登录</el-button>
      <el-link :underline="false" type="primary" style="margin-top:40px;">切换其他方式登录</el-link>
      <el-divider></el-divider>
      <div style="width:100%;display:flex;text-align:center;margin-top:20px;font-size:15px;">
        <el-link :underline="false" style="flex:1;">
          <router-link to='/register'>立即注册</router-link>
        </el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link :underline="false" style="flex:1;">忘记账号</el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link :underline="false" style="flex:1;">忘记密码</el-link>
      </div>
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
        // if (value == '2018') {
        //   console.log('user', value)
        //   callback()
        // } else {
        //   callback(new Error('请输入正确的用户名'))
        // }
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
        fontstyle: {},
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
              message: "请输入密码",
              trigger: "blur"
            }
            // { min: 6, message: "密码长度最少为6位", trigger: "blur" }
          ],
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
    props: [],
    methods: {
      keyupSubmit() {
        document.onkeydown = e => {
          let _key = window.event.keyCode;
          if (_key === 13) {
            this.sendPost()
          }
        }
      },
      showPassword() {
        this.fontstyle === "" ?
          (this.fontstyle = "color: red") :
          (this.fontstyle = ""); // 改变密码可见按钮颜色
        this.passwordType === "" ?
          (this.passwordType = "password") :
          (this.passwordType = "");
      },
      // 点击登录按钮
      handleLogin() {
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
        var obj;
        var params = new URLSearchParams();
        let that = this;
        params.append("user_id", this.loginForm.username);
        params.append("password", this.loginForm.password);
        axios
          .post("https://ly.inftime.cn/weapp/Login", params, {})
          .then(function(response) {
            console.log(response);
            obj = response.data;
            console.log(obj);
            localStorage.setItem("user_id", obj.user_id);
            localStorage.setItem("nickname", obj.nickname);
            console.log(localStorage.getItem("nickname"));
            localStorage.setItem("imageurl", obj.imageurl);
            console.log(localStorage.getItem("imageurl"));
            localStorage.setItem("logged", false);
            console.log(localStorage.getItem("logged"));
            if (obj == "password error") {
              that.$notify({
                title: '账号或密码错误',
                message: '请您重新核实您填写的内容',
                type: 'error',
                position: 'top-right',
                offset: 80
              });
            } else if (localStorage.logged == "false") {
              that.$notify({
                title: '登录成功',
                message: 'ok',
                type: 'success',
                position: 'top-right',
                offset: 100
              });
              that.$router.push({
                path: "/"
              });
              that.$router.go(0);
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

  a {
    text-decoration: none;
  }


  .router-link-active {
    text-decoration: none;
  }

  .login-bg {
    background-image: url("https://ly.inftime.cn/login.png");
    overflow: auto;
  }


  .login-box {
    margin: auto;
    margin-top: 170px;
  }



  @media screen and (max-width: 768px) {
    .login-bg {
      background-image: none;
      overflow: auto;
    }

    .login-box {
      margin: auto;
      margin-top: 100px;
    }
  }
</style>
