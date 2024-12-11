<template>
  <div class="content">
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-33"
      >
        <chart-card
          :chart-data="dailySalesChart.data"
          :chart-options="dailySalesChart.options"
          :chart-type="'Line'"
          data-background-color="blue"
        >
          <template slot="content">
            <h4 class="title">每天都要学数据库</h4>
            <p class="category">
              <span class="text-success"
                ><i class="fas fa-long-arrow-alt-up"></i>
                10%
              </span>
              日均进步，今天你写数据库了吗
            </p>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>access_time</md-icon>
              马上更新
            </div>
          </template>
        </chart-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-33"
      >
        <chart-card
          :key="chartKey0"
          :chart-data="goods.data"
          :chart-options="goods.options"
          :chart-responsive-options="
            goods.responsiveOptions
          "
          :chart-type="'Bar'"
          data-background-color="red"
        >
          <template slot="content">
            <h4 class="title">物资类别一览表</h4>
            <p class="category">每种物资都闪闪发光</p>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>access_time</md-icon>
              更新于{{ updateTime1 }}
            </div>
          </template>
        </chart-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-33"
      >
        <chart-card
          :key="chartKey1"
          :chart-data="leaseApplicationsChart.data"
          :chart-options="leaseApplicationsChart.options"
          :chart-type="'Line'"
          data-background-color="green"
        >
          <template slot="content">
            <h4 class="title">租赁申请分布图</h4>
            <p class="category">看看客户最偏爱哪个时间</p>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>access_time</md-icon>
              更新于{{ updateTime2 }}
            </div>
          </template>
        </chart-card>
      </div>
      <div
        class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25"
      >
        <stats-card data-background-color="green">
          <template slot="header">
            <md-icon>store</md-icon>
          </template>

          <template slot="content">
            <p class="category">库中物资</p>
            <h3 class="title">
              {{ data.goodsNumOfStorage }}<small>件</small>
            </h3>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>date_range</md-icon>
              已稳健运营{{ days }}天
            </div>
          </template>
        </stats-card>
      </div>
      <div
        class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25"
      >
        <stats-card data-background-color="orange">
          <template slot="header">
            <md-icon>content_copy</md-icon>
          </template>

          <template slot="content">
            <p class="category">租赁中物资</p>
            <h3 class="title">
              {{ data.goodsNumOfLease }}
              <small>件</small>
            </h3>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>local_offer</md-icon>
              累计服务客户{{ data.leaseApplicationNum }}人次
            </div>
          </template>
        </stats-card>
      </div>
      <div
        class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25"
      >
        <stats-card
          :data-background-color="
            data.goodsNumOfDamage > 0 ? 'red' : 'green'
          "
        >
          <template slot="header">
            <md-icon>info_outline</md-icon>
          </template>

          <template slot="content">
            <p class="category">损坏物资</p>
            <h3 class="title">
              {{ data.goodsNumOfDamage }}<small>件</small>
            </h3>
          </template>

          <template slot="footer">
            <div v-if="data.goodsNumOfDamage > 0">
              <md-icon class="text-danger">warning</md-icon>
              请立刻开展物资维护工作！
            </div>
            <div v-else class="stats">
              <md-icon class="text-success"
                >thumb_up</md-icon
              >
              你们的工作值得肯定!
            </div>
          </template>
        </stats-card>
      </div>
      <div
        class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25"
      >
        <stats-card data-background-color="blue">
          <template slot="header">
            <i class="fab fa-twitter"></i>
          </template>

          <template slot="content">
            <p class="category">成员数量</p>
            <h3 class="title">
              {{ data.userNum }}<small>人</small>
            </h3>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon class="text-danger"
                >diversity_1</md-icon
              >
              我们的队伍更加壮大！
            </div>
          </template>
        </stats-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <Managers />
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <Tasks />
      </div>
    </div>
  </div>
</template>

