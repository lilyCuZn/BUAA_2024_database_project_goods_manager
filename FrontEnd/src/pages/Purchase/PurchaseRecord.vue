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
        v-for="(item, index) in purchaseRecords"
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
              <span class="text-success">{{
                item.created_time
              }}</span>
              由
              <span class="text-info">{{
                item.applicant.name
              }}</span>
              发起的
              <span class="text-danger">采购</span>
              记录，状态为
              <span class="text-danger">{{
                item.status
              }}</span>
            </div>
          </md-table-cell>
          <div style="text-align: right">
            <md-button
              class="md-just-icon md-simple md-primary"
              @click="completePurchaseRecord(item)"
              v-if="item.status !== '已采购'"
            >
              <md-icon>check</md-icon>

              <md-tooltip md-direction="top"
                >完成该订单</md-tooltip
              >
            </md-button>
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
          <div class="md-layout-item">
            <md-field>
              <label>采购记录编号</label>
              <md-input
                v-model="item.id"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>申请记录编号</label>
              <md-input
                v-model="item.approver"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>供应商</label>
              <md-input
                v-model="item.provider"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>物资类别</label>
              <md-input
                v-model="item.goods_type"
                type="text"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>物资数量</label>
              <md-input
                v-model="item.goods_num"
                type="text"
                disabled
              ></md-input>
            </md-field>
          </div>

          <div
            class="md-layout-item md-small-size-100 md-size-50"
          >
            <md-field>
              <label>创建时间</label>
              <md-input
                v-model="item.created_time"
                type="text"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>完成时间</label>
              <md-input
                v-model="item.completed_time"
                type="text"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>记录状态</label>
              <md-input
                v-model="item.status"
                type="text"
                disabled
              ></md-input>
            </md-field>
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
          @click="exportData"
        >
          <md-icon>download</md-icon>
          <md-tooltip md-direction="top">导出</md-tooltip>
        </md-button>
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
          {{ purchaseRecords.length }} 条，{{ totalPages }}
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
    await this.updatePurchaseRecords();
  },
  computed: {
    paginatedData() {
      const start =
        (this.currentPage - 1) * this.itemsPerPage;
      const end = this.currentPage * this.itemsPerPage;
      return this.purchaseRecords.slice(start, end);
    },
    totalPages() {
      return Math.ceil(
        this.purchaseRecords.length / this.itemsPerPage
      );
    },
  },
  data() {
    return {
      purchaseRecords: [],
      focusedItem: null,

      currentPage: 1,
      itemsPerPage: 10,

      isLoading: false,
    };
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    async updatePurchaseRecords() {
      console.log("getPurchaseRecords");
      this.isLoading = true;
      let req = {
        action: "getPurchaseRecords",
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      console.log("msg:", msg);
      if (msg && msg.result === "success") {
        this.purchaseRecords = msg.orders;
        console.log(
          "this.purchaseRecords:",
          this.purchaseRecords
        );
      }
      this.isLoading = false;
    },
    async completePurchaseRecord(item) {
      console.log("completePurchaseRecord");
      let req = {
        action: "completePurchaseRecord",
        recordId: item.id,
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        await this.updatePurchaseRecords();
        this.$notifyVue("完成采购成功!");
      }
    },
    toggleDetail(item) {
      console.log("item:", item);
      this.focusedItem =
        this.focusedItem === item ? null : item;
      this.isEditing = false;
    },
    exportData() {
      console.log("exportData");
      const modifiedData = this.filteredUsers.map(
        (item) => {
          return {
            采购记录编号: item.id,
            申请记录编号: item.approver,
            供应商: item.provider,
            物资类别: item.goods_type,
            物资数量: item.goods_num,
            创建时间: item.created_time,
            完成时间: item.completed_time,
            记录状态: item.status,
          };
        }
      );
      this.$ExportFile(modifiedData, "采购记录表.txt");
    },
  },
};
</script>
