<template>
  <form>
    <md-card>
      <md-card-header
        :data-background-color="dataBackgroundColor"
      >
        <h4 class="title">个人信息</h4>
      </md-card-header>

      <md-card-content>
        <div class="md-layout">
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>公司</label>
              <md-input
                v-model="company"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>账户</label>
              <md-input v-model="id" disabled></md-input>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>姓名</label>
              <md-input
                v-model="name"
                type="text"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>身份</label>
              <md-input
                v-model="identity"
                type="text"
                disabled
              ></md-input>
            </md-field>
            <md-field>
              <label>部门</label>
              <md-input
                v-model="department_name"
                type="text"
                disabled
              ></md-input>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>邮箱</label>
              <md-input
                v-model="email"
                type="email"
                :disabled="!isEditing"
              ></md-input>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>联系方式</label>
              <md-input
                v-model="phone"
                type="text"
                :disabled="!isEditing"
              ></md-input>
            </md-field>
          </div>
          <div
            class="md-layout-item md-small-size-100 md-size-100"
          >
            <md-field>
              <label>密码</label>
              <md-input
                v-model="password"
                type="password"
                :disabled="!isEditing"
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-size-100">
            <md-field maxlength="5">
              <label>个人简介</label>
              <md-textarea
                v-model="aboutme"
                :disabled="!isEditing"
              ></md-textarea>
            </md-field>
          </div>
          <div
            class="md-layout-item md-size-100 text-right"
          >
            <md-button
              class="md-just-icon md-success"
              v-if="!isEditing"
              @click="enableEditing"
              ><md-icon>edit</md-icon
              ><md-tooltip md-direction="top"
                >编辑</md-tooltip
              ></md-button
            >
          </div>
          <div
            class="md-layout-item md-size-100 text-right"
            v-if="isEditing"
          >
            <md-button
              class="md-just-icon md-success"
              @click="confirmEditing"
              ><md-icon>check</md-icon
              ><md-tooltip md-direction="top"
                >确认</md-tooltip
              ></md-button
            >
            <md-button
              class="md-just-icon md-white"
              @click="cancelEditing"
              ><md-icon>close</md-icon
              ><md-tooltip md-direction="top"
                >取消</md-tooltip
              ></md-button
            >
          </div>
        </div>
      </md-card-content>
    </md-card>
  </form>
</template>
<script>
export default {
  name: "edit-profile-form",
  props: {
    dataBackgroundColor: {
      type: String,
      default: "",
    },
  },
  async mounted() {
    await this.getUserInfo();
  },
  data() {
    return {
      company: "Goods Manager 集团",
      id: null,
      name: null,
      identity: null,
      department_name: null,
      email: null,
      phone: null,
      password: null,
      aboutme: "这个人写数据库去了，什么都没留下……",
      isEditing: false,
    };
  },
  methods: {
    async getUserInfo() {
      console.log("getUserInfo");
      let req = {
        action: "getUserInfo",
        id: this.$store.state.user.id,
      };
      console.log("req:", req);

      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        this.id = msg.id;
        this.name = msg.name;
        this.identity = msg.identity;
        this.department_name = msg.department_name;
        this.email = msg.email;
        this.phone = msg.phone;
        this.password = msg.password;
      }
      console.log("this.isEditing:", this.isEditing);
    },
    async modifyUserInfo() {
      console.log("modifyUserInfo");
      let req = {
        action: "modifyUserInfo",
        id: this.$store.state.user.id,
        newEmail: this.email,
        newPhone: this.phone,
        newPassword: this.password,
      };
      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        await this.getUserInfo();
      }
    },

    enableEditing() {
      this.isEditing = true;
    },
    async cancelEditing() {
      await this.getUserInfo();
      this.isEditing = false;
    },
    async confirmEditing() {
      await this.modifyUserInfo();
      this.isEditing = false;
      this.$notifyVue("编辑成功");
    },
  },
};
</script>
<style></style>
