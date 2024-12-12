<template>
  <div>
    <!-- 维护申请表 -->
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
                @click="createMaintainRecord(item.id)"
                :disabled="item.status !== '同意'"
              >
                <md-icon>add</md-icon>

                <md-tooltip md-direction="top"
                  >为该申请创建维护记录</md-tooltip
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
          <div
            class="md-layout"
            v-if="focusedItem === item"
          >
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
          !isAddingMaintainRecord &&
          !isAddingMaintainApplication
        "
      >
        <div>
          <md-button
            class="md-just-icon md-success"
            @click="changePage(currentPage - 1)"
            :disabled="currentPage <= 1"
          >
            <md-icon>west</md-icon>
            <md-tooltip md-direction="top"
              >上一页</md-tooltip
            >
          </md-button>
          <md-button
            class="md-just-icon md-success"
            @click="changePage(currentPage + 1)"
            :disabled="currentPage >= totalPages"
          >
            <md-icon>east</md-icon>
            <md-tooltip md-direction="top"
              >下一页</md-tooltip
            >
          </md-button>
          <md-button
            class="md-just-icon md-success"
            @click="createMaintainApplication"
          >
            <md-icon>add</md-icon>
            <md-tooltip md-direction="top"
              >发起维护申请</md-tooltip
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
            {{ maintainApplications.length }} 条，{{
              totalPages
            }}
            页
          </span>
        </div>
      </div>
    </div>

    <div
      class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      v-if="isAddingMaintainRecord"
    >
      <md-card>
        <md-card-header data-background-color="green">
          <h4 class="title">新增维护记录</h4>
        </md-card-header>
        <md-card-content>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>{{ "审批编号" }}</label>
              <md-input
                v-model="newMaintainRecord.approveId"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div>
            <md-table
              v-model="paginatedGoods"
              md-card
              :md-selected-value.sync="selected"
            >
              <md-table-toolbar>
                <div class="md-toolbar-section-start">
                  <h1 class="md-title">选择维护物资</h1>
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
                <h1 class="md-title">选择物资</h1>
              </md-table-toolbar>

              <md-table-row
                slot="md-table-row"
                slot-scope="{ item }"
                md-selectable="multiple"
                md-auto-select
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
                  @click="selected = []"
                >
                  <md-icon>delete</md-icon>
                  <md-tooltip md-direction="top"
                    >清空</md-tooltip
                  >
                </md-button>
                <md-button
                  class="md-just-icon md-success"
                  @click="selected = searched"
                >
                  <md-icon>select_all</md-icon>
                  <md-tooltip md-direction="top"
                    >全选</md-tooltip
                  >
                </md-button>
              </div>
              <div>
                <span>
                  第 {{ currentPage }} 页，总计
                  {{ searched.length }} 条，{{
                    totalPages
                  }}
                  页。{{ selected.length }}
                  件物资被选择。
                </span>
              </div>
            </div>
          </div>
        </md-card-content>
        <md-card-content>
          <div class="text-right">
            <md-button
              class="md-just-icon md-success"
              @click="confirmAddingMaintainRecord"
            >
              <md-icon>check</md-icon>
              <md-tooltip md-direction="top"
                >确认</md-tooltip
              >
            </md-button>
            <md-button
              class="md-just-icon"
              @click="cancelAddingMaintainRecord"
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
    <!-- 新增维护申请 -->
    <div
      class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      v-if="isAddingMaintainApplication"
    >
      <md-card>
        <md-card-header data-background-color="green">
          <h4 class="title">新增维护申请</h4>
        </md-card-header>
        <md-card-content>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>{{ "维护说明" }}</label>
              <md-textarea
                v-model="newMaintainApplication.description"
              ></md-textarea>
            </md-field>
          </div>
        </md-card-content>
        <md-card-content>
          <div class="text-right">
            <md-button
              class="md-just-icon md-success"
              @click="confirmAddingMaintainApplication"
            >
              <md-icon>check</md-icon>
              <md-tooltip md-direction="top"
                >确认</md-tooltip
              >
            </md-button>
            <md-button
              class="md-just-icon"
              @click="cancelAddingMaintainApplication"
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
    await this.updateMaintainApplications();
  },
  data() {
    return {
      maintainApplications: [],
      applicationOptions: ["待确认", "拒绝", "同意"],
      newMaintainApplication: null,
      isAddingMaintainApplication: false,

      newMaintainRecord: null,
      isAddingMaintainRecord: false,

      focusedItem: null,

      currentPage: 1,
      itemsPerPage: 5,

      currentGoodsPage: 1,
      goodsPerPage: 5,

      isLoading: false,

      goods: [],
      selected: [],
      search: "",
      searched: [],
    };
  },
  computed: {
    paginatedData() {
      const start =
        (this.currentPage - 1) * this.itemsPerPage;
      const end = this.currentPage * this.itemsPerPage;
      return this.maintainApplications.slice(start, end);
    },
    totalPages() {
      return Math.ceil(
        this.maintainApplications.length / this.itemsPerPage
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
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
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
    toggleDetail(item) {
      console.log("item:", item);
      this.focusedItem =
        this.focusedItem === item ? null : item;
      this.isEditing = false;
    },
    getDefaultMaintainRecord(id) {
      return {
        userId: this.$store.state.user.id,
        approveId: id,
        goods: [],
      };
    },
    async getDamageGoods() {
      console.log("getDamageGoods");
      this.isLoading = true;
      try {
        let req = {
          action: "getDamageGoods",
        };
        let res = await this.$Backend(req);
        console.log("res:", res);
        if (res && res.result === "success") {
          console.log("getGoods success");
          this.goods = res.goods;
        }
      } finally {
        this.isLoading = false;
      }
    },
    async createMaintainRecord(applicationId) {
      console.log("createMaintainRecord");
      console.log("applicationId:", applicationId);
      this.newMaintainRecord =
        this.getDefaultMaintainRecord(applicationId);
      await this.getDamageGoods();
      this.searched = this.goods;
      this.isAddingMaintainRecord = true;
    },
    async confirmAddingMaintainRecord() {
      console.log("confirmAddingMaintainRecord");
      console.log("this.selected:", this.selected);
      console.log(
        "this.newMaintainRecord:",
        this.newMaintainRecord
      );
      this.newMaintainRecord.goods = this.selected.map(
        (good) => good.id
      );

      let req = {
        action: "createMaintainRecord",
        record: JSON.parse(
          JSON.stringify(this.newMaintainRecord)
        ),
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        this.isAddingMaintainRecord = false;
        this.$notifyVue(
          "新增维护记录成功!",
          "success",
          "bottom"
        );
      }
      this.isAddingMaintainRecord = false;
      this.selected = [];
    },
    cancelAddingMaintainRecord() {
      console.log("cancelAddingMaintainRecord");
      this.isAddingMaintainRecord = false;
    },
    async updateMaintainApplications() {
      console.log("updateMaintainApplications");
      this.isLoading = true;
      let req = {
        action: "getMaintainApplications",
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      console.log("msg:", msg);
      if (msg && msg.result === "success") {
        this.maintainApplications = msg.applications;
        console.log(
          "this.maintainApplications:",
          this.maintainApplications
        );
      }
      this.isLoading = false;
    },
    getDefaultMaintainApplication() {
      return {
        userId: this.$store.state.user.id,
        description: null,
      };
    },
    createMaintainApplication() {
      console.log("createMaintainApplication");
      this.newMaintainApplication =
        this.getDefaultMaintainApplication();
      this.isAddingMaintainApplication = true;
    },
    async confirmAddingMaintainApplication() {
      console.log("confirmAddingMaintainApplication");
      // TODO
      let req = {
        action: "createMaintainApplication",
        application: JSON.parse(
          JSON.stringify(this.newMaintainApplication)
        ),
      };
      console.log("req:", req);
      let msg = await this.$Backend(req);
      console.log("msg:", msg);
      if (msg && msg.result === "success") {
        await this.updateMaintainApplications();
        await this.updateMaintainApplications();
        this.isAddingMaintainApplication = false;

        this.$notifyVue("新增维护申请成功!");
      }
    },
    cancelAddingMaintainApplication() {
      console.log("cancelAddingMaintainApplication");
      this.isAddingMaintainApplication = false;
    },
    exportData() {
      console.log("exportMaintainApplication");
      const modifiedData = this.maintainApplications.map(
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
      this.$ExportFile(modifiedData, "维护申请表.xlsx");
      this.$notifyVue("导出成功");
    },
  },
};
</script>
