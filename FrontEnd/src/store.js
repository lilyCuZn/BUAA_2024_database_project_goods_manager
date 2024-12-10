// store.js
import Vue from "vue";
import Vuex from "vuex";
import VuexPersistence from "vuex-persistedstate";
Vue.use(Vuex);

export default new Vuex.Store({
  state: { user: null },
  mutations: {
    setUser(state, obj) {
      console.log("setUser:");
      console.log("obj", obj);
      state.user = obj;
      console.log("state", state);
    },
    clearUser(state) {
      console.log("clearUser:");
      state.user = null;
    },
  },
  actions: {
    login({ commit }, obj) {
      console.log("login:");
      commit("setUser", obj);
    },
    logout({ commit }) {
      console.log("logout:");
      commit("clearUser");
    },
  },
  plugins: [
    new VuexPersistence({
      storage: window.localStorage,
    }),
  ],
});
