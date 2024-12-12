<template>
  <div>
    <!-- 过滤条件 -->
    <div class="md-layout">
      <div class="md-layout-item md-size-25">
        <md-field>
          <label>{{ idHeader }}</label>
          <md-input
            v-model="filters.id"
            @input="updateFilteredGoods"
          ></md-input>
        </md-field>
      </div>
      <div class="md-layout-item md-size-25">
        <md-field>
          <label>{{ purchaseIdHeader }}</label>
          <md-input
            v-model="filters.purchaseId"
            type="text"
            @input="updateFilteredGoods"
          ></md-input>
        </md-field>
      </div>
      <div class="md-layout-item md-size-25">
        <md-field>
          <label>{{ categoryHeader }}</label>
          <md-select
            v-model="filters.category"
            @input="updateFilteredGoods"
          >
            <md-option
              v-for="option in filter_categoryOptions"
              :key="option"
              :value="option"
              >{{ option }}</md-option
            >
          </md-select>
        </md-field>
      </div>
      <div class="md-layout-item md-size-25">
        <md-field>
          <label>{{ statusHeader }}</label>
          <md-select
            v-model="filters.status"
            @input="updateFilteredGoods"
          >
            <md-option
              v-for="option in filter_statusOptions"
              :key="option"
              :value="option"
              >{{ option }}</md-option
            >
          </md-select>
        </md-field>
      </div>
    </div>
    <div style="text-align: center" v-if="isLoading">
      <md-progress-spinner
        :md-diameter="100"
        :md-stroke="10"
        md-mode="indeterminate"
      ></md-progress-spinner>
    </div>
    <!-- 物资列表 -->
    <div v-if="!isLoading">
      <md-table
        v-model="paginatedData"
        table-header-color="green"
      >
        <md-table-row
          slot="md-table-row"
          slot-scope="{ item }"
        >
          <md-table-cell :md-label="idHeader">{{
            item.id
          }}</md-table-cell>
          <md-table-cell :md-label="purchaseIdHeader">{{
            item.purchaseId
          }}</md-table-cell>
          <md-table-cell :md-label="categoryHeader">{{
            item.category
          }}</md-table-cell>
          <md-table-cell :md-label="statusHeader">{{
            item.status
          }}</md-table-cell>
        </md-table-row>
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
          v-if="
            this.$store.state.user.identity === '管理员'
          "
          class="md-just-icon md-success"
          @click="deleteGoods"
        >
          <md-icon>delete</md-icon>
          <md-tooltip md-direction="top"
            >删除报废、已丢失、已逾期的物资</md-tooltip
          >
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
          {{ filteredGoods.length }} 条，{{ totalPages }}
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
    await this.getGoodsCategory();
    await this.updateGoods();
  },
  computed: {
    paginatedData() {
      const start =
        (this.currentPage - 1) * this.itemsPerPage;
      const end = this.currentPage * this.itemsPerPage;
      return this.filteredGoods.slice(start, end);
    },
    totalPages() {
      return Math.ceil(
        this.filteredGoods.length / this.itemsPerPage
      );
    },
  },
  data() {
    return {
      goods: [],
      statusOptions: [
        "租赁中",
        "维护中",
        "库中",
        "已报废",
        "已丢失",
        "已逾期",
      ],

      filter_statusOptions: [
        "租赁中",
        "维护中",
        "库中",
        "全部状态",
        "已报废",
        "已丢失",
        "已逾期",
      ],
      filter_categoryOptions: [],
      filters: {
        id: "",
        purchaseId: "",
        name: "",
        category: "全部类别",
        price: "",
        status: "全部状态",
      },
      idHeader: "物资编号",
      purchaseIdHeader: "采购订单编号",
      nameHeader: "物资名称",
      categoryHeader: "物资类别",
      priceHeader: "物资单价",
      statusHeader: "物资状态",
      filteredGoods: [],

      currentPage: 1,
      itemsPerPage: 10,

      isLoading: false,

      //
    };
  },
  methods: {
    async getGoodsCategory() {
      console.log("getGoodsCategory");
      let req = {
        action: "getGoodsCategory",
      };
      let res = await this.$Backend(req);
      if (res && res.result) {
        console.log("getGoodsCategory success");
        this.filter_categoryOptions = res.categoryList.map(
          (item) => item.name
        );
        this.filter_categoryOptions.push("全部类别");
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    updateFilteredGoods() {
      console.log("updateFilteredGoods");
      console.log("this.filters:", this.filters);
      this.currentPage = 1;
      this.filteredGoods = this.goods.filter((item) => {
        console.log(item);
        return (
          (this.filters.id === "" ||
            item.id.includes(this.filters.id)) &&
          (this.filters.purchaseId === "" ||
            item.purchaseId.includes(
              this.filters.purchaseId
            )) &&
          (this.filters.category === "" ||
            this.filters.category === "全部类别" ||
            item.category.includes(
              this.filters.category
            )) &&
          (this.filters.status === "" ||
            this.filters.status === "全部状态" ||
            item.status.includes(this.filters.status))
        );
      });
    },

    async updateGoods() {
      console.log("getGoods");
      this.isLoading = true;
      try {
        let req = {
          action: "getGoods",
        };
        let res = await this.$Backend(req);
        console.log("res:", res);
        if (res && res.result === "success") {
          console.log("getGoods success");
          this.goods = res.goods;
          this.updateFilteredGoods();
        }
      } finally {
        this.isLoading = false;
      }
    },
    async deleteGoods() {
      console.log("deleteGoods");
      let req = {
        action: "deleteGoods",
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        console.log("deleteGoods success");
        await this.updateGoods();
      }
    },
    exportData() {
      console.log("exportPurchaseApproves");
      const modifiedData = this.filteredGoods.map(
        (item) => {
          return {
            物资编号: item.id,
            采购订单编号: item.purchaseId,
            物资类别: item.category,
            物资状态: item.status,
          };
        }
      );
      this.$ExportFile(modifiedData, "物资表.xlsx");
      this.$notifyVue("导出成功");
    },
  },
};
</script>
