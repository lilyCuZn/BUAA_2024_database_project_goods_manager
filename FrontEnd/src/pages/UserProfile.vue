<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-medium-size">
        <edit-profile-form data-background-color="green"> </edit-profile-form>
      </div>

    </div>
  </div>
</template>

<script>
import { EditProfileForm, UserCard } from "@/pages";

export default {
  components: {
    EditProfileForm,
  },
};
</script>
