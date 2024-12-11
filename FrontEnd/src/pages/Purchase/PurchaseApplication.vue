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
              @click="createPurchaseRecord(item.id)"
              :disabled="item.status !== '同意'"
            >
              <md-icon>add</md-icon>

              <md-tooltip md-direction="top"
                >为该申请创建采购记录</md-tooltip
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
      v-if="
        !isAddingPurchaseRecord &&
        !isAddingPurchaseApplication
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
          @click="createPurchaseApplication"
        >
          <md-icon>add</md-icon>
          <md-tooltip md-direction="top"
            >发起采购申请</md-tooltip
          ></md-button
        >
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
          {{ purchaseApplications.length }} 条，{{
            totalPages
          }}
          页
        </span>
      </div>
    </div>
    <!-- 新增采购记录 -->
    <div
      class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      v-if="isAddingPurchaseRecord"
    >
      <md-card>
        <md-card-header data-background-color="green">
          <h4 class="title">新增采购记录</h4>
        </md-card-header>
        <md-card-content>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>{{ "审批编号" }}</label>
              <md-input
                v-model="newPurchaseRecord.approve_id"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>{{ "供应商" }}</label>
              <md-input
                v-model="newPurchaseRecord.provider"
              ></md-input>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>{{ "物资类别" }}</label>
              <md-input
                v-model="newPurchaseRecord.goods_type"
              ></md-input>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>{{ "物资数量" }}</label>
              <md-input
                v-model="newPurchaseRecord.goods_num"
              ></md-input>
            </md-field>
          </div>
        </md-card-content>
        <md-card-content>
          <div class="text-right">
            <md-button
              class="md-just-icon md-success"
              @click="confirmAddingPurchaseRecord"
            >
              <md-icon>check</md-icon>
              <md-tooltip md-direction="top"
                >确认</md-tooltip
              >
            </md-button>
            <md-button
              class="md-just-icon"
              @click="cancelAddingPurchaseRecord"
            >
              <md-icon>close</md-icon>
              <md-tooltip md-direction="top"
                >取消</md-tooltip
              >
            </md-button>
          </div>
        </md-card-content>
      </md-card>
    </div>
    <!-- 新增采购申请 -->
    <div
      class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      v-if="isAddingPurchaseApplication"
    >
      <md-card>
        <md-card-header data-background-color="green">
          <h4 class="title">新增采购申请</h4>
        </md-card-header>
        <md-card-content>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>{{ "采购说明" }}</label>
              <md-textarea
                v-model="newPurchaseApplication.description"
              ></md-textarea>
            </md-field>
          </div>
        </md-card-content>
        <md-card-content>
          <div class="text-right">
            <md-button
              class="md-just-icon md-success"
              @click="confirmAddingPurchaseApplication"
            >
              <md-icon>check</md-icon>
              <md-tooltip md-direction="top"
                >确认</md-tooltip
              >
            </md-button>
            <md-button
              class="md-just-icon"
              @click="cancelAddingPurchaseApplication"
            >
              <md-icon>close</md-icon>
              <md-tooltip md-direction="top"
                >取消</md-tooltip
              >
            </md-button>
          </div>
        </md-card-content>
      </md-card>
    </div>
  </div>
</template>
<script>
export default {
  async mounted() {
    await this.updatePurchaseApplications();
  },
  data() {
    return {
      purchaseApplications: [],
      applicationOptions: ["待确认", "拒绝", "同意"],
      newPurchaseApplication: null,
      isAddingPurchaseApplication: false,

      newPurchaseRecord: null,
      isAddingPurchaseRecord: false,

      focusedItem: null,

      currentPage: 1,
      itemsPerPage: 5,

      isLoading: false,
    };
  },
  computed: {
    paginatedData() {
      const start =
        (this.currentPage - 1) * this.itemsPerPage;
      const end = this.currentPage * this.itemsPerPage;
      return this.purchaseApplications.slice(start, end);
    },
    totalPages() {
      return Math.ceil(
        this.purchaseApplications.length / this.itemsPerPage
      );
    },
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    toggleDetail(item) {
      console.log("item:", item);
      this.focusedItem =
        this.focusedItem === item ? null : item;
      this.isEditing = false;
    },
    getDefaultPurchaseRecord(id) {
      return {
        id: null,
        userId: this.$store.state.user.id,
        provider: null,
        approve_id: id,
        created_time: null,
        completed_time: null,
        goods_type: null,
        goods_num: null,
        status: "未完成",
      };
    },
    createPurchaseRecord(applicationId) {
      console.log("createPurchaseRecord");
      console.log("applicationId:", applicationId);
      this.newPurchaseRecord =
        this.getDefaultPurchaseRecord(applicationId);
      this.isAddingPurchaseRecord = true;
    },
    async confirmAddingPurchaseRecord() {
      console.log("confirmAddingPurchaseRecord");
      let req = {
        action: "createPurchaseRecord",
        record: JSON.parse(
          JSON.stringify(this.newPurchaseRecord)
        ),
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        this.isAddingPurchaseRecord = false;
        this.$notifyVue(
          "新增采购记录成功!",
          "success",
          "bottom"
        );
      }
      this.isAddingPurchaseRecord = false;
    },
    cancelAddingPurchaseRecord() {
      console.log("cancelAddingPurchaseRecord");
      this.isAddingPurchaseRecord = false;
    },
    async updatePurchaseApplications() {
      console.log("getPurchaseApplications");
      this.isLoading = true;
      let req = {
        action: "getPurchaseApplications",
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      console.log("msg:", msg);
      if (msg && msg.result === "success") {
        this.purchaseApplications = msg.applications;
        console.log(
          "this.purchaseApplications:",
          this.purchaseApplications
        );
      }
      this.isLoading = false;
    },
    getDefaultPurchaseApplication() {
      return {
        applicant: {
          id: this.$store.state.user.id,
          name: this.$store.state.user.name,
          department_name:
            this.$store.state.user.department_name,
        },
        operation_type: null,
        created_time: null,
        updated_time: null,
        description: null,
        status: "待确认",
        approver: null,
        reply: null,
      };
    },
    createPurchaseApplication() {
      console.log("createPurchaseApplication");
      this.newPurchaseApplication =
        this.getDefaultPurchaseApplication();
      this.isAddingPurchaseApplication = true;
    },
    async confirmAddingPurchaseApplication() {
      console.log("confirmAddingPurchaseApplication");
      // TODO
      let req = {
        action: "createPurchaseApplication",
        application: JSON.parse(
          JSON.stringify(this.newPurchaseApplication)
        ),
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      console.log("msg:", msg);
      if (msg && msg.result === "success") {
        await this.updatePurchaseApplications();
        await this.updatePurchaseApplications();
        this.isAddingPurchaseApplication = false;

        this.$notifyVue("新增采购申请成功!");
      }
    },
    cancelAddingPurchaseApplication() {
      console.log("cancelAddingPurchaseApplication");
      this.isAddingPurchaseApplication = false;
    },
    exportData() {
      console.log("exportPurchaseApplication");
      const modifiedData = this.purchaseApplications.map(
        (item) => {
          return {
            申请编号: item.id,
            申请人: item.applicant.name,
            申请时间: item.created_time,
            申请内容: item.description,
            更新时间: item.updated_time,
            申请状态: item.status,
            答复: item.reply,
          };
        }
      );
      this.$ExportFile(modifiedData, "采购申请表.xlsx");
      this.$notifyVue("导出采购申请成功!");
    },
  },
};
</script>
