<template>
  <div>
    <nav-tabs-card>
      <template slot="content">
        <span class="md-nav-tabs-title">任务:</span>
        <md-tabs
          class="md-success"
          md-alignment="left"
          :md-active-tab="activeTab"
        >
          <md-tab
            id="approve"
            md-label="审批部门"
            md-icon="flaky"
          >
            <md-table v-model="approveMsg">
              <md-table-empty-state
                :md-description="goodJob"
              >
                <img :src="gif" style="height: 150px" />
              </md-table-empty-state>
              <md-table-row
                slot="md-table-row"
                slot-scope="{ item }"
              >
                <md-table-cell>{{
                  item.task
                }}</md-table-cell>
                <md-table-cell>
                  <md-button
                    v-if="item.removeMsg"
                    class="md-just-icon md-success"
                    @click="removeMsg(item.id)"
                    ><md-icon>check</md-icon
                    ><md-tooltip
                      >完成</md-tooltip
                    ></md-button
                  >
                </md-table-cell>
              </md-table-row>
            </md-table>
          </md-tab>
          <md-tab
            id="purchase"
            md-label="采购部门"
            md-icon="shopping_bag"
          >
            <md-table v-model="purchaseMsg">
              <md-table-empty-state
                :md-description="goodJob"
              >
                <img :src="gif" style="height: 150px" />
              </md-table-empty-state>
              <md-table-row
                slot="md-table-row"
                slot-scope="{ item }"
              >
                <md-table-cell>{{
                  item.task
                }}</md-table-cell>
                <md-table-cell>
                  <md-button
                    v-if="item.removeMsg === 'true'"
                    class="md-just-icon md-success"
                    @click="removeMsg(item.id)"
                    ><md-icon>check</md-icon
                    ><md-tooltip
                      >完成</md-tooltip
                    ></md-button
                  >
                </md-table-cell>
              </md-table-row>
            </md-table>
          </md-tab>
          <md-tab
            id="storage"
            md-label="物资管理部门"
            md-icon="warehouse"
          >
            <md-table v-model="storageMsg">
              <md-table-empty-state
                :md-description="goodJob"
              >
                <img :src="gif" style="height: 150px" />
              </md-table-empty-state>
              <md-table-row
                slot="md-table-row"
                slot-scope="{ item }"
              >
                <md-table-cell>{{
                  item.task
                }}</md-table-cell>
                <md-table-cell>
                  <md-button
                    v-if="item.removeMsg === 'true'"
                    class="md-just-icon md-success"
                    @click="removeMsg(item.id)"
                    ><md-icon>check</md-icon
                    ><md-tooltip
                      >完成</md-tooltip
                    ></md-button
                  >
                </md-table-cell>
              </md-table-row>
            </md-table>
          </md-tab>
        </md-tabs>
      </template>
    </nav-tabs-card>
  </div>
</template>

<script>
import { NavTabsCard } from "@/components";
import { remove } from "lodash";
export default {
  async mounted() {
    this.initActiveTab();
    await this.updateMsg();
  },
  components: {
    NavTabsCard,
  },
  data() {
    return {
      activeTab: "approve",
      approveMsg: [],
      purchaseMsg: [],
      storageMsg: [],
      gif: require("@/assets/gif/goodJob.gif"),
      goodJob: "恭喜你们，完成所有任务！",
    };
  },
  methods: {
    initActiveTab() {
      console.log("initActiveTab");
      let department =
        this.$store.state.user.department_name;

      if (department === "审批部门") {
        this.activeTab = "approve";
      } else if (department === "采购部门") {
        console.log("purchase");
        this.activeTab = "purchase";
      } else if (department === "物资管理部门") {
        this.activeTab = "storage";
      }
    },
    async updateMsg() {
      console.log("updateMsg");
      let req = {
        action: "getTasks",
      };
      let res = await this.$Backend(req);
      if (res && res.result === "success") {
        console.log("updateMsg", res);
        this.approveMsg = res.approveMsg;
        this.purchaseMsg = res.purchaseMsg;
        this.storageMsg = res.storageMsg;
      }
    },
    async removeMsg(id) {
      console.log("removeMsg");
      let req = {
        action: "removeMsg",
        id: id,
      };
      let res = await this.$Backend(req);
      if (res && res.result === "success") {
        await this.updateMsg();
      }
    },
  },
};
</script>