<script>
import { StatsCard, ChartCard } from "@/components";
import Tasks from "./Tasks.vue";
import Managers from "./Managers.vue";
export default {
  async mounted() {
    await this.init();
  },
  components: {
    StatsCard,
    ChartCard,
    Tasks,
    Managers,
  },
  data() {
    return {
      chartKey0: 0,
      chartKey1: 0,
      dailySalesChart: {
        data: {
          labels: ["M", "T", "W", "T", "F", "S", "S"],
          series: [[4, 7, 5, 6, 10, 5, 20]],
        },
        options: {
          lineSmooth: this.$Chartist.Interpolation.cardinal(
            {
              tension: 0,
            }
          ),
          low: 0,
          high: 25, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0,
          },
        },
      },
      leaseApplicationsChart: {
        data: {
          labels: [
            "0时",
            "3时",
            "6时",
            "9时",
            "12时",
            "15时",
            "18时",
            "21时",
          ],
          series: [],
        },

        options: {
          lineSmooth: this.$Chartist.Interpolation.cardinal(
            {
              tension: 0,
            }
          ),
          low: 0,
          high: 1000, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0,
          },
        },
      },
      goods: {
        data: {
          labels: ["A", "B", "C", "D"],
          series: [[1, 2, 3, 4]],
        },
        options: {
          axisX: {
            showGrid: true,
          },
          low: 0,
          high: 10,
          chartPadding: {
            top: 0,
            right: 5,
            bottom: 0,
            left: 0,
          },
        },
        responsiveOptions: [
          [
            "screen and (max-width: 640px)",
            {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc: function (value) {
                  return value[0];
                },
              },
            },
          ],
        ],
      },
      days: 114514,
      data: {
        goodsNumOfStorage: 65536,
        goodsNumOfLease: 32767,
        days: 114514,
        leaseApplicationNum: 6666,
        goodsNumOfDamage: 0,
        userNum: 123,
      },
      updateTime1: null,
      updateTime2: null,
    };
  },
  methods: {
    async init() {
      await this.getStatisticalData();
      await this.getGoodsCategory();
      await this.getLeaseApplicationsTime();
    },
    async getStatisticalData() {
      console.log("getStatisticalData");
      let req = {
        action: "getStatisticalData",
      };
      console.log("req", req);
      let res = await this.$Backend(req);
      if (res && res.result === "success") {
        this.data = res.data;
      }
    },
    async getGoodsCategory() {
      console.log("getCategoryNum");
      let req = {
        action: "getCategoryNum",
      };
      let res = await this.$Backend(req);
      if (res && res.result === "success") {
        console.log("getCategoryNum success");
        this.goods.data.labels = res.categories;
        this.goods.data.series = [res.nums];
        const maxNum = Math.max(...res.nums);
        this.goods.options.high = maxNum + 10;
        this.chartKey0 += 1;
        this.updateTime1 = this.getTime();
        console.log("this.goods", this.goods);
      }
    },
    async getLeaseApplicationsTime() {
      console.log("getLeaseApplicationsTime");
      let req = {
        action: "getLeaseApplicationsTime",
      };
      let res = await this.$Backend(req);
      if (res && res.result === "success") {
        console.log("getLeaseApplicationsTime success");
        this.leaseApplicationsChart.data.series = [
          res.nums,
        ];
        const maxNum = Math.max(...res.nums);
        this.leaseApplicationsChart.options.high =
          maxNum + 5;
        this.chartKey1 += 1;
        this.updateTime2 = this.getTime();
        console.log(
          "this.leaseApplicationsTime",
          this.leaseApplicationsTime
        );
      }
    },
    getTime() {
      const now = new Date();
      const hours = String(now.getHours()).padStart(2, "0");
      const minutes = String(now.getMinutes()).padStart(
        2,
        "0"
      );
      const seconds = String(now.getSeconds()).padStart(
        2,
        "0"
      );

      const timeString = `${hours}:${minutes}:${seconds}`;

      return timeString;
    },
  },
};
</script>
