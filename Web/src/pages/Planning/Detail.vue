<template>
  <div>
    <el-container>
      <el-dialog title="交通方式详情" :visible.sync="dialogVisible" width="50%" append-to-body>
        <!--append-to-body 嵌套对话框-->
        <span v-html="dialogText"></span>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
        </span>
      </el-dialog>
      <el-main style="height:100%;">
        <el-button v-if="false" type="primary" @click="exportData()">导出<i class="el-icon-upload el-icon--right"></i></el-button>
        <el-table :data="this.$store.state.points[day]">
          <el-table-column type='expand' fixed>
            <template slot-scope="scope">
              <el-form label-position="left">
                <el-form-item>
                  <div v-if="getPriceData(scope.row)[2]!=0">
                    <label class="label">{{getPriceData(scope.row)[2]}}</label>
                    <span>{{getPriceData(scope.row)[3]}}</span>
                    <br>
                  </div>
                  <div v-if="getPriceData(scope.row)[0]!=''">
                    <label class="label">交通方式</label>
                    <span style="display:inline-block;width: 90px;">{{getTransportType(scope.row.transfer)}}</span>
                    <el-link style="margin-top:-2px;display:inline-block;" type="primary" :underline="false" @click="getTransferDetail(scope.row.transfer)">查看详情</el-link>
                    <br>
                    <label class="label">{{getPriceData(scope.row)[0]}}</label>
                    <span>{{getPriceData(scope.row)[1]}} 元</span>
                    <br>
                    <label class="label">{{getDistanceData(scope.row.transfer)[0]}}</label>
                    <span>{{getDistanceData(scope.row.transfer)[1]}} 公里</span>
                    <br>
                    <label class="label">耗时</label>
                    <span>{{getTimeCost(scope.row.transfer)}}</span>
                    <br>
                  </div>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column prop="detail.name" label="名称" fixed width='200px'></el-table-column>
          <el-table-column label="地址" fixed width='300px'>
            <template slot-scope="scope">
              <span>{{cityaddress(scope.row.detail)}}</span>
            </template>
          </el-table-column>
          <el-table-column label="标签">
            <template slot-scope="scope">
              <el-tag>{{scope.row.detail.type.split(';')[0]}}</el-tag>
              <el-tag>{{scope.row.detail.type.split(';')[scope.row.detail.type.split(';').length-1]}}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import {
    isNullOrUndefined
  } from 'util';
  import {
    close
  } from 'fs';
  import MapContainer from './City/MapContainer';
  import {
    clearInterval
  } from 'timers';
  export default {
    name: 'Detail',
    data() {
      return {
        logged: false,
        dialogVisible: false,
        dialogText: '',
      }
    },
    props: ['day'],
    methods: {
      getTransferDetail(transfer) {
        this.dialogText = '';
        switch (transfer.type) {
          case 'bus':
            {
              for (let i = 0; i < transfer.plan.plans[0].segments.length; i++) {
                this.dialogText +=
                  '<p style="text-align:left;margin-bottom: 10px; line-height: 1.75em;display:inline-block;width: 380px;">';
                this.dialogText += transfer.plan.plans[0].segments[i].instruction +
                  '</p><p style="text-align:right;margin-bottom: 10px; line-height: 1.75em;display:inline-block;width: 120px;">';
                if (transfer.plan.plans[0].segments[i].time >= 3600)
                  this.dialogText += parseInt(transfer.plan.plans[0].segments[i].time / 3600) + ' 小时 ';
                if (transfer.plan.plans[0].segments[i].time >= 60)
                  this.dialogText += parseInt((transfer.plan.plans[0].segments[i].time % 3600) / 60) + ' 分钟';
                this.dialogText += '</p><br>';
              }
              break;
            }
          case 'driving':
            {
              for (let i = 0; i < transfer.plan.routes[0].steps.length; i++) {
                this.dialogText +=
                  '<p style="text-align:left;margin-bottom: 10px; line-height: 1.75em;display:inline-block;width: 380px;">';
                this.dialogText += transfer.plan.routes[0].steps[i].instruction +
                  '</p><p style="text-align:right;margin-bottom: 10px; line-height: 1.75em;display:inline-block;width: 120px;">';
                if (transfer.plan.routes[0].steps[i].time >= 3600)
                  this.dialogText += parseInt(transfer.plan.routes[0].steps[i].time / 3600) + ' 小时 ';
                if (transfer.plan.routes[0].steps[i].time >= 60)
                  this.dialogText += parseInt((transfer.plan.routes[0].steps[i].time % 3600) / 60) + ' 分钟';
                this.dialogText += '</p><br>';
              }
              break;
            }
        }
        this.dialogVisible = true;
      },
      cityaddress(detail) {
        return detail.cityname + ' / ' + detail.address;
      },
      getTransportType(transfer) {
        switch (transfer.type) {
          case 'bus':
            return '公交';
            break;
          case 'driving':
            return '驾车';
            break;
        }
      },
      getPriceData(point) { //0交通费用描述 1交通费 2其他费用描述 3景点门票/餐饮人均消费/酒店
        let priceData = ['', '', 0, ''];
        if (!isNullOrUndefined(point.transfer)) {
          switch (point.transfer.type) {
            case 'bus':
              {
                priceData[0] = '票价';
                priceData[1] = point.transfer.plan.plans[0].cost;
                break;
              }
            case 'driving':
              {
                priceData[0] = '路费';
                priceData[1] = point.transfer.plan.routes[0].tolls;
                break;
              }
          }
        }
        if (!isNullOrUndefined(point.detail.deep_type)) {
          switch (point.detail.deep_type) {
            case 'SCENIC':
              {
                priceData[2] = '门票价格';
                if (parseFloat(point.detail.scenic.price) >= 0) {
                  priceData[3] = point.detail.scenic.price + '元';
                } else {
                  priceData[3] = point.detail.scenic.price;
                }
                break;
              }
            case 'DINING':
              {
                priceData[2] = '人均消费';
                priceData[3] = point.detail.dining.cost + " 元";
                break;
              }
            case 'HOTEL':
              {
                priceData[2] = '最低房价';
                priceData[3] = point.detail.hotel.lowest_price + " 元";
                break;
              }
          }
        } else {
          priceData[2] = 0;
        }
        return priceData;
      },
      getDistanceData(transfer) {
        let data = [];
        switch (transfer.type) {
          case 'bus':
            {
              data[0] = '步行距离';
              data[1] = (transfer.plan.plans[0].walking_distance / 1000).toFixed(1);
              break;
            }
          case 'driving':
            {
              data[0] = '距离';
              data[1] = (transfer.plan.routes[0].distance / 1000).toFixed(1);
              break;
            }
        }
        return data;
      },
      getTimeCost(transfer) {
        let s = '';
        let plan;
        switch (transfer.type) {
          case 'bus':
            plan = transfer.plan.plans[0];
            break;
          case 'driving':
            plan = transfer.plan.routes[0];
            break;
        }
        if (plan.time >= 3600)
          s += parseInt(plan.time / 3600) + ' 小时 ';
        s += parseInt((plan.time % 3600) / 60) + ' 分钟';
        return s;
      },
      exportData() {
        alert('请将以下代码复制给开发者:) \n' + JSON.stringify(this.$store.getters.exportData));
        console.log(JSON.stringify(this.$store.getters.exportData));
      }
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .label {
    display: inline-block;
    width: 90px;
    color: #99a9bf;
  }
</style>
