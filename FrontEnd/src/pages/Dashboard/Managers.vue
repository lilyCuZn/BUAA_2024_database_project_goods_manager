<template>
  <div>
    <md-card>
      <md-card-header data-background-color="orange">
        <h4 class="title">部门负责人</h4>
        <p class="category">火车跑得快，全靠车头带~</p>
      </md-card-header>
      <md-card-content>
        <md-table
          v-model="managers"
          :table-header-color="orange"
        >
          <md-table-row
            slot="md-table-row"
            slot-scope="{ item }"
          >
            <md-table-cell md-label="部门">{{
              item.department_name
            }}</md-table-cell>
            <md-table-cell md-label="负责人">{{
              item.name
            }}</md-table-cell>
            <md-table-cell md-label="电话">{{
              item.phone
            }}</md-table-cell>
            <md-table-cell md-label="邮箱">{{
              item.email
            }}</md-table-cell>
          </md-table-row>
        </md-table>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
export default {
  async mounted() {
    await this.updateManagers();
  },
  data() {
    return {
      managers: [
        {
          department_name_id: "物资管理部门",
          name: "张三",
          phone: "123456789",
          email: "database@buaa.edu.cn",
        },
      ],
    };
  },
  methods: {
    async updateManagers() {
      console.log("updateManagers");
      let req = {
        action: "getManagers",
      };
      let res = await this.$Backend(req);
      if (res && res.result === "success") {
        this.managers = res.principals;
      }
    },
  },
};
</script>
