<template>
  <div class="content">
    <div class="md-layout">
      <!-- 编辑用户表 -->
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      >
        <md-card>
          <!-- 卡片头部 -->
          <md-card-header data-background-color="green">
            <div
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
              "
            >
              <div>
                <h4 class="title">用户管理</h4>
                <p class="category">
                  试着添加一些过滤条件，查看、添加、修改、删除用户信息，默认密码为：{{
                    defaultPassword
                  }}
                </p>
              </div>
              <div><md-icon>search</md-icon></div>
            </div>
          </md-card-header>
          <!-- 过滤条件 -->
          <md-card-content>
            <div class="md-layout">
              <div
                class="md-layout-item md-size-10"
                v-if="isDeleting || isResettingPassword"
              ></div>
              <div class="md-layout-item md-size-10">
                <md-field>
                  <label>账户</label>
                  <md-input
                    v-model="filters.id"
                    @input="updateFilteredUsers"
                  ></md-input>
                </md-field>
              </div>
              <div class="md-layout-item md-size-10">
                <md-field>
                  <label>姓名</label>
                  <md-input
                    v-model="filters.name"
                    type="text"
                    @input="updateFilteredUsers"
                  ></md-input>
                </md-field>
              </div>
              <div class="md-layout-item md-size-15">
                <md-field>
                  <label>身份</label>
                  <md-select
                    v-model="filters.identity"
                    @md-selected="updateFilteredUsers"
                  >
                    <md-option
                      v-for="option in filterIdentityOptions"
                      :key="option"
                      :value="option"
                      >{{ option }}</md-option
                    >
                  </md-select>
                </md-field>
              </div>
              <div class="md-layout-item md-size-15">
                <md-field>
                  <label>部门</label>
                  <md-select
                    v-model="filters.department_name_id"
                    @md-selected="updateFilteredUsers"
                  >
                    <md-option
                      v-for="option in filterdepartment_name_idOptions"
                      :key="option"
                      :value="option"
                      >{{ option }}</md-option
                    >
                  </md-select>
                </md-field>
              </div>
              <div class="md-layout-item md-size-20">
                <md-field>
                  <label>邮箱</label>
                  <md-input
                    v-model="filters.email"
                    @input="updateFilteredUsers"
                    type="email"
                  ></md-input>
                </md-field>
              </div>
              <div class="md-layout-item md-size-20">
                <md-field>
                  <label>电话</label>
                  <md-input
                    v-model="filters.phone"
                    type="text"
                    @input="updateFilteredUsers"
                  ></md-input>
                </md-field>
              </div>
            </div>
          </md-card-content>
          <!-- 用户表 -->
          <md-card-content>
            <div
              style="text-align: center"
              v-if="isLoading"
            >
              <md-progress-spinner
                :md-diameter="100"
                :md-stroke="10"
                md-mode="indeterminate"
              ></md-progress-spinner>
            </div>

            <div v-if="!isLoading">
              <div
                class="md-layout"
                v-for="(item, index) in paginatedData"
                :key="index"
              >
                <div
                  class="md-layout-item md-size-10"
                  v-if="isDeleting || isResettingPassword"
                >
                  <md-checkbox
                    v-model="selectedUsers"
                    :disabled="item.identity === '管理员'"
                    :value="item.id"
                  ></md-checkbox>
                </div>
                <div class="md-layout-item md-size-10">
                  <md-field>
                    <md-input
                      v-model="item.id"
                      type="text"
                      disabled
                    ></md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-10">
                  <md-field>
                    <md-input
                      v-model="item.name"
                      type="text"
                      :disabled="disabledItem(item)"
                      @input="markedAsModified(item)"
                    ></md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-15">
                  <md-field>
                    <md-select
                      v-model="item.identity"
                      :disabled="disabledItem(item)"
                      @input="
                        markedAsModified(item, $event)
                      "
                    >
                      <md-option
                        v-for="option in identityOptions"
                        :key="option"
                        :value="option"
                        >{{ option }}</md-option
                      >
                    </md-select>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-15">
                  <md-field>
                    <md-select
                      v-model="item.department_name_id"
                      :disabled="disabledItem(item)"
                      @input="
                        markedAsModified(item, $event)
                      "
                    >
                      <md-option
                        v-for="option in department_name_idOptions"
                        :key="option"
                        :value="option"
                        >{{ option }}</md-option
                      >
                    </md-select>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-20">
                  <md-field>
                    <md-input
                      v-model="item.email"
                      type="email"
                      :disabled="disabledItem(item)"
                      @input="markedAsModified(item)"
                    ></md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-size-20">
                  <md-field>
                    <md-input
                      v-model="item.phone"
                      type="phone"
                      :disabled="disabledItem(item)"
                      @input="markedAsModified(item)"
                    ></md-input>
                  </md-field>
                </div>
              </div>
            </div>
          </md-card-content>
          <!-- 添加、删除、编辑、导出、重置密码按钮 -->
          <div
            style="
              display: flex;
              justify-content: space-between;
              align-items: center;
            "
          >
            <div>
              <md-button
                class="md-just-icon md-success"
                @click="changePage(currentPage - 1)"
                :disabled="currentPage <= 1"
              >
                <md-icon>west</md-icon>
                <md-tooltip md-direction="top"
                  >上一页</md-tooltip
                >
              </md-button>
              <md-button
                class="md-just-icon md-success"
                @click="changePage(currentPage + 1)"
                :disabled="currentPage >= totalPages"
              >
                <md-icon>east</md-icon>
                <md-tooltip md-direction="top"
                  >下一页</md-tooltip
                >
              </md-button>
              <md-button
                v-if="isDeleting || isResettingPassword"
                class="md-just-icon md-success"
                @click="selectAll"
              >
                <md-icon>select_all</md-icon>
                <md-tooltip md-direction="top"
                  >全部选择</md-tooltip
                >
              </md-button>
              <md-button
                v-if="isDeleting || isResettingPassword"
                class="md-just-icon md-success"
                @click="selectedUsers = []"
              >
                <md-icon>delete</md-icon>
                <md-tooltip md-direction="top"
                  >全部取消</md-tooltip
                >
              </md-button>
              <md-button
                v-if="!isWorking"
                class="md-just-icon md-success"
                @click="enableAdding"
                ><md-icon>add</md-icon>
                <md-tooltip md-direction="top"
                  >添加</md-tooltip
                ></md-button
              >
              <md-button
                v-if="!isWorking"
                class="md-just-icon md-success"
                @click="enableDeleting"
                ><md-icon>remove</md-icon>
                <md-tooltip md-direction="top"
                  >删除</md-tooltip
                >
              </md-button>
              <md-button
                v-if="!isWorking"
                class="md-just-icon md-success"
                @click="enableEditing"
                ><md-icon>edit</md-icon
                ><md-tooltip md-direction="top"
                  >编辑</md-tooltip
                ></md-button
              >

              <md-button
                v-if="!isWorking"
                class="md-just-icon md-success"
                @click="enableResettingPassword"
                ><md-icon>lock_reset</md-icon
                ><md-tooltip md-direction="top"
                  >重置密码</md-tooltip
                ></md-button
              >
              <md-button
                v-if="!isWorking"
                class="md-just-icon md-success"
                @click="exportFilteredUsers"
                ><md-icon>download</md-icon
                ><md-tooltip md-direction="top"
                  >导出</md-tooltip
                ></md-button
              >
            </div>

            <div style="padding-right: 5%">
              <span>
                第 {{ currentPage }} 页，总计
                {{ filteredUsers.length }} 条，{{
                  totalPages
                }}
                页
              </span>
              <span
                v-if="isDeleting || isResettingPassword"
              >
                ， 已选择 {{ selectedUsers.length }} 项
              </span>
            </div>
          </div>
          <div
            class="md-layout-item md-size-100 text-right"
          ></div>
          <!-- 编辑确认与取消按钮 -->
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
            <!-- 删除确认与取消按钮 -->
          </div>
          <div
            class="md-layout-item md-size-100 text-right"
            v-if="isDeleting"
          >
            <md-button
              class="md-just-icon md-success"
              @click="confirmDeleting"
              ><md-icon>check</md-icon
              ><md-tooltip md-direction="top"
                >确认</md-tooltip
              ></md-button
            >
            <md-button
              class="md-just-icon md-white"
              @click="cancelDeleting"
              ><md-icon>close</md-icon
              ><md-tooltip md-direction="top"
                >取消</md-tooltip
              ></md-button
            >
          </div>
          <!-- 重置密码确认与取消按钮 -->
          <div
            class="md-layout-item md-size-100 text-right"
            v-if="isResettingPassword"
          >
            <md-button
              class="md-just-icon md-success"
              @click="confirmResettingPassword"
              ><md-icon>check</md-icon
              ><md-tooltip md-direction="top"
                >确认</md-tooltip
              ></md-button
            >
            <md-button
              class="md-just-icon md-white"
              @click="cancelResettingPassword"
              ><md-icon>close</md-icon
              ><md-tooltip md-direction="top"
                >取消</md-tooltip
              ></md-button
            >
          </div>
          <!-- 新增确认与取消按钮 -->
          <div
            class="md-layout-item md-size-100 text-right"
            v-if="isAdding"
          >
            <md-button
              class="md-just-icon md-success"
              @click="confirmAdding"
              ><md-icon>check</md-icon
              ><md-tooltip md-direction="top"
                >确认</md-tooltip
              ></md-button
            >
            <md-button
              class="md-just-icon md-white"
              @click="cancelAdding"
              ><md-icon>close</md-icon
              ><md-tooltip md-direction="top"
                >取消</md-tooltip
              ></md-button
            >
          </div>
          <!-- 新增用户表 -->
          <div
            class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
            v-if="isAdding"
          >
            <md-card>
              <md-card-header data-background-color="green">
                <h4 class="title">新增用户表</h4>
                <p class="category">
                  试着下载模板文件并通过文件上传新用户信息，账户将由系统自动分配~
                </p>
              </md-card-header>
              <md-card-content>
                <div>
                  <md-table
                    v-model="addingUsers"
                    table-header-color="green"
                  >
                    <md-table-row
                      slot="md-table-row"
                      slot-scope="{ item }"
                    >
                      <md-table-cell :md-label="nameHeader">
                        <md-field>
                          <md-input
                            v-model="item.name"
                            type="text"
                          ></md-input>
                        </md-field>
                      </md-table-cell>
                      <md-table-cell
                        :md-label="identityHeader"
                      >
                        <md-field>
                          <md-select
                            v-model="item.identity"
                            @input="
                              markedAsModified(item, $event)
                            "
                          >
                            <md-option
                              v-for="option in identityOptions"
                              :key="option"
                              :value="option"
                              >{{ option }}</md-option
                            >
                          </md-select>
                        </md-field>
                      </md-table-cell>
                      <md-table-cell
                        :md-label="department_name_idHeader"
                      >
                        <md-field>
                          <md-select
                            v-model="
                              item.department_name_id
                            "
                            @input="
                              markedAsModified(item, $event)
                            "
                          >
                            <md-option
                              v-for="option in department_name_idOptions"
                              :key="option"
                              :value="option"
                              >{{ option }}</md-option
                            >
                          </md-select>
                        </md-field>
                      </md-table-cell>
                      <md-table-cell
                        :md-label="emailHeader"
                      >
                        <md-field>
                          <md-input
                            v-model="item.email"
                            type="email"
                          ></md-input>
                        </md-field>
                      </md-table-cell>
                      <md-table-cell
                        :md-label="phoneHeader"
                      >
                        <md-field>
                          <md-input
                            v-model="item.phone"
                            type="phone"
                          ></md-input>
                        </md-field>
                      </md-table-cell>
                    </md-table-row>
                  </md-table>
                </div>
              </md-card-content>
              <div
                class="md-layout-item md-size-100 text-right"
              >
                <md-button
                  @click="downloadTemplateFile"
                  class="md-just-icon md-success"
                  ><md-icon>download</md-icon
                  ><md-tooltip direction="top"
                    >下载模板文件</md-tooltip
                  ></md-button
                >
                <!-- 文件上传按钮 -->
                <md-button
                  @click="triggerFileInput"
                  class="md-just-icon md-success"
                  ><md-icon>upload</md-icon
                  ><md-tooltip direction="top"
                    >文件上传</md-tooltip
                  ></md-button
                >
                <input
                  type="file"
                  ref="fileInput"
                  style="display: none"
                  @change="handleUsersFile"
                />
                <!-- 增加表项按钮 -->
                <md-button
                  @click="increaseAddUser"
                  class="md-just-icon md-success"
                  ><md-icon>add</md-icon
                  ><md-tooltip direction="top"
                    >新增表项</md-tooltip
                  ></md-button
                >
                <!-- 减少表项按钮 -->
                <md-button
                  @click="decreaseAddUser"
                  class="md-just-icon md-success"
                  ><md-icon>remove</md-icon
                  ><md-tooltip direction="top"
                    >减少表项</md-tooltip
                  ></md-button
                >
              </div>
            </md-card>
          </div>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import cloneDeep from "lodash/cloneDeep";
