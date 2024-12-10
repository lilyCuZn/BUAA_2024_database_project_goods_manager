<template>
  <div class="form-check form-switch">
    <input
      :id="id"
      class="form-check-input"
      type="checkbox"
      :name="id"
      :checked="checked"
      @change="$emit('input', $event.target.checked)"
    />
    <label
      class="form-check-label d-block"
      :class="labelClass"
      :for="id"
    >
      <slot />
    </label>
    <slot name="description" v-if="$slots.description" />
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: String,
      required: true,
    },
    checked: {
      type: Boolean,
      default: false, // 保持为布尔值
    },
    labelClass: {
      type: String,
      default: "",
    },
  },
};
</script>
