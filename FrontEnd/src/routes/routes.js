import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import Dashboard from "@/pages/Dashboard/Dashboard.vue";
import UserProfile from "@/pages/UserProfile.vue";
import TableList from "@/pages/TableList.vue";
import Notifications from "@/pages/Notifications.vue";
import SignInView from "@/pages/SignInView.vue";
import UerManage from "@/pages/UerManage.vue";
import Lease from "@/pages/Lease.vue";
import Approve from "@/pages/Approve/Approve.vue";
import Purchase from "@/pages/Purchase/Purchase.vue";
import WareHouse from "@/pages/Storage/Storage.vue";
const routes = [
  {
    path: "/",
    redirect: "/signin",
    component: DashboardLayout,
    children: [
      {
        path: "warehouse",
        name: "物资管理部门",
        component: WareHouse,
      },
      {
        path: "purchase",
        name: "采购部门",
        component: Purchase,
      },
      {
        path: "approve",
        name: "审批部门",
        component: Approve,
      },
      {
        path: "lease",
        name: "租赁申请",
        component: Lease,
      },
      {
        path: "dashboard",
        name: "工作面板",
        component: Dashboard,
      },
      {
        path: "user",
        name: "个人信息",
        component: UserProfile,
      },
      {
        path: "table",
        name: "Table List",
        component: TableList,
      },
      {
        path: "/userManage",
        name: "用户管理",
        component: UerManage,
      },
      {
        path: "notifications",
        name: "Notifications",
        component: Notifications,
      },
    ],
  },
  {
    path: "/signin",
    component: SignInView,
  },
];

export default routes;
