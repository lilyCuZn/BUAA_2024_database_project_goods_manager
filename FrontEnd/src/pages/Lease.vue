<template>
  <div class="content">
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      >
        <md-card>
          <!-- 表头 -->
          <md-card-header data-background-color="green">
            <div
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
              "
            >
              <div>
                <h4 class="title">租赁申请</h4>
                <p class="category">
                  试着添加一些过滤条件，查看租赁申请状态~
                </p>
              </div>
              <div><md-icon>search</md-icon></div>
            </div>
          </md-card-header>
          <!-- 过滤条件 -->
          <md-card-content>
            <div class="md-layout">
              <div class="md-layout-item md-size-5">
                <md-field>
                  <label>{{ idHeader }}</label>
                  <md-input
                    v-model="filters.id"
                    @input="updateFilteredLeaseApplies"
                  ></md-input>
                </md-field>
              </div>
              <div class="md-layout-item md-size-20">
                <md-field>
                  <label>{{ createdTimeHeader }}</label>
                  <md-input
                    v-model="filters.createdTime"
                    @input="updateFilteredLeaseApplies"
                  ></md-input>
                </md-field>
              </div>
              <div class="md-layout-item md-size-25">
                <md-field>
                  <label>{{ goodsInfoHeader }}</label>
                  <md-input
                    v-model="filters.goodsInfo"
                    @input="updateFilteredLeaseApplies"
                  ></md-input>
                </md-field>
              </div>

              <div class="md-layout-item md-size-25">
                <md-field>
                  <label>{{ goodsUsageHeader }}</label>
                  <md-input
                    v-model="filters.goodsUsage"
                    @input="updateFilteredLeaseApplies"
                  ></md-input>
                </md-field>
              </div>

              <div class="md-layout-item md-size-10">
                <md-field>
                  <label>{{ stateHeader }}</label>
                  <md-select
                    v-model="filters.state"
                    @input="updateFilteredLeaseApplies"
                  >
                    <md-option
                      v-for="option in filterStateOptions"
                      :key="option"
                      :value="option"
                      >{{ option }}</md-option
                    >
                  </md-select>
                </md-field>
              </div>
              <div class="md-layout-item md-size-10">
                <md-field>
                  <label>{{ returnMessageHeader }}</label>
                  <md-input
                    v-model="filters.returnMessage"
                    @input="updateFilteredLeaseApplies"
                  ></md-input>
                </md-field>
              </div>
              <div class="md-layout-item md-size-5"></div>
            </div>
            <div
              style="text-align: center"
              v-if="isLoading"
            >
              <md-progress-spinner
                :md-diameter="100"
                :md-stroke="10"
                md-mode="indeterminate"
              ></md-progress-spinner>
            </div>
            <div v-if="!isLoading">
              <div
                class="md-layout"
                style="padding-left: 10px"
                table-header-color="green"
                v-for="(item, index) in paginatedData"
                :key="index"
              >
                <div class="md-layout-item md-size-5">
                  <md-field>
                    <md-input
                      v-model="item.id"
                      disabled
                    ></md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-20">
                  <md-field>
                    <md-input
                      v-model="item.createdTime"
                      disabled
                    ></md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-25">
                  <md-field>
                    <md-input
                      v-model="item.goodsInfo"
                      disabled
                    ></md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-25">
                  <md-field>
                    <md-input
                      v-model="item.goodsUsage"
                      disabled
                    ></md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-10">
                  <md-field>
                    <md-input v-model="item.state" disabled>
                    </md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-10">
                  <md-field>
                    <md-input
                      v-model="item.returnMessage"
                      disabled
                    >
                    </md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-5">
                  <md-button
                    class="md-just-icon md-success"
                    :style="{
                      textAlign: 'right',
                      display:
                        item.state === '租赁中'
                          ? 'block'
                          : 'none',
                    }"
                    @click="setReturn(item)"
                  >
                    <md-icon>done_outline</md-icon
                    ><md-tooltip
                      >归还</md-tooltip
                    ></md-button
                  >
                </div>
              </div>
            </div>
          </md-card-content>
          <div
            style="
              display: flex;
              justify-content: space-between;
              align-items: center;
            "
            v-if="!isAdding"
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
                v-if="!isAdding"
                @click="exportFilteredLeaseApplies"
                ><md-icon>download</md-icon
                ><md-tooltip direction="top"
                  >导出</md-tooltip
                ></md-button
              >
              <md-button
                class="md-just-icon md-success"
                @click="enableAdding"
                ><md-icon>add</md-icon
                ><md-tooltip direction="top"
                  >新增租赁申请</md-tooltip
                ></md-button
              >
            </div>
            <div style="padding-right: 5%">
              <span>
                第 {{ currentPage }} 页，总计
                {{ filteredLeaseApplies.length }} 条，{{
                  totalPages
                }}
                页
              </span>
            </div>
          </div>

          <!-- 新增确认与取消按钮 -->
          <div
            class="md-layout-item md-size-100 text-right"
            v-if="isAdding"
          >
            <md-button
              class="md-just-icon md-success"
              @click="confirmAdding"
              ><md-icon>check</md-icon
              ><md-tooltip md-direction="top"
                >确认</md-tooltip
              ></md-button
            >
            <md-button
              class="md-just-icon md-white"
              @click="cancelAdding"
              ><md-icon>close</md-icon
              ><md-tooltip md-direction="top"
                >取消</md-tooltip
              ></md-button
            >
          </div>
          <div
            class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
            v-if="isAdding"
          >
            <md-card>
              <md-card-header data-background-color="green">
                <h4 class="title">新增租赁申请</h4>
              </md-card-header>
              <md-card-content>
                <div
                  class="md-layout-item md-size-100 md-size-100"
                >
                  <md-field>
                    <label>{{ goodsInfoHeader }}</label>
                    <md-textarea
                      v-model="addingLeaseApply.goodsInfo"
                    ></md-textarea>
                  </md-field>
                </div>
                <div
                  class="md-layout-item md-size-100 md-size-100"
                >
                  <md-field>
                    <label>{{ goodsUsageHeader }}</label>
                    <md-textarea
                      v-model="addingLeaseApply.goodsUsage"
                    ></md-textarea>
                  </md-field>
                </div>
              </md-card-content>
            </md-card>
          </div>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      idHeader: "编号",
      applicantHeader: "申请人",
      phoneHeader: "手机",
      goodsInfoHeader: "物资信息",
      createdTimeHeader: "创建时间",
      returnMessageHeader: "批示信息",
      goodsUsageHeader: "物资用途",
      stateHeader: "状态",

      stateOptions: [
        "待确认",
        "租赁中",
        "拒绝",
        "已结束",
        "归还中",
      ],
      leaseApplies: [],

      filters: {
        id: "",
        applicant: "",
        phone: "",
        createdTime: "",
        goodsInfo: "",
        goodsUsage: "",
        state: "全部状态",
      },
      filterStateOptions: [
        "待确认",
        "租赁中",
        "拒绝",
        "已结束",
        "归还中",
        "全部状态",
      ],
      filteredLeaseApplies: [],

      isAdding: false,
      addingLeaseApply: null,

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
      return this.filteredLeaseApplies.slice(start, end);
    },
    totalPages() {
      return Math.ceil(
        this.filteredLeaseApplies.length / this.itemsPerPage
      );
    },
  },
  async mounted() {
    console.log("mounted");
    this.filteredLeaseApplies = this.leaseApplies;
    this.addingLeaseApply = this.defaultLeaseApply();
    this.updateLeaseApplies();
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    defaultLeaseApply() {
      return {
        id: null,
        userId: this.$store.state.user.id,
        applicant: this.$store.state.user.name,
        type: "",
        phone: this.$store.state.user.phone,
        goodsInfo: "",
        goodsUsage: "",
        state: "待确认",
      };
    },
    async setReturn(application) {
      console.log("setReturn");
      let req = {
        action: "setReturn",
        applicationId: application.id,
      };
      let res = await this.$Backend(req);
      if (res && res.result === "success") {
        console.log("setReturn success");
        await this.updateLeaseApplies();
      }
    },
    updateFilteredLeaseApplies() {
      console.log("updateFilteredLeaseApplies");
      console.log(this.filters);
      this.filteredLeaseApplies = this.leaseApplies.filter(
        (leaseApply) =>
          (this.filters.applicant
            ? leaseApply.applicant.includes(
                this.filters.applicant
              )
            : true) &&
          (this.filters.phone
            ? leaseApply.phone.includes(this.filters.phone)
            : true) &&
          (this.filters.goodsInfo
            ? leaseApply.goodsInfo.includes(
                this.filters.goodsInfo
              )
            : true) &&
          (this.filters.goodsUsage
            ? leaseApply.goodsUsage.includes(
                this.filters.goodsUsage
              )
            : true) &&
          (this.filters.state
            ? this.filters.state === "全部状态" ||
              leaseApply.state.includes(this.filters.state)
            : true)
      );
    },
    async updateLeaseApplies() {
      console.log("getAllLeaseApplies of");
      this.isLoading = true;
      let req = {
        action: "getUserLeaseApplies",
        userId: this.$store.state.user.id,
      };
      console.log("req:", req);
      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        console.log("getAllLeaseApplies success");
        this.leaseApplies = [];
        for (let leaseApply of msg.applications) {
          leaseApply.applicant =
            this.$store.state.user.name;
          this.leaseApplies.push(leaseApply);
        }
        this.updateFilteredLeaseApplies();
      }
      this.isLoading = false;
    },
    async addLeaseApply(newLeaseApply) {
      console.log("addLeaseApply", newLeaseApply);
      let req = {
        action: "addLeaseApply",
        leaseApply: newLeaseApply,
      };
      console.log("req:", req);
      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        console.log("addLeaseApply success");
        newLeaseApply.id = msg.id;
        this.updateLeaseApplies();
      }
    },
    enableAdding() {
      console.log("enableAdding");
      this.isAdding = true;
    },
    cancelAdding() {
      console.log("cancelAdding");
      this.isAdding = false;
      this.addLeaseApply = this.defaultLeaseApply();
    },
    async confirmAdding() {
      console.log("confirmAdding");
      await this.addLeaseApply(this.addingLeaseApply);
      this.isAdding = false;
      this.addingLeaseApply = this.defaultLeaseApply();
      this.$notifyVue("新增租赁申请成功", "success");
    },
    exportFilteredLeaseApplies() {
      const modifiedData = this.filteredLeaseApplies.map(
        (item) => {
          return {
            申请人: item.applicant,
            手机: item.phone,
            物资信息: item.goodsInfo,
            物资用途: item.goodsUsage,
            申请状态: item.state,
          };
        }
      );

      this.$ExportFile(modifiedData, "租赁申请记录.xlsx");
      this.$notifyVue("导出租赁申请成功", "success");
    },
  },
};
</script>
