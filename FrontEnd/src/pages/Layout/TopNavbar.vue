<template>
  <md-toolbar md-elevation="0" class="md-transparent">
    <div class="md-toolbar-row">
      <div class="md-toolbar-section-start">
        <h3 class="md-title">{{ $route.name }}</h3>
      </div>
      <div class="md-toolbar-section-end">
        <md-button
          class="md-just-icon md-simple md-toolbar-toggle"
          :class="{ toggled: $sidebar.showSidebar }"
          @click="toggleSidebar"
        >
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </md-button>

        <div class="md-collapse">
          <md-button
            class="md-just-icon md-simple"
            @click="goto('/dashboard')"
          >
            <md-icon
              >home
              <md-tooltip>工作面板</md-tooltip>
            </md-icon>
          </md-button>
          <md-button
            class="md-just-icon md-simple"
            @click="goto('/user')"
          >
            <md-icon
              >account_circle
              <md-tooltip>用户中心</md-tooltip>
            </md-icon>
          </md-button>
        </div>
      </div>
    </div>
  </md-toolbar>
</template>

<script>
export default {
  data() {
    return {
      selectedEmployee: null,
      employees: [
        "Jim Halpert",
        "Dwight Schrute",
        "Michael Scott",
        "Pam Beesly",
        "Angela Martin",
        "Kelly Kapoor",
        "Ryan Howard",
        "Kevin Malone",
      ],
    };
  },
  methods: {
    toggleSidebar() {
      this.$sidebar.displaySidebar(
        !this.$sidebar.showSidebar
      );
    },
    goto(page) {
      if (this.$route.path !== page) {
        this.$router.push(page);
      }
    },
  },
};
</script>

<style lang="css"></style>
