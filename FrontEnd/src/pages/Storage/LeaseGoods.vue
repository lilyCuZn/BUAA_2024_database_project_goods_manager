<template>
  <div>
    <md-table v-model="paginatedData" md-card>
      <md-table-toolbar>
        <div class="md-toolbar-section-start">
          <h1 class="md-title">借出物资</h1>
        </div>
      </md-table-toolbar>
      <md-table-toolbar>
        <h1 class="md-title">物资</h1>
      </md-table-toolbar>

      <md-table-row
        slot="md-table-row"
        slot-scope="{ item }"
      >
        <md-table-cell md-label="物资类别">{{
          item.category
        }}</md-table-cell>
        <md-table-cell md-label="物资数量">
          <md-field>
            <md-input
              v-model="item.num"
              type="number"
            ></md-input>
          </md-field>
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
  async mounted() {
    await this.getLeaseGoodsCategory();
  },
  computed: {
    paginatedData() {
      return this.searched.slice(
        (this.currentPage - 1) * this.itemsPerPage,
        this.currentPage * this.itemsPerPage
      );
    },
    totalPages() {
      return Math.ceil(
        this.searched.length / this.itemsPerPage
      );
    },
  },
  data() {
    return {
      itemsPerPage: 5,
      currentPage: 1,
      searched: [],
      categoryNum: [],
    };
  },
  methods: {
    async getLeaseGoodsCategory() {
      console.log("getLeaseGoodsCategory");
      let req = {
        action: "getGoodsCategory",
      };
      let res = await this.$Backend(req);
      if (res && res.result) {
        console.log("getLeaseGoodsCategory success");
        this.categoryNum = res.categoryList.map((item) => {
          return {
            category: item.name,
            num: 0,
          };
        });
        this.searched = this.categoryNum;
      }
    },
    async leaseGoods(application) {
      console.log("leaseGoods");
      let req = {
        action: "leaseGoods",
        applicationId: application.id,
        categoryNum: this.categoryNum,
        message: application.returnMessage,
      };
      let res = await this.$Backend(req);
      if (res && res.result === "success") {
        if (res.reply === "success") {
          this.$notifyVue("租赁成功!");
          return "success";
        } else {
          this.$notifyVue(
            "库中物资不足，租赁失败！",
            "danger",
            "bottom"
          );
          return "fail";
        }
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
};
</script>
