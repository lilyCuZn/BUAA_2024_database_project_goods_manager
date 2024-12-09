<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item">
        <nav-tabs-card>
          <template slot="content">
            <span class="md-nav-tabs-title">采购管理:</span>
            <md-tabs
              class="md-success"
              md-alignment="right"
              @md-changed="update"
            >
              <md-tab
                id="purchase application"
                md-label="采购申请"
                md-icon="workspace_premium"
              >
                <PurchaseApplication
                  ref="PurchaseApplication"
                />
              </md-tab>
              <md-tab
                id="purchase record"
                md-label="采购记录"
                md-icon="format_list_bulleted"
              >
                <PurchaseRecord ref="PurchaseRecord" />
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
import PurchaseApplication from "./PurchaseApplication.vue";
import PurchaseRecord from "./PurchaseRecord.vue";
export default {
  components: {
    NavTabsCard,
    PurchaseRecord,
    PurchaseApplication,
  },
  data() {
    return {};
  },
  async mounted() {},
  methods: {
    update(activeTab) {
      if (activeTab === "purchase application") {
        this.$refs.PurchaseApplication.updatePurchaseApplications();
      } else if (activeTab === "purchase record") {
        this.$refs.PurchaseRecord.updatePurchaseRecords();
      }
    },
  },
};
</script>
