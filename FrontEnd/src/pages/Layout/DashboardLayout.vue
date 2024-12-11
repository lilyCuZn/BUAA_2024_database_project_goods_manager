<template>
  <div
    class="wrapper"
    :class="{ 'nav-open': $sidebar.showSidebar }"
  >
    <notifications></notifications>

    <side-bar
      :sidebar-item-color="sidebarBackground"
      :sidebar-background-image="sidebarBackgroundImage"
    >
      <mobile-menu slot="content"></mobile-menu>
      <sidebar-link to="/dashboard">
        <md-icon>dashboard</md-icon>
        <p>工作面板</p>
      </sidebar-link>
      <sidebar-link to="/user">
        <md-icon>person</md-icon>
        <p>个人信息</p>
      </sidebar-link>
      <sidebar-link
        to="/userManage"
        v-if="
          this.$store.state.demo ||
          this.$store.state.user.identity === '管理员'
        "
      >
        <md-icon>manage_accounts</md-icon>
        <p>用户管理</p>
      </sidebar-link>
      <sidebar-link
        to="/approve"
        v-if="
          this.$store.state.demo ||
          this.$store.state.user.department_name ===
            '审批部门'
        "
      >
        <md-icon>flaky</md-icon>
        <p>审批部门</p>
      </sidebar-link>
      <sidebar-link
        to="/lease"
        v-if="
          this.$store.state.demo ||
          this.$store.state.user.department_name ===
            '外联部门'
        "
      >
        <md-icon>sell</md-icon>
        <p>外联部门</p>
      </sidebar-link>
      <sidebar-link
        to="/purchase"
        v-if="
          this.$store.state.demo ||
          this.$store.state.user.department_name ===
            '采购部门'
        "
      >
        <md-icon>shopping_bag</md-icon>
        <p>采购部门</p>
      </sidebar-link>
      <sidebar-link
        to="/warehouse"
        v-if="
          this.$store.state.demo ||
          this.$store.state.user.department_name ===
            '物资管理部门'
        "
      >
        <md-icon>warehouse</md-icon>
        <p>物资管理部门</p>
      </sidebar-link>
    </side-bar>

    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content> </dashboard-content>
    </div>
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "@/pages/Layout/MobileMenu.vue";

export default {
  mounted() {
    console.log("state.user:", this.$store.state.user);
  },
  components: {
    TopNavbar,
    DashboardContent,
    MobileMenu,
  },
  data() {
    return {
      sidebarBackground: "green",
      sidebarBackgroundImage: require("@/assets/img/sidebar-2.jpg"),
    };
  },
};
</script>
