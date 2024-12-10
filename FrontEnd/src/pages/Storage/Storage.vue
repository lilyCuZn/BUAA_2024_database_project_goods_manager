<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item">
        <md-card class="md-card-nav-tabs">
          <md-card-content>
            <span class="md-nav-tabs-title">物资管理:</span>

            <md-tabs
              class="md-success"
              md-alignment="right"
              @md-changed="update"
            >
              <md-tab
                id="goods list"
                md-label="物资列表"
                md-icon="list"
              >
                <WareHouse ref="WareHouse" />
              </md-tab>
              <!-- 维护申请 -->
              <md-tab
                id="maintain apply"
                md-label="维护申请"
                md-icon="workspace_premium"
              >
                <MaintainApplication
                  ref="MaintainApplication"
                />
              </md-tab>
              <!-- 维护记录 -->
              <md-tab
                id="maintain record"
                md-label="维护记录"
                md-icon="format_list_bulleted"
              >
                <MaintainRecord ref="MaintainRecord" />
              </md-tab>
              <!-- 租赁申请 -->
              <md-tab
                id="lease application"
                md-label="租赁申请"
                md-icon="format_list_bulleted"
              >
                <LeaseApplication ref="LeaseApplication" />
              </md-tab>
            </md-tabs>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import WareHouse from "./WareHouse.vue";
import MaintainApplication from "./MaintainApplication.vue";
import MaintainRecord from "./MaintainRecord.vue";
import { update } from "lodash";
import LeaseApplication from "./LeaseApplication.vue";
export default {
  components: {
    WareHouse,
    MaintainApplication,
    MaintainRecord,
    LeaseApplication,
  },
  async mounted() {
    // await this.getGoods();
  },
  data() {
    return {};
  },
  methods: {
    update(activeTab) {
      if (activeTab === "goods list") {
        this.$refs.WareHouse.updateGoods();
      } else if (activeTab === "maintain apply") {
        this.$refs.MaintainApplication.updateMaintainApplications();
      } else if (activeTab === "maintain record") {
        this.$refs.MaintainRecord.updateMaintainRecords();
      } else if (activeTab === "lease application") {
        this.$refs.LeaseApplication.updateLeaseApplications();
      }
    },
  },
};
</script>
