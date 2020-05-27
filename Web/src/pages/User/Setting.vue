<template>
  <!-- 暂时未排版 -->
  <div style="text-align: left;position:relative;" class="setting-box">
    <el-card class="card-box" :body-style="{ padding: '0px' }" shadow="never">
    <div style="margin-top:15px;display:inline-block">
      <div style="flex:1">
      <div style="font-size:20px;font-weight:bold;margin-left:20px;">用户信息</div>
      <div style="display:flex;text-align : left;margin-top:20px;">
        <span
          class="demonstration"
          style="vertical-align: center;margin-right:30px;margin-top:20px;color:#606266;"
        >头像</span>
        <el-avatar
          style="margin-top:10px;margin-left:10px;"
          v-bind:src='imageurl'
        ></el-avatar>
      </div>
      </div>
      <div style="flex:1">
      <div style="display:block;text-align : left;margin-top:20px;">
        <span class="demonstration" style="vertical-align: center;color:#606266;">用户名</span>
        <el-input v-model="userName" style="width:200px;" placeholder="请输入用户名"></el-input>
      </div>
      </div>
    </div>
    <div style="margin-top:50px;">
      <div style="font-size:20px;font-weight:bold;margin-left:20px;">其他设置</div>
      <div style="display:block;text-align : left;margin-top:30px;">
        <span class="demonstration" style="vertical-align: center;color:#606266;margin-right:34px;">生日</span>
        <el-date-picker v-model="birthday" type="date" placeholder="选择您的生日"></el-date-picker>
      </div>
      <div style="display:block;text-align : left;margin-top:20px;">
        <span class="demonstration" style="vertical-align: center;color:#606266;">联系电话</span>
        <el-input v-model="phoneNum" style="width:200px;" placeholder="请输入您的联系方式"></el-input>
      </div>
    </div>
      <el-button style="margin-top:40px;margin-left:20px;" type="danger" plain @click="exit()">退出登录</el-button>
      </el-card>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      logged: false,
      userName: localStorage.getItem('nickname'),
      imageurl: localStorage.getItem('imageurl'),
      birthday:"1999-05-13",
      phoneNum:""
    };
  },

  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    exit() {
      localStorage.setItem("logged", true);
      this.$router.push({
        //核心语句
        path: "/" //跳转的路径
      });
      this.$router.go(0);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.demonstration {
  margin-right: 20px;
  margin-left: 20px;
}
.setting-box{
  right:20px;
}

.card-box{
  padding:20px 20px 60px 30px;
}

@media screen and (max-width: 992px) {
    .setting-box{
      right:0px;
      margin-bottom: 20px;
    }

    .card-box{
      padding:20px 20px 20px 20px;
    }
  }

</style>