import * as XLSX from "xlsx";
export default {
  data() {
    return {
      identityOptions: ["管理员", "普通用户"],
      department_name_idOptions: [
        "物资管理部门",
        "采购部门",
        "审批部门",
        "外联部门",
      ],
      filterIdentityOptions: [
        "管理员",
        "普通用户",
        "全部身份",
      ],
      filterdepartment_name_idOptions: [
        "物资管理部门",
        "采购部门",
        "审批部门",
        "外联部门",
        "全部部门",
      ],
      users: [],
      filters: {
        id: "",
        name: "",
        identity: "全部身份",
        department_name_id: "全部部门",
        email: "",
        phone: "",
        password: "",
      },
      filteredUsers: [],
      defaultNewUser: {
        name: "",
        identity: "普通用户",
        department_name_id: "物资管理部门",
        email: "",
        phone: "",
        password: "iloveworking",
      },
      idHeader: "账户",
      nameHeader: "姓名",
      identityHeader: "身份",
      department_name_idHeader: "部门",
      emailHeader: "邮箱",
      phoneHeader: "电话",
      passwordHeader: "密码",
      defaultPassword: "behappyeveryday",
      isEditing: false,
      isDeleting: false,
      isResettingPassword: false,
      isAdding: false,
      selectedUsers: [],
      addingUsers: [],
      currentPage: 1,
      itemsPerPage: 6,
      isLength: false,
      isLoading: false,
    };
  },
  async mounted() {
    console.log("mounted");
    this.defaultNewUser.password = this.defaultPassword;
    this.filteredUsers = this.users;
    console.log(
      "this.defaultNewUser:",
      this.defaultNewUser
    );
    console.log("this.addingUsers:", this.addingUsers);
    await this.updateUsersInfo();
  },
  computed: {
    isWorking() {
      return (
        this.isEditing ||
        this.isDeleting ||
        this.isAdding ||
        this.isResettingPassword
      );
    },
    paginatedData() {
      const start =
        (this.currentPage - 1) * this.itemsPerPage;
      const end = this.currentPage * this.itemsPerPage;
      console.log(
        "this.filteredUsers:",
        this.filteredUsers
      );
      let tmp = this.filteredUsers.slice(start, end);
      return tmp;
    },
    totalPages() {
      return Math.ceil(
        this.filteredUsers.length / this.itemsPerPage
      );
    },
  },
  methods: {
    disabledItem(item) {
      return (
        !this.isEditing ||
        (item.identity === "管理员" &&
          item.id !== this.$store.state.user.id)
      );
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    updateFilteredUsers() {
      console.log("updateFilteredUsers");
      console.log("this.filters:", this.filters);
      this.currentPage = 1;
      this.filteredUsers = this.users.filter((user) => {
        return (
          (this.filters.id
            ? user.id.includes(this.filters.id)
            : true) &&
          (this.filters.name
            ? user.name.includes(this.filters.name)
            : true) &&
          (this.filters.identity
            ? this.filters.identity === "全部身份" ||
              user.identity === this.filters.identity
            : true) &&
          (this.filters.department_name_id
            ? this.filters.department_name_id ===
                "全部部门" ||
              user.department_name_id ===
                this.filters.department_name_id
            : true) &&
          (this.filters.email
            ? user.email.includes(this.filters.email)
            : true) &&
          (this.filters.phone
            ? user.phone.includes(this.filters.phone)
            : true) &&
          (this.filters.password
            ? user.password.includes(this.filters.password)
            : true)
        );
      });
    },
    async updateUsersInfo() {
      console.log("getAllUsersInfo of");
      let req = {
        action: "getAllUsersInfo",
      };
      console.log("req:", req);
      this.isLoading = true;
      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        this.users = msg.usersList;
        this.updateFilteredUsers();
        console.log("users:", this.users);
        console.log("filteredUsers:", this.filteredUsers);
      }
      this.isLoading = false;
    },
    async resetUserInfo(targetid) {
      console.log("getUserInfo of", targetid);
      let req = {
        action: "getUserInfo",
        userid: targetid,
      };
      console.log("req:", req);
      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        const index = this.users.findIndex(
          (user) => user.id === targetid
        );
        if (index !== -1) {
          this.users[index].username = msg.name;
          this.users[index].identity = msg.identity;
          this.users[index].department_name_id =
            msg.department_name_id_name;
          this.users[index].email = msg.email;
          this.users[index].phone = msg.phone;
          this.users[index].password = msg.password;
        }
      }
    },
    async modifyUserInfo(targetUser) {
      console.log("admin modifyUserInfo of", targetUser.id);
      let req = {
        action: "adminModifyUserInfo",
        user: targetUser,
      };
      console.log("req:", req);
      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        console.log("modify success");
      }
    },
    async deleteUser(targetid) {
      console.log("deleteUser of", targetid);
      let req = {
        action: "deleteUser",
        id: targetid,
      };
      console.log("req:", req);
      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        console.log("delete success");
        this.users = this.users.filter(
          (user) => user.id !== targetid
        );
      }
    },
    async resetPassword(targetid) {
      console.log("resetPassword of", targetid);
      let req = {
        action: "resetPassword",
        id: targetid,
      };
      console.log("req:", req);
      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        console.log("reset success");
      }
      console.log("???");
    },
    async addUser(newUser) {
      console.log("addUser", newUser);
      let req = {
        action: "addMember",
        user: newUser,
      };
      console.log("req:", req);
      const msg = await this.$Backend(req);
      if (msg && msg.result === "success") {
        console.log("add success");
        this.users.push(msg.user);
        this.updateFilteredUsers();
        console.log("users:", this.users);
      }
    },
    enableEditing() {
      console.log("enableEditing");
      this.isEditing = true;
    },
    async cancelEditing() {
      console.log("cancelEditing");
      this.isEditing = false;
      for (const user of this.users) {
        if (user.modified) {
          await this.resetUserInfo(user.id);
          user.modified = false;
        }
      }
    },
    async confirmEditing() {
      console.log("confirmEditing");
      await this.submitChanges();
      this.isEditing = false;
      this.$notifyVue("修改成功!");
    },
    markedAsModified(user) {
      console.log(user.id, "markedAsModified");
      user.modified = true;
    },
    async submitChanges() {
      const modifiedUsers = this.users.filter(
        (user) => user.modified
      );
      for (const user of modifiedUsers) {
        console.log("submitting", user);
        await this.modifyUserInfo(user);
        user.modified = false;
      }
    },
    enableDeleting() {
      console.log("enableDeleting");
      this.isDeleting = true;
    },
    cancelDeleting() {
      console.log("cancelDeleting");
      this.isDeleting = false;
      this.selectedUsers = [];
    },
    async confirmDeleting() {
      console.log("confirmDeleting");
      for (const user of this.selectedUsers) {
        console.log("deleting", user);
        await this.deleteUser(user);
      }
      this.updateFilteredUsers();
      this.isDeleting = false;
      this.selectedUsers = [];
      this.$notifyVue("删除成功!");
    },
    enableResettingPassword() {
      console.log("enableResettingPassword");
      this.isResettingPassword = true;
    },
    cancelResettingPassword() {
      console.log("cancelResettingPassword");
      this.isResettingPassword = false;
      this.selectedUsers = [];
    },
    async confirmResettingPassword() {
      console.log("confirmResettingPassword");
      for (const user of this.selectedUsers) {
        console.log("resetting", user);
        await this.resetPassword(user);
      }
      this.isResettingPassword = false;
      this.selectedUsers = [];
      this.$notifyVue("重置成功!");
    },
    increaseAddUser() {
      console.log("newAddUser");
      this.addingUsers.push(cloneDeep(this.defaultNewUser));
    },
    decreaseAddUser() {
      console.log("newAddUser");
      this.addingUsers.pop();
    },
    enableAdding() {
      console.log("enableAdding");
      this.isAdding = true;
    },
    cancelAdding() {
      console.log("cancelAdding");
      this.isAdding = false;
      this.addingUsers = [cloneDeep(this.defaultNewUser)];
    },
    async confirmAdding() {
      console.log("confirmAdding");
      for (const user of this.addingUsers) {
        console.log("adding", user);
        await this.addUser(user);
      }
      this.isAdding = false;
      this.addingUsers = [cloneDeep(this.defaultNewUser)];
      this.updateUsersInfo();
      this.$notifyVue("添加新用户成功!");
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleUsersFile(event) {
      const file = event.target.files[0];
      if (file) {
        const fileExtension = file.name
          .split(".")
          .pop()
          .toLowerCase();
        const reader = new FileReader();

        reader.onload = (e) => {
          const fileContent = e.target.result;

          if (fileExtension === "xlsx") {
            this.parseExcel(fileContent);
          } else {
            this.$notifyVue(
              "文件格式错误，请下载模板文件并按照模板文件格式填写！",
              "danger"
            );
            return;
          }
        };
        reader.readAsArrayBuffer(file);
      }
    },
    parseExcel(fileContent) {
      const workbook = XLSX.read(fileContent, {
        type: "array",
      });
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(worksheet);
      for (const data of jsonData) {
        console.log("data", data);
        let user = cloneDeep(this.defaultNewUser);
        user.name = data["姓名"];
        user.identity = data["身份"];
        user.department_name_id = data["部门"];
        user.email = data["邮箱"];
        user.phone = data["电话"];
        this.addingUsers.push(user);
      }
    },
    downloadTemplateFile() {
      const link = document.createElement("a");
      link.href = "/templateFiles/新建用户模板.xlsx";
      link.download = "新建用户模板.xlsx";
      link.click();
    },
    exportFilteredUsers() {
      const modifiedData = this.filteredUsers.map(
        (item) => {
          return {
            账户: item.id,
            姓名: item.name,
            身份: item.identity,
            部门: item.department_name_id,
            邮箱: item.email,
            电话: item.phone,
          };
        }
      );
      this.$ExportFile(modifiedData, "用户信息.xlsx");
      this.$notifyVue("导出成功!");
    },
    selectAll() {
      this.selectedUsers = this.filteredUsers
        .filter((user) => user.identity !== "管理员")
        .map((user) => user.id);
    },
  },
};
</script>
