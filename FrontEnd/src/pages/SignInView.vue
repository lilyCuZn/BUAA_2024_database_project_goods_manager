<script>
import MyHeader from "@/examples/Header.vue";
import MaterialInput from "@/components/MaterialInput.vue";
import MaterialButton from "@/components/MaterialButton.vue";
import setMaterialInput from "@/assets/js/material-input";
export default {
  components: {
    MyHeader,
    MaterialInput,
    MaterialButton,
  },
  data() {
    return {
      id: "",
      password: "",
      errorMsg: null,
    };
  },
  mounted() {
    setMaterialInput();
  },
  methods: {
    async check(userInfo) {
      userInfo.action = "login";
      const result = await this.$Backend(userInfo);
      console.log("check msg:", result);
      return result;
    },
    async handleSubmit() {
      const userInfo = {
        id: this.id,
        password: this.password,
      };
      let msg = await this.check(userInfo);

      console.log("msg:", msg);
      if (msg.result === "success") {
        console.log("login success");
        this.$store.dispatch("login", msg.user);
        this.$router.push("/dashboard");
      } else if (msg.result === "invalid account") {
        console.log("id error");
        this.errorMsg = "账户不存在，请联系管理员注册！";
      } else if (msg.result === "wrong password") {
        console.log("password error");
        this.errorMsg = "密码错误，请重新输入！";
      } else {
        console.log("network error");
        this.errorMsg = "网络错误，请联系管理员！";
      }
    },
  },
};
</script>
<template>
  <MyHeader>
    <div
      class="page-header align-items-start min-vh-100"
      :style="{
        backgroundImage:
          'url(https://images.unsplash.com/photo-1497294815431-9365093b7331?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1950&q=80)',
      }"
      loading="lazy"
    >
      <span class="mask bg-gradient-dark opacity-6"></span>
      <div class="container my-auto">
        <div class="col-lg-4 col-md-8 col-12 mx-auto">
          <div class="card z-index-0 fadeIn3 fadeInBottom">
            <div class="card-body">
              <div style="margin-top: 5%">
                <h2
                  class="font-weight-bolder text-center mt-2 mb-0"
                  style="
                    font-family: 'Noto Serif SC', serif;
                  "
                >
                  Goods Manager
                </h2>
              </div>
              <form
                role="form"
                class="text-start"
                @submit.prevent="handleSubmit"
              >
                <MaterialInput
                  id="id"
                  class="input-group-outline my-3"
                  :label="{
                    text: '账号',
                    class: 'form-label',
                  }"
                  v-model="id"
                  type="text"
                />
                <MaterialInput
                  id="password"
                  class="input-group-outline mb-3"
                  :label="{
                    text: '密码',
                    class: 'form-label',
                  }"
                  v-model="password"
                  type="password"
                />

                <div
                  v-if="errorMsg"
                  class="text-danger text-center mb-3"
                >
                  {{ errorMsg }}
                </div>
                <div class="text-center">
                  <MaterialButton
                    class="my-4 mb-2"
                    variant="gradient"
                    color="success"
                    type="submit"
                    fullWidth
                  >
                    登录
                  </MaterialButton>
                </div>
                <p class="mt-4 text-sm text-center">
                  没有账户？忘记密码？快去联系管理员吧~
                </p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MyHeader>
</template>
