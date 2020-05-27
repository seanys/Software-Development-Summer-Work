<template>
  <div id="app" style="height: 100%;">
    <el-menu :router="true" class="el-menu-demo" mode="horizontal" style="position: fixed;right:0px;left:0px;z-index:3000;top: 0;">
      <img @click="navTravel" class="hidden-xs-only" src="https://inftime.cn/travel_around.png" style="width:50px;height:50px;float: left;margin-right:20px;margin-left:20px;margin-top: 5px;" />
      <el-menu-item index="/travel">首页</el-menu-item>
      <el-menu-item index="/planning">规划</el-menu-item>
      <el-menu-item index="/community">社区</el-menu-item>
      <el-menu-item index="/recommend">推荐</el-menu-item>
      <el-menu-item style="float:right" v-if="logged">
        <el-button type="primary" plain @click="toLogin()">登录</el-button>
      </el-menu-item>
      <!--     <el-submenu class="hidden-sm-and-up" trigger="click">
        <template slot="title">功能</template>
        <el-menu-item index="/travel">首页</el-menu-item>
        <el-menu-item index="/planning">规划</el-menu-item>
        <el-menu-item index="/community">社区</el-menu-item>
        <el-menu-item index="/recommend">推荐</el-menu-item>
      </el-submenu> -->
      <el-menu-item index="/user" style="float:right;display:flex" v-if="!logged">
        <span style="margin-right:10px;margin-top:3px;" class="hidden-xs-only">{{nickname}}</span>
        <el-avatar style="margin-top:10px;" v-bind:src="imageurl"></el-avatar>
      </el-menu-item>
    </el-menu>
    <div style="height:60px;"></div>
    <router-view style="margin-top: 0;height: 100%;min-height: auto;" />
  </div>
</template>

<script>
  export default {
    name: "App",
    data() {
      return {
        imageurl: "",
        nickname: "",
        activeIndex: 1,
        activeIndex2: 1,
        visible: false,
        logged: true,
        form: {
          name: "",
          password: "",
          region: "",
          date1: "",
          date2: "",
          delivery: false,
          type: [],
          resource: "",
          desc: ""
        }
      };
    },
    created: function() {
      if (localStorage.getItem("logged") == "false") {
        this.logged = false;
        this.imageurl = localStorage.getItem("imageurl");
        this.nickname = localStorage.getItem("nickname");
      } else {
        this.logged = true;
      }
    },
    methods: {
      init() {
        this.logged = localStorage.getItem("logged");
        this.imageurl = localStorage.getItem("imageurl");
        this.nickname = localStorage.getItem("nickname");
        console.log(this.logged); //获取传入的参数
        console.log(this.imageurl);
        console.log(this.nickname);
      },
      navTravel() {
        this.$router.push("/");
      },
      toLogin() {
        this.$router.push("/login");
      }
    }
  };
</script>

<style>
  #app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
</style>
