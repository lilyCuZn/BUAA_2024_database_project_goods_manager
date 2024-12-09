<template>
  <div>
    <md-table v-model="paginatedData" md-card>
      <md-table-toolbar>
        <div class="md-toolbar-section-start">
          <h1 class="md-title">归还物资</h1>
        </div>
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
        <md-table-cell md-label="物资状态">
          {{ item.status }}
        </md-table-cell>
        <md-table-cell
          md-label="检查"
          v-if="item.status === '租赁中'"
        >
          <md-button
            class="md-just-icon md-simple"
            @click="setGoodsStatus(item.id, '完好')"
          >
            <md-icon>verified</md-icon>
            <md-tooltip md-direction="top">完好</md-tooltip>
          </md-button>
          <md-button
            class="md-just-icon md-simple"
            @click="setGoodsStatus(item.id, '损坏')"
          >
            <md-icon>heart_broken</md-icon>
            <md-tooltip md-direction="top">损坏</md-tooltip>
          </md-button>
          <md-button
            class="md-just-icon md-simple"
            @click="setGoodsStatus(item.id, '丢失')"
          >
            <md-icon>heart_broken</md-icon>
            <md-tooltip md-direction="top">丢失</md-tooltip>
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
</template>
<script>
export default {
  props: {
    applicationId: {
      type: Number,
      required: true, // 强制父组件提供该值
    },
  },
  async mounted() {
    console.log("mounted");
    await this.getReturnGoods();
  },
  computed: {
    paginatedData() {
      return this.searched.slice(
        (this.currentPage - 1) * 10,
        this.currentPage * 10
      );
    },
  },
  data() {
    return {
      currentPage: 1,
      totalPages: 1,
      searched: [],
      returnGoods: [],
    };
  },
  methods: {
    canReturn() {
      console.log("canReturn");
      return this.returnGoods.every(
        (item) => item.status != "租赁中"
      );
    },
    async setGoodsStatus(id, status) {
      console.log("setGoodsStatus");
      let req = {
        action: "setGoodsStatus",
        goodsId: id,
        status: status,
        applicationId: this.applicationId,
      };
      let res = await this.$Backend(req);
      if (res && res.result) {
        console.log("setGoodsStatus success");
        await this.getReturnGoods();
      }
    },
    async getReturnGoods() {
      console.log("getReturnGoods");
      let req = {
        action: "getReturnGoods",
        applicationId: this.applicationId,
      };
      let res = await this.$Backend(req);
      if (res && res.result) {
        console.log("getReturnGoods success");
        this.returnGoods = res.returnGoods;
        this.searched = this.returnGoods;
      }
    },
    changePage(page) {
      this.currentPage = page;
    },
  },
};
</script>
