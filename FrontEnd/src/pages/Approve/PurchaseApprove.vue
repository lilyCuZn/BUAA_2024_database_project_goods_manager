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
        v-for="(item, index) in paginatedData"
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
              申请编号：<span class="text-info">{{
                item.id
              }}</span
              >,
              <span class="text-success">{{
                item.created_time
              }}</span>
              由
              <span class="text-info">{{
                item.applicant.name
              }}</span>
              发起的
              <span class="text-danger">{{
                item.operation_type
              }}</span>
              请求，状态为
              <span class="text-danger">{{
                item.status
              }}</span
              ><span v-if="item.status !== '待确认'"
                >，更新时间为&nbsp;<span
                  class="text-success"
                  >{{ item.updated_time }}</span
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
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>申请状态</label>
              <md-select v-model="item.status" disabled>
                <md-option
                  v-for="option in approveOptions"
                  :key="option"
                  :value="option"
                  >{{ option }}</md-option
                >
              </md-select>
            </md-field>
          </div>

          <div
            class="md-layout-item md-small-size-100 md-size-50"
          >
            <md-field>
              <label>申请内容</label>
              <md-textarea
                v-model="item.description"
                type="textarea"
                disabled
              ></md-textarea>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-50"
          >
            <md-field>
              <label>答复</label>
              <md-textarea
                v-model="item.reply"
                type="textarea"
                disabled
              ></md-textarea>
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
          {{ purchaseApproves.length }} 条，{{ totalPages }}
          页
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PurchaseApprove",
  async mounted() {
    console.log("mounted");
    await this.updatePurchaseApproves();
  },
  data() {
    return {
      purchaseApproves: [],
      approveOptions: ["待确认", "拒绝", "同意"],
      focusedItem: null,

      currentPage: 1,
      itemsPerPage: 10,

      isLoading: false,
    };
  },
  computed: {
    paginatedData() {
      const start =
        (this.currentPage - 1) * this.itemsPerPage;
      const end = this.currentPage * this.itemsPerPage;
      return this.purchaseApproves.slice(start, end);
    },
    totalPages() {
      return Math.ceil(
        this.purchaseApproves.length / this.itemsPerPage
      );
    },
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    async updatePurchaseApproves() {
      console.log("updatePurchaseApproves");
      this.isLoading = true;
      let req = {
        action: "getPurchaseApproves",
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        console.log("updatePurchaseApproves success");
        this.purchaseApproves = msg.applications;
      }
      this.isLoading = false;
    },

    toggleDetail(item) {
      console.log("item:", item);
      this.focusedItem =
        this.focusedItem === item ? null : item;
    },
    exportData() {
      console.log("exportPurchaseApproves");
      const modifiedData = this.purchaseApproves.map(
        (item) => {
          return {
            申请编号: item.id,
            申请人: item.applicant.name,
            部门: item.applicant.department_name,
            申请类型: item.operation_type,
            申请时间: item.created_time,
            申请内容: item.description,
            更新时间: item.updated_time,
            答复: item.reply,
            申请状态: item.status,
          };
        }
      );
      this.$ExportFile(
        modifiedData,
        "采购部门审批记录.xlsx"
      );
    },
  },
};
</script>
