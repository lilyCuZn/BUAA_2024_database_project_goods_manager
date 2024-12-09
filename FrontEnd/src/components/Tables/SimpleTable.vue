<template>
  <div>
    <md-table
      v-model="users"
      :table-header-color="tableHeaderColor"
    >
      <md-table-row
        slot="md-table-row"
        slot-scope="{ item }"
      >
        <md-table-cell
          v-for="(header, index) in headers"
          :key="index"
          :md-label="header"
        >
          <md-field>
            <md-input
              v-model="item[header.toLowerCase()]"
              type="text"
            ></md-input>
          </md-field>
        </md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
export default {
  name: "simple-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: "",
    },
    users: {
      type: Array,
      default: () => [],
    },
    headers: {
      type: Array,
      default: () => [],
    },
  },
};
</script>
