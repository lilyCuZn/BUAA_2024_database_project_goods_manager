<template>
  <div>
    <div style="text-align: center" v-if="isLoading">
      <md-progress-spinner
        :md-diameter="100"
        :md-stroke="10"
        md-mode="indeterminate"
      ></md-progress-spinner>
    </div>
    <div v-if="!isLoading">
      <md-table
        v-for="(item, index) in maintainRecords"
        :key="index"
      >
        <md-table-row>
          <md-table-cell
            style="
              text-align: center;
              font-family: '楷体';
              font-size: large;
            "
          >
            <div style="letter-spacing: 2px">
              维护记录编号：<span class="text-info">{{
                item.id
              }}</span
              >，
              <span class="text-success">{{
                item.createdTime
              }}</span>
              由
              <span class="text-info">{{
                item.applicant.name
              }}</span>
              发起的
              <span class="text-danger">维护</span>
              记录，状态为
              <span class="text-danger">{{
                item.status
              }}</span>
              <span
                v-if="
                  item.status === '已完成' ||
                  item.status === '拒绝'
                "
                >，完结时间为&nbsp;<span
                  class="text-success"
                  >{{ item.completedTime }}</span
                ></span
              >
            </div>
          </md-table-cell>
          <div style="text-align: right">
            <md-button
              class="md-just-icon md-simple md-primary"
              @click="toggleDetail(item)"
            >
              <md-icon v-if="focusedItem !== item"
                >unfold_more</md-icon
              >
              <md-icon v-else>unfold_less</md-icon>
              <md-tooltip
                md-direction="top"
                v-if="focusedItem !== item"
                >展开</md-tooltip
              >
              <md-tooltip md-direction="top" v-else
                >折叠</md-tooltip
              >
            </md-button>
          </div>
        </md-table-row>
        <div class="md-layout" v-if="focusedItem === item">
          <div class="md-layout-item md-size-100">
            <md-field>
              <label>申请记录编号</label>
              <md-input
                v-model="item.applicationId"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-size-100">
            <md-table v-model="paginatedGoods" md-card>
              <md-table-toolbar>
                <div class="md-toolbar-section-start">
                  <h1 class="md-title">维护物资</h1>
                </div>
                <md-field
                  md-clearable
                  class="md-toolbar-section-end"
                >
                  <md-input
                    placeholder="根据类型搜索"
                    v-model="search"
                    @input="searchOnTable"
                  />
                </md-field>
              </md-table-toolbar>
              <md-table-toolbar>
                <h1 class="md-title">物资</h1>
              </md-table-toolbar>

              <md-table-row
                slot="md-table-row"
                slot-scope="{ item }"
              >
                <md-table-cell md-label="物资编号">{{
                  item.id
                }}</md-table-cell>
                <md-table-cell md-label="采购订单编号">{{
                  item.purchaseId
                }}</md-table-cell>
                <md-table-cell md-label="物资类别">{{
                  item.category
                }}</md-table-cell>
                <md-table-cell md-label="物资状态">{{
                  item.status
                }}</md-table-cell>
                <md-table-cell
                  md-label="维护"
                  v-if="item.status === '维护中'"
                >
                  <md-button
                    class="md-just-icon md-success"
                    @click="repairGoods(item.id)"
                  >
                    <md-icon>sentiment_satisfied</md-icon>
                    <md-tooltip md-direction="top"
                      >成功维护</md-tooltip
                    >
                  </md-button>
                  <md-button
                    class="md-just-icon md-danger"
                    @click="removeGoods(item.id)"
                  >
                    <md-icon>delete</md-icon>
                    <md-tooltip md-direction="top"
                      >报废</md-tooltip
                    >
                  </md-button>
                </md-table-cell>
              </md-table-row>
            </md-table>
            <div
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
              "
            >
              <div>
                <md-button
                  class="md-just-icon md-success"
                  @click="
                    changeGoodsPage(currentGoodsPage - 1)
                  "
                  :disabled="currentGoodsPage <= 1"
                >
                  <md-icon>west</md-icon>
                  <md-tooltip md-direction="top"
                    >上一页</md-tooltip
                  >
                </md-button>
                <md-button
                  class="md-just-icon md-success"
                  @click="
                    changeGoodsPage(currentGoodsPage + 1)
                  "
                  :disabled="
                    currentGoodsPage >= totalGoodsPages
                  "
                >
                  <md-icon>east</md-icon>
                  <md-tooltip md-direction="top"
                    >下一页</md-tooltip
                  >
                </md-button>
                <md-button
                  class="md-just-icon md-success"
                  @click="completeMaintainRecord(item)"
                  v-if="
                    canCompleted && item.status !== '已完成'
                  "
                >
                  <md-icon>done_outline</md-icon>
                  <md-tooltip md-direction="top"
                    >完成</md-tooltip
                  >
                </md-button>
              </div>
              <div>
                <span>
                  第 {{ currentPage }} 页，总计
                  {{ searched.length }} 条，{{ totalPages }}
                  页。
                </span>
              </div>
            </div>
          </div>
        </div>
      </md-table>
    </div>
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
      "
    >
      <div>
        <md-button
          class="md-just-icon md-success"
          @click="changePage(currentPage - 1)"
          :disabled="currentPage <= 1"
        >
          <md-icon>west</md-icon>
          <md-tooltip md-direction="top">上一页</md-tooltip>
        </md-button>
        <md-button
          class="md-just-icon md-success"
          @click="changePage(currentPage + 1)"
          :disabled="currentPage >= totalPages"
        >
          <md-icon>east</md-icon>
          <md-tooltip md-direction="top">下一页</md-tooltip>
        </md-button>
        <md-button
          class="md-just-icon md-success"
          @click="exportData"
        >
          <md-icon>download</md-icon>
          <md-tooltip md-direction="top">导出</md-tooltip>
        </md-button>
      </div>
      <div>
        <span>
          第 {{ currentPage }} 页，总计
          {{ maintainRecords.length }} 条，{{ totalPages }}
          页
        </span>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  async mounted() {
    console.log("mounted");
    await this.updateMaintainRecords();
  },
  computed: {
    paginatedData() {
      const start =
        (this.currentPage - 1) * this.itemsPerPage;
      const end = this.currentPage * this.itemsPerPage;
      return this.maintainRecords.slice(start, end);
    },
    totalPages() {
      return Math.ceil(
        this.maintainRecords.length / this.itemsPerPage
      );
    },
    paginatedGoods() {
      console.log("paginatedGoods");
      const start =
        (this.currentGoodsPage - 1) * this.goodsPerPage;
      const end = this.currentGoodsPage * this.goodsPerPage;
      return this.searched.slice(start, end);
    },
    totalGoodsPages() {
      return Math.ceil(
        this.searched.length / this.goodsPerPage
      );
    },
    canCompleted() {
      console.log("canCompleted");
      return this.goods.every(
        (good) => good.status !== "维护中"
      );
    },
  },
  data() {
    return {
      maintainRecords: [],
      focusedItem: null,

      currentPage: 1,
      itemsPerPage: 10,

      isLoading: false,

      currentGoodsPage: 1,
      goodsPerPage: 5,

      goods: [],
      search: "",
      searched: [],
    };
  },
  methods: {
    async updateRecordGoods() {
      console.log("getRecordGoods");
      let req = {
        action: "getRecordGoods",
        recordId: this.focusedItem.id,
      };
      console.log("req", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        this.goods = msg.goods;
        this.searched = this.goods;
        console.log("getRecordGoods success");
      }
    },
    async repairGoods(goodsId) {
      console.log("repair goods", goodsId);
      let req = {
        action: "maintainGoods",
        maintainId: this.focusedItem.id,
        goodsId: goodsId,
        result: "修缮",
      };
      console.log("req", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        await this.updateRecordGoods();
        console.log("repair success");
      }
    },
    async removeGoods(goodsId) {
      console.log("removeGoods", goodsId);
      let req = {
        action: "maintainGoods",
        goodsId: goodsId,
        maintainId: this.focusedItem.id,
        result: "报废",
      };
      console.log("req", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        await this.updateRecordGoods();
        console.log("removeGoods success");
      }
    },
    changeGoodsPage(page) {
      if (page >= 1 && page <= this.totalGoodsPages) {
        this.currentGoodsPage = page;
      }
    },
    searchOnTable() {
      this.searched = this.goods.filter((item) => {
        return item.category.includes(this.search);
      });
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    async updateMaintainRecords() {
      console.log("getMaintainRecords");
      this.isLoading = true;
      let req = {
        action: "getMaintainRecords",
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      console.log("msg:", msg);
      if (msg && msg.result === "success") {
        this.maintainRecords = msg.record_list;
        console.log(
          "this.maintainRecords:",
          this.maintainRecords
        );
      }
      this.isLoading = false;
    },
    async completeMaintainRecord(item) {
      console.log("completeMaintainRecord");
      let req = {
        action: "completeMaintainRecord",
        recordId: item.id,
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        await this.updateMaintainRecords();
        this.$notifyVue("完成采购成功!");
      }
    },
    async toggleDetail(item) {
      console.log("item:", item);
      this.focusedItem =
        this.focusedItem === item ? null : item;
      this.isEditing = false;
      if (this.focusedItem) {
        await this.updateRecordGoods();
      }
    },
    exportData() {
      console.log("exportData");
      const modifiedData = this.maintainRecords.map(
        (item) => {
          return {
            维护记录编号: item.id,
            申请记录编号: item.applicationId,
            申请人: item.applicant.name,
            创建时间: item.createdTime,
            状态: item.status,
            完结时间: item.completedTime,
          };
        }
      );
      this.$ExportFile(modifiedData, "维护记录.xlsx");
      this.$notifyVue("导出成功!");
    },
  },
};
</script>
