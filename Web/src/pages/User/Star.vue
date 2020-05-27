<template>
  <div>
      <div style="max-width:800px;position:relative;position:relative;top:-20px;">
        <div v-for="(story,index) in stories" :key="story" >
          <router-link
            v-if="index<pagenum && index>=pagenums"
              :to="{ path: '/article', query : {article_id : story.article_id}}"
              target="_blank"
            >
            <el-card :body-style="{ padding: '0px' }" style="margin:20px;">
              <el-container>
                <el-aside style="background-size: cover;position: relative;min-height:170px;" :style="{backgroundImage:'url(' + story.image + ')'}">
                </el-aside>
                <el-main style="text-align:left;margin-left:20px;margin-right:20px;min-width:200px">
                    <p style="margin-bottom:10px;margin-top:15px;font-size:18px;font-weight:bold;display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 1;overflow: hidden;">{{story.title}}</p>
                    <p style="color:#606266;font-size:14px;display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 3;overflow: hidden;">{{story.introduce}}</p>
                </el-main>
              </el-container>
            </el-card>
            </router-link>
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
  name: "App",
  mounted(){
    var that=this
    that.stories=[]
    axios.get('https://ly.inftime.cn/weapp/Articlecollection',{
    params: {
      user_id : localStorage.getItem('user_id')
    }})
    .then(function (response) {
    
    console.log(response)
    var obj=response.data
    if(obj=="无数据"){
       that.$notify({
                title: '您还没有收藏',
                message: '请您快去阅读文章吧',
                type: 'warning',
                position: 'top-right',
                offset: 80
              });
    }
    else{
    console.log(that.stories)
    for(var i=0;i<obj.length;i++){
      that.stories.push(obj[i])
    }
    }
    console.log(that.stories)
    })
    .catch(function (error) {
    console.log(error)
    })
  },
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
  data() {
    return {
      currentPage: 1,
// 每页数量
      pageSize: 3,
      pagenum: 3,
      pagenums: 0,
      filterText: "",
      radio: "1",
      checkList: ["线路", "文章"],
      stories: [
        {
          article_id: 0 ,
          place: '' ,
          title: "辞职后的第一场旅行，我又来到了新西兰",
          introduce: "世界那么大，一生这么短。小时候，是麻麻带我周游各地；长大了，是时候该我带麻麻看看更广阔的世界了。 🌟先来美图镇楼🌟 花花世界，没看过的风景还有那么多，能让人想一去再去的一定有着某种超凡的“魔力”…新西兰，就是这么个wonderland～ 作为我最心...",
          image:
            "https://b1-q.mafengwo.net/s11/M00/37/E8/wKgBEFqSyD2AOxg3AATbP0ICVV824.jpeg?imageMogr2%2Fthumbnail%2F1360x%2Fstrip%2Fquality%2F90"
        },
      ]
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

.router-link-active {
  text-decoration: none !important;
}

a {
  text-decoration: none;
}

.clearfix:after {
  clear: both;
}
</style>
