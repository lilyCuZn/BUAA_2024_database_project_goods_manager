<template>
  <header class="header-2">
    <div
      class="page-header"
      :class="minHeight"
      :style="`background-image: url(${image})`"
      loading="lazy"
      v-if="title"
    >
      <span :class="mask"></span>
      <div :class="fullWidth ? 'w-100' : 'container'">
        <div class="row">
          <div
            :class="`${$attrs.class ?? 'col-lg-7'} ${
              center ? 'text-center mx-auto' : ''
            }`"
          >
            <component
              :is="title.variant ? title.variant : 'h1'"
              class="text-white"
              :class="title.class"
            >
              {{
                typeof title == "object"
                  ? title.text
                  : title
              }}
            </component>
            <p
              class="lead text-white"
              :class="description.class"
            >
              {{
                typeof description == "object"
                  ? description.text
                  : description
              }}
            </p>
            <slot />
          </div>
        </div>
      </div>
    </div>
    <slot v-else />
  </header>
</template>

<script>
export default {
  props: {
    image: {
      type: String,
      default: "",
    },
    title: {
      type: [String, Object],
      default: "",
      validator(value) {
        // Since title can be an object with text and variant, validator for variant only
        if (typeof value === "object" && value.variant) {
          return [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
          ].includes(value.variant);
        }
        return true;
      },
    },
    description: {
      type: [String, Object],
      default: "",
    },
    mask: {
      type: String,
      default: "mask bg-gradient-success opacity-4",
    },
    center: {
      type: Boolean,
      default: false,
    },
    minHeight: {
      type: String,
      default: " min-vh-75",
    },
    fullWidth: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
