<template>
  <div>
    <el-container class="main-container">
      <el-aside width="200px" style="margin-left:0px;height: 600px;position:fixed;" class="hidden-xs-only">
        <div style="margin-right:30px;margin-top:40px;">
          <router-link :to="{ path: '/publish'}" target="_blank">
          <el-button type="primary" icon="el-icon-edit" style="width:100%">写游记</el-button>
          </router-link>
        </div>
        <div style="margin-right:30px;margin-top:25px;">
          <el-input placeholder="输入国家/城市" style="margin-bottom:10px;" v-model="filterText"></el-input>
          <el-tree @node-click="handleNodeClick" class="filter-tree" :data="data" :props="defaultProps"
            :filter-node-method="filterNode" :highlight-current="highlight-current" ref="tree"></el-tree>
        </div>
      </el-aside>
      <el-main class="article-area">
        <el-input placeholder="输入国家/城市" style="margin-bottom:10px;width:90%;" class="hidden-sm-and-up input-xs" v-model="filterText"></el-input>
        <div style="max-width:800px;">
          <div v-for="(story,index) in stories" :key="story" v-if="index<pagenum && index>=pagenums">
            <router-link :to="{ path: '/article', query : {article_id : story.article_id}}" target="_blank">
              <el-card :body-style="{ padding: '0px' }" style="margin:20px;text-decoration:none;" class="card-margin-xs">
                <el-container>
                  <el-aside style="background-size: cover;position: relative;min-height:170px;" class="float-image"
                    :style="{backgroundImage:'url(' + story.image + ')'}"></el-aside>
                  <el-main style="text-align:left;margin-left:20px;margin-right:20px;min-width:200px" class="hidden-xs-only">
                    <p style="margin-bottom:10px;margin-top:15px;font-size:18px;font-weight:bold;display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 1;overflow: hidden;text-decoration: none!important;">{{story.title}}</p>
                    <p style="color:#606266;font-size:14px;display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 3;overflow: hidden;text-decoration: none!important;">{{story.introduce}}</p>
                  </el-main>
                </el-container>
                <div style="padding: 14px;" class="hidden-sm-and-up">
                  <p style="margin-bottom:10px;margin-top:15px;font-size:18px;font-weight:bold;display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 1;overflow: hidden;text-decoration: none!important;">{{story.title}}</p>
                  <p style="color:#606266;font-size:14px;display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 3;overflow: hidden;text-decoration: none!important;">{{story.introduce}}</p>
                </div>

              </el-card>
            </router-link>
          </div>
          <div style="position: relative;top: 10px;">
            <el-pagination @current-change="handleCurrentChange" layout="prev, pager, next" :page-size="pageSize"
              :total="stories.length"></el-pagination>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import axios from "axios";
  export default {
    name: "Community",
    methods: {
      handleNodeClick(data, node, vuecomponent) {
        this.currentPage = 1;
        this.pagenum = 3,
          this.pagenums = 0
        if (data.id > 8) {
          console.log("data:", data, "\n");
          var that = this;
          that.stories = [];
          console.log(data.label);
          axios
            .get("https://ly.inftime.cn/weapp/articlelist", {
              params: {
                place: data.label
              }
            })
            .then(function(response) {
              console.log(response);
              var obj = response.data;
              console.log(that.stories);
              for (var i = 0; i < obj.length; i++) {
                that.stories.push(obj[i]);
              }
              console.log(that.stories);
            })
            .catch(function(error) {
              console.log(error);
            });
        } else if (data.id == 1) {
          var that = this
          that.stories = [];
          axios
            .get("https://ly.inftime.cn/weapp/articlelist")
            .then(function(response) {
              console.log(response);
              var obj = response.data;
              console.log(that.stories);
              for (var i = 0; i < obj.length; i++) {
                that.stories.push(obj[i]);
              }
              console.log(that.stories);
            })
            .catch(function(error) {
              console.log(error);
            })
        }
      },
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      /*toarticle(story) {
        this.$router.push({
          //核心语句
          path: "/planview" ,
          query: {
            article_id :st.id  //跳转的路径
        }
        })
      },*/
      handleCurrentChange(val) {
        // 获取当前页
        this.currentPage = val;
        console.log(this.currentPage);
        this.pagenum = this.currentPage * this.pageSize;
        this.pagenums = (this.currentPage - 1) * this.pageSize;
      },
      openFullScreen() {
        const loading = this.$loading({
          lock: true,
          text: '请稍等',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.1)'
        });
        return loading;
      },
      closeFullScreen(loading) {
        loading.close();
      }
    },
    watch: {
      filterText(val) {
        this.$refs.tree.filter(val);
      }
    },
    data() {
      return {
        loading: true,
        article_id: 0,
        // 当前页码
        currentPage: 1,
        // 每页数量
        pageSize: 3,
        pagenum: 3,
        pagenums: 0,
        filterText: "",
        radio: "1",
        checkList: ["攻略", "游记", "景点介绍"],
        stories: [],
        data: [{
            id: 1,
            label: "全部"
          },
          {
            id: 2,
            label: "中国大陆",
            children: [{
                id: 4,
                label: "上海"
              },
              {
                id: 4,
                label: "北京"
              },
              {
                id: 4,
                label: "天津"
              },
              {
                id: 4,
                label: "湖南",
                children: [{
                    id: 4,
                    label: "长沙"
                  },
                  {
                    id: 4,
                    label: "岳阳"
                  }
                ]
              }
            ]
          },
          {
            id: 3,
            label: "港澳台地区",
            children: [{
                id: 7,
                label: "日本"
              },
              {
                id: 8,
                label: "韩国"
              },
              {
                id: 8,
                label: "新加坡"
              }
            ]
          },
          {
            id: 4,
            label: "亚洲",
            children: [{
                id: 7,
                label: "意大利",
                children: [{
                    id: 7,
                    label: "罗马"
                  },
                  {
                    id: 8,
                    label: "威尼斯"
                  }
                ]
              },
              {
                id: 8,
                label: "英国"
              },
              {
                id: 8,
                label: "法国"
              },
              {
                id: 8,
                label: "西班牙"
              }
            ]
          },
          {
            id: 5,
            label: "北美洲",
            children: []
          },
          {
            id: 6,
            label: "欧洲",
            children: []
          },
          {
            id: 7,
            label: "澳洲",
            children: []
          },
          {
            id: 8,
            label: "非洲",
            children: []
          }
        ],
        defaultProps: {
          children: "children",
          label: "label"
        }
      };
    },
    mounted() {
      this.openFullScreen();
      var that = this;
      that.data[1].children = [];
      that.data[2].children = [];
      that.data[3].children = [];
      that.data[4].children = [];
      that.stories = [];
      axios
        .get("https://ly.inftime.cn/weapp/articlelist")
        .then(function(response) {
          console.log(response);
          var obj = response.data;
          console.log(that.stories);
          for (var i = 0; i < obj.length; i++) {
            that.stories.push(obj[i]);
          }
          console.log(that.stories);

        })
        .catch(function(error) {
          console.log(error);
          that.closeFullScreen(that.openFullScreen());
        })
      var obj
      if (that.$store.state.data == '') {
        axios
          .get("https://ly.inftime.cn/weapp/regions")
          .then(function(response) {
            console.log(response);
            obj = response.data;
            that.$store.commit('setdata', obj)
            console.log(that.$store.state.data)
            for (var i = 0; i < obj.length; i++) {
              if (obj[i].url == "中国大陆") {
                let child = {
                  id: 9,
                  label: obj[i].name
                };
                that.data[1].children.push(child);
              } else if (obj[i].url == "港澳台地区") {
                let child = {
                  id: 10,
                  label: obj[i].name
                };
                that.data[2].children.push(child);
              } else if (obj[i].url == "亚洲") {
                let child = {
                  id: 11,
                  label: obj[i].name
                };
                that.data[3].children.push(child);
              } else if (obj[i].url == "北美洲") {
                let child = {
                  id: 12,
                  label: obj[i].name
                };
                that.data[4].children.push(child);
              } else if (obj[i].url == "欧洲") {
                let child = {
                  id: 13,
                  label: obj[i].name
                };
                that.data[5].children.push(child);
              } else if (obj[i].url == "澳洲") {
                let child = {
                  id: 14,
                  label: obj[i].name
                };
                that.data[6].children.push(child);
              } else if (obj[i].url == "非洲") {
                let child = {
                  id: 15,
                  label: obj[i].name
                };
                that.data[7].children.push(child);
              }
            }
            that.closeFullScreen(that.openFullScreen())
          })
          .catch(function(error) {
            console.log(error);
          })
      } else {
        obj = that.$store.state.data
        for (var i = 0; i < obj.length; i++) {
          if (obj[i].url == "中国大陆") {
            let child = {
              id: 9,
              label: obj[i].name
            };
            that.data[1].children.push(child);
          } else if (obj[i].url == "港澳台地区") {
            let child = {
              id: 10,
              label: obj[i].name
            };
            that.data[2].children.push(child);
          } else if (obj[i].url == "亚洲") {
            let child = {
              id: 11,
              label: obj[i].name
            };
            that.data[3].children.push(child);
          } else if (obj[i].url == "北美洲") {
            let child = {
              id: 12,
              label: obj[i].name
            };
            that.data[4].children.push(child);
          } else if (obj[i].url == "欧洲") {
            let child = {
              id: 13,
              label: obj[i].name
            };
            that.data[5].children.push(child);
          } else if (obj[i].url == "澳洲") {
            let child = {
              id: 14,
              label: obj[i].name
            };
            that.data[6].children.push(child);
          } else if (obj[i].url == "非洲") {
            let child = {
              id: 15,
              label: obj[i].name
            };
            that.data[7].children.push(child);
          }
        }
        that.closeFullScreen(that.openFullScreen())
      }
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

  .router-link-active {
    text-decoration: none !important;
  }

  .float-image {
    width: 300px;
  }

  .article-area{
    margin-left:180px;
  }

  .main-container{
    margin-left:100px;margin-right:50px;margin-top:20px;
  }

  @media screen and (max-width: 768px) {
    .float-image {
      width: 100%!important;
    }

      .article-area{
      margin-left:0px;
    }

      .main-container{
      margin-left:0px;margin-right:0px;margin-top:0px;
    }

    .card-margin-xs{
      margin:20px 10px!important;
    }

    .input-xs{
      width: 95%!important;
    }

  }

  a {
    text-decoration: none;
  }
</style>
