<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item">
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">使用说明</h4>
            <p class="category">
              感谢您对我们的支持！
              <i class="fa fa-heart heart"></i>
            </p>
          </md-card-header>
          <md-card-content>
            <div class="md-layout">
              <div class="md-layout-item md-size-100">
                <h3>产品概况</h3>
                <div data-notify="container">
                  <p data-notify="message">
                    本产品是由
                    <a
                      href="https://github.com/lilyCuZn"
                      target="_blank"
                      >lilyCuZn</a
                    >、<a
                      href="https://github.com/Ascendira"
                      target="_blank"
                      >Ascendira</a
                    >
                    和
                    <a
                      href="https://github.com/Foolish-Han"
                      target="_blank"
                      >Foolish-Han</a
                    >开发的，基于 vue 前端、django 后端和
                    GaussDB
                    数据库的，面向企业级用户的物资管理系统。致力于解决企业物资管理中物资生命周期不明、部门职能分工耦合、成员权限划分混乱的痛点，提高企业物资管理的效率。
                  </p>
                  <p>
                    为了更好地展示系统效果，当前系统处于演示模式，即审批、外联、采购、物资管理四大部门的接口都将暴露给访客体验。在真实生产环境中，只有相应部门的用户才能访问相应接口。
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-size-100">
                <h3>四种部门</h3>
              </div>
              <div class="md-layout-item md-size-50">
                <h4>审批部门</h4>
                <div
                  data-notify="container"
                  class="alert alert-warning"
                >
                  <p data-notify="message">
                    该部门负责根据公司的规章制度、财务状况、市场需求等因素，对物资管理部门提交的维护物资请求和采购部门提交的采购物资请求进行审批。
                  </p>
                  <p data-notify="message">
                    该界面提供了对待确认的审批执行批准或驳回操作的接口，并提供了查看部门审批历史记录及导出详细信息的功能。
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-size-50">
                <h4>采购部门</h4>
                <div
                  data-notify="container"
                  class="alert alert-primary"
                >
                  <p data-notify="message">
                    该部门负责根据公司生产运营的实际需求决定是否进行物资采购，以及采购的物资种类、数量等，报经审批部门通过后，方可凭借申请进行实际采购并记录。
                  </p>
                  <p data-notify="message">
                    该界面提供了发起采购申请、为通过的采购申请创建采购记录、完成采购并将物资入库等操作的接口，并提供了查看部门采购申请和记录及导出详细信息的功能。
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-size-50">
                <h4>外联部门</h4>
                <div
                  data-notify="container"
                  class="alert alert-info"
                >
                  <p data-notify="message">
                    该部门是公司物资管理系统暴露给其他部门的、用于实现以租赁物资为代表的物资相关业务的接口，向物资管理部门发起租赁申请并等待批准后可租赁物资，物资使用完毕后可向物资管理部门归还物资并查看检查结果。
                  </p>
                  <p data-notify="message">
                    该界面提供了发起租赁申请、归还物资等操作的接口，并提供了查看部门租赁记录及导出详细信息的功能。
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-size-50">
                <h4>物资管理部门</h4>
                <div
                  data-notify="container"
                  class="alert alert-danger"
                >
                  <p data-notify="message">
                    该部门是本系统的核心部门。可以总览库中所有物资的信息，包括物资的种类、状态、采购信息等；可以向审批部门发起维护物资请求，对库中状态为损坏的物资进行检修维护；可以处理外联部门发起的租赁申请，根据库中物资的状态决定是否批准及选择借出物资，并对归还的物资状态进行检查入库。
                  </p>
                  <p data-notify="message">
                    该界面提供了查看物资、发起维护申请、填写维护记录和处理租赁申请等操作的接口，并提供了查看物资信息、维护历史、租赁申请历史及导出详细信息的功能。
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-size-100">
                <h3>三类流程</h3>
              </div>
              <div class="md-layout-item md-size-40">
                <h4>物资采购</h4>
                <img :src="purchase_flow" alt="采购流程" />
              </div>
              <div class="md-layout-item md-size-60">
                <h4>物资维护</h4>
                <img :src="maintain_flow" alt="维护流程" />
              </div>
              <div class="md-layout-item md-size-100">
                <h4>物资租赁</h4>
                <img :src="lease_flow" alt="租赁流程" />
              </div>
              <div class="md-layout-item md-size-100">
                <h3>两种身份</h3>
              </div>
              <div class="md-layout-item md-size-100">
                <div data-notify="container">
                  <p data-notify="message">
                    管理员用户负责与我方开发人员对接、确定公司的具体业务需求并负责日常维护操作，具有总览系统成员信息，创建用户、删除用户、修改用户信息和重置密码等操作的权限。用户管理界面提供了相关操作的接口并提供了文件导入导出的功能。
                  </p>
                  <p data-notify="message">
                    普通用户负责根据所属部门执行相应的业务操作，可以在个人信息界面有限地修改个人信息，包括电话、邮箱、密码等。
                  </p>
                </div>
              </div>
            </div>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      type: ["", "info", "success", "warning", "danger"],
      notifications: {
        topCenter: false,
      },
      purchase_flow: require("@/assets/img/purchase_flow.png"),
      maintain_flow: require("@/assets/img/maintain_flow.png"),
      lease_flow: require("@/assets/img/lease_flow.png"),
      visible: false,
      currentImg: "",
    };
  },
  methods: {
    notifyVue(verticalAlign, horizontalAlign) {
      var color = Math.floor(Math.random() * 4 + 1);
      this.$notify({
        message:
          "Welcome to <b>Material Dashboard</b> - a beautiful freebie for every web developer.",
        horizontalAlign: horizontalAlign,
        verticalAlign: verticalAlign,
        type: this.type[color],
      });
    },
  },
};
</script>
