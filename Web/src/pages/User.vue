<template>
  <div>
    <el-container class="setting-container-box">
      <el-aside width="200px" style="margin-left:20px;margin-right:20px;position:fixed;" class="hidden-sm-and-down">
        <el-card style="margin-top:20px;padding:0" :body-style="{ padding: '0px' }" shadow="never">
          <el-menu default-active="1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" router="true"
            style="border:none;">
            <el-menu-item index="1" route="/user/star">
              <i class="el-icon-star-on"></i>
              <span slot="title">收藏</span>
            </el-menu-item>
            <el-menu-item index="2" route="/user/history">
              <i class="el-icon-s-order"></i>
              <span slot="title">历史</span>
            </el-menu-item>
            <el-menu-item index="3" route="/user/setting">
              <i class="el-icon-setting"></i>
              <span slot="title">设置</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-aside>

      <el-main class="setting-main-box">

        <router-view style="main-root"></router-view>
                <div style="text-align: center;width: 100%;position: relative;top:0px" class="hidden-md-and-up">
          <div style="display: flex;margin: auto;width: 80%;border: 1px solid #EBEEF5;border-radius: 2px;box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);line-height: 44px;">
          <el-link type="primary" @click="toDetail('star')"  style="flex: 1;">收藏</el-link>
          <el-link type="primary" @click="toDetail('history')" style="flex: 1;">历史</el-link>
          <el-link type="primary" @click="toDetail('setting')" style="flex: 1;">设置</el-link>
        </div>

        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  export default {
    name: 'User',
    data() {
      const item = {
        date: '2016-05-02',
        name: '羊山今天运动了吗',
        address: '上海市普陀区金沙江路 1518 弄'
      }
      return {
        activeIndex: 1,
        activeIndex2: 1,
        rightIndex: 1,
        visible: false,
        logged: false,
        tableData: Array(20).fill(item)
      }
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath)
      },
      toDetail(page) {
        if(page=="star"){
          this.$router.push({path:'/user/star'})
        }else if(page=="history"){
          this.$router.push({path:'/user/history'})
        }else{
          this.$router.push({path:'/user/setting'})
        }
         // window.open("http://ly.inftime.cn//#/community");
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .setting-container-box {
    margin-left: 100px;
    margin-right: 50px;
    margin-top: 20px;
  }

  .setting-main-box {
    margin-left: 300px;
  }

  @media screen and (max-width: 992px) {
    .setting-container-box {
      margin-left: 10px;
      margin-right: 10px;
      margin-top: 20px;
    }

    .setting-main-box {
      margin-left: 0px;
    }
    .main-root{
      margin-top:40px
    }
  }
</style>
