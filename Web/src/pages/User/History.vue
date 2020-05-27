<template>
  <div style="display:block!important;">
    <div class="history-box" >
        <div v-for="(story,index) in stories" :key="story" >
            <el-card v-if="index<pagenum && index>=pagenums" :body-style="{ padding: '0px' }" style="margin:20px;">
              <el-container>
                <el-aside style="background-size: cover;position: relative;min-height:170px;" :style="{backgroundImage:'url(' + story.photo + ')'}">
                </el-aside>
                <el-main style="text-align:left;margin-left:20px;margin-right:20px;min-width:200px">
                    <p style="margin-bottom:10px;margin-top:15px;font-size:18px;font-weight:bold;display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 1;overflow: hidden;">{{story.title}}</p>
                    <p style="color:#606266;font-size:14px;display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 3;overflow: hidden;">{{story.detail}}</p>
                </el-main>
              </el-container>
            </el-card>
        </div>
        <div style="position: relative;top: 10px;">
          <el-pagination @current-change="handleCurrentChange" layout="prev, pager, next" :page-size = pageSize :total="stories.length"></el-pagination>
        </div>
    </div>
  </div>
</template>
<script>
import axios from "axios"
export default {
  name: "History",
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    handleCurrentChange (val) {
      // 获取当前页
      this.currentPage = val
      console.log(this.currentPage)
      this.pagenum = this.currentPage * this.pageSize
      this.pagenums = (this.currentPage - 1) * this.pageSize
    },
    filterNode(value, data) {
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    }
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    }
  },
  mounted:function(){
    let that=this;
    axios.get('https://ly.inftime.cn/weapp/routecollection', {
      params: {
          action:3,
          user_id:localStorage.getItem('user_id')
        },
      headers:{
        'Content-Type':'application/x-www-form-urlencoded'
      }
      })
      .then(function (response) {
        let history=response.data.data.history;
        console.log(history)
        for(let i=0;i<history.length;i++){
          let story={
            title:history[i].title,
            detail:history[i].introduce,
            photo:history[i].normal_picture,
          };
          that.stories.push(story);
        }
      })
      .catch(function (error) {
        console.log(error);
      })
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 3,
      pagenum: 3,
      pagenums: 0,
      filterText: "",
      radio: "1",
      checkList: ["线路", "文章"],
      stories: []
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.history-box{
  max-width:800px;position:relative;top:-20px;
}

  @media screen and (max-width: 992px) {
    .history-box{
      max-width:none;position:relative;top:-20px;
    }
  }
</style>
