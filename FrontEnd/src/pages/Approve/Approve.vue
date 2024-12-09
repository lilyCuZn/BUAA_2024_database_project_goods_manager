<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item">
        <nav-tabs-card>
          <template slot="content">
            <span class="md-nav-tabs-title">审批记录:</span>
            <md-tabs
              class="md-success"
              md-alignment="right"
              @md-changed="update"
            >
              <!-- 待确认 -->
              <md-tab
                id="pending tab"
                md-label="待确认"
                md-icon="pending"
              >
                <PendingApprove ref="PendingApprove" />
              </md-tab>
              <!-- 物资管理部门审批 -->
              <md-tab
                id="storage tab"
                md-label="物资管理部门"
                md-icon="warehouse"
              >
                <StorageApprove ref="StorageApprove" />
              </md-tab>
              <!-- 采购部门审批 -->
              <md-tab
                id="purchase tab"
                md-label="采购部门"
                md-icon="shopping_bag"
              >
                <PurchaseApprove ref="PurchaseApprove" />
              </md-tab>
            </md-tabs>
          </template>
        </nav-tabs-card>
      </div>
    </div>
  </div>
</template>

<script>
import { NavTabsCard } from "@/components";
import PendingApprove from "@/pages/Approve/PendingApprove.vue";
import PurchaseApprove from "./PurchaseApprove.vue";
import StorageApprove from "./StorageApprove.vue";
export default {
  components: {
    PendingApprove,
    PurchaseApprove,
    StorageApprove,
    NavTabsCard,
  },
  async mounted() {},
  data() {
    return {};
  },
  methods: {
    update(activeTab) {
      console.log("onTabChange");
      if (activeTab === "pending tab") {
        this.$refs.PendingApprove.updatePendingApproves();
      } else if (activeTab === "storage tab") {
        this.$refs.StorageApprove.updateStorageApproves();
      } else if (activeTab === "purchase tab") {
        this.$refs.PurchaseApprove.updatePurchaseApproves();
      }
    },
  },
};
</script>
