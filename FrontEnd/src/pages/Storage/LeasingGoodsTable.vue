<template>
  <div>
    <md-table v-model="paginatedData" md-card>
      <md-table-toolbar>
        <div class="md-toolbar-section-start">
          <h1 class="md-title">租赁中的物资</h1>
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
