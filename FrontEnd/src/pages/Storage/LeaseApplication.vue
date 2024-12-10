<template>
  <div>
    <!-- 租赁申请表 -->
    <div style="text-align: center" v-if="isLoading">
      <md-progress-spinner
        :md-diameter="100"
        :md-stroke="10"
        md-mode="indeterminate"
      ></md-progress-spinner>
    </div>
    <div v-if="!isLoading">
      <md-table
        v-for="(item, index) in leaseApplications"
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
                item.createdTime
              }}</span>
              由
              <span class="text-info">{{
                item.applicant.name
              }}</span>
              发起的
              <span class="text-danger">租赁</span>
              申请，状态为
              <span class="text-danger">{{
                item.status
              }}</span>
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
          <div class="md-layout-item">
            <md-field>
              <label>编号</label>
              <md-input
                v-model="item.id"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>发起人</label>
              <md-input
                v-model="item.applicant.name"
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
                v-model="item.createdTime"
                type="text"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>物资信息</label>
              <md-input
                v-model="item.message"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>物资用途</label>
              <md-input
                v-model="item.usage"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>结束时间</label>
              <md-input
                v-model="item.completedTime"
                type="text"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>状态</label>
              <md-input
                v-model="item.status"
                type="text"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item">
            <md-field>
              <label>批示信息</label>
              <md-input
                v-model="item.returnMessage"
              ></md-input>
            </md-field>
          </div>
          <!-- 借出物资 -->
          <div
            class="md-layout-item md-size-100"
            v-if="item.status === '待确认'"
          >
            <LeaseGoods ref="LeaseGoods" />
            <md-button
              class="md-just-icon"
              @click="confirmLease(item)"
            >
              <md-icon>check</md-icon>
              <md-tooltip>确认借出</md-tooltip></md-button
            >
            <md-button
              class="md-just-icon"
              @click="refuseLease(item)"
            >
              <md-icon>close</md-icon>
              <md-tooltip>拒绝借出</md-tooltip></md-button
            >
          </div>
          <!-- 归还物资 -->
          <div
            v-if="
              item.status === '归还中' ||
              item.status === '已结束'
            "
            class="md-layout-item md-size-100"
          >
            <ReturnGoods
              ref="ReturnGoods"
              :applicationId="item.id"
            />
            <md-button
              v-if="canReturn"
              class="md-just-icon"
              @click="checkReturn(item)"
            >
              <md-icon>check</md-icon>
              <md-tooltip>检查完毕</md-tooltip></md-button
            >
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
          {{ leaseApplications.length }} 条，{{
            totalPages
          }}
          页
        </span>
      </div>
    </div>
  </div>
</template>
<script>
import LeaseGoods from "./LeaseGoods.vue";
import ReturnGoods from "./ReturnGoods.vue";
export default {
  components: {
    LeaseGoods,
    ReturnGoods,
  },
  async mounted() {
    console.log("mounted");
    await this.updateLeaseApplications();
  },
  computed: {
    paginatedData() {
      const start =
        (this.currentPage - 1) * this.itemsPerPage;
      const end = this.currentPage * this.itemsPerPage;
      return this.leaseApplications.slice(start, end);
    },
    totalPages() {
      return Math.ceil(
        this.leaseApplications.length / this.itemsPerPage
      );
    },
    paginatedLeaseGoods() {
      console.log("paginatedLeaseGoods");
      const start =
        (this.currentLeaseGoodsPage - 1) *
        this.leaseLeaseGoodsPerPage;
      const end =
        this.currentLeaseGoodsPage *
        this.leaseLeaseGoodsPerPage;
      return this.leaseGoodsSearched.slice(start, end);
    },
    totalLeaseGoodsPages() {
      return Math.ceil(
        this.leaseGoodsSearched.length /
          this.leaseLeaseGoodsPerPage
      );
    },
    canCompleted() {
      console.log("canCompleted");
      return this.leaseLeaseGoods.every(
        (good) => good.status !== "维护中"
      );
    },
  },
  data() {
    return {
      selected: [],
      leaseApplications: [],
      focusedItem: null,

      currentPage: 1,
      itemsPerPage: 10,

      isLoading: false,

      currentLeaseGoodsPage: 1,
      leaseLeaseGoodsPerPage: 5,

      leaseLeaseGoods: [],
      leaseGoodsSearched: [],

      goodsCategory: [],
    };
  },
  methods: {
    canReturn(item) {
      console.log("item.status", item.status);
      return (
        this.$refs.ReturnGoods[0].canReturn() &&
        item.status != "已结束"
      );
    },
    async refuseLease(item) {
      console.log("refuseLease", item);
      let req = {
        action: "refuseLease",
        applicationId: item.id,
        message: item.returnMessage,
      };
      console.log("req", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        await this.updateLeaseApplications();
      }
    },

    async checkReturn(item) {
      console.log("checkReturn", item);
      let req = {
        action: "checkReturn",
        applicationId: item.id,
      };
      console.log("req", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        await this.updateLeaseApplications();
      }
    },
    async confirmLease(item) {
      console.log("confirmLease", item);
      console.log(
        "this.$refs.LeaseGoods",
        this.$refs.LeaseGoods[0],
        typeof this.$refs.LeaseGoods[0].leaseGoods
      );
      let res = await this.$refs.LeaseGoods[0].leaseGoods(
        item
      );
      if (res === "success") {
        await this.updateLeaseApplications();
      }
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    async updateLeaseApplications() {
      console.log("getLeaseApplications");
      this.isLoading = true;
      let req = {
        action: "getLeaseApplications",
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      console.log("msg:", msg);
      if (msg && msg.result === "success") {
        console.log("getLeaseApplications success");
        this.leaseApplications = msg.applications;
      }
      this.isLoading = false;
    },

    async toggleDetail(item) {
      console.log("item:", item);
      this.focusedItem =
        this.focusedItem === item ? null : item;
      this.isEditing = false;
      if (this.focusedItem) {
        // await this.$refs.LeaseGoods.getLeaseGoodsCategory();
      }
    },
    exportData() {
      console.log("exportData");
      const modifiedData = this.filteredUsers.map(
        (item) => {
          return {
            租赁申请编号: item.approveId,
            申请人编号: item.applicant.id,
            申请人姓名: item.applicant.name,
            创建时间: item.createdTime,
            物资信息: item.message,
            物资用途: item.usage,
          };
        }
      );
      this.$ExportFile(modifiedData, "采购记录表.txt");
    },
  },
};
</script>
