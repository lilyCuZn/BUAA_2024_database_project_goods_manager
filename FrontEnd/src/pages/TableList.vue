<template>
  <div class="content">
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      >
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">Simple Table</h4>
            <p class="category">
              Here is a subtitle for this table
            </p>
          </md-card-header>
          <md-card-content>
            <simple-table
              :users="users"
              :headers="headers"
              :table-header-color="green"
            ></simple-table>
          </md-card-content>
        </md-card>
      </div>

      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      >
        <md-card class="md-card-plain">
          <md-card-header data-background-color="green">
            <h4 class="title">Table on Plain Background</h4>
            <p class="category">
              Here is a subtitle for this table
            </p>
          </md-card-header>
          <md-card-content>
            <ordered-table></ordered-table>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import { SimpleTable, OrderedTable } from "@/components";

export default {
  components: {
    OrderedTable,
    SimpleTable,
  },
  data() {
    return {
      users: [
        {
          name: "Dakota Rice",
          salary: "$36,738",
          country: "Niger",
          city: "Oud-Turnhout",
        },
        {
          name: "Minerva Hooper",
          salary: "$23,738",
          country: "Curaçao",
          city: "Sinaai-Waas",
        },
        {
          name: "Sage Rodriguez",
          salary: "$56,142",
          country: "Netherlands",
          city: "Overland Park",
        },
        {
          name: "Philip Chaney",
          salary: "$38,735",
          country: "Korea, South",
          city: "Gloucester",
        },
        {
          name: "Doris Greene",
          salary: "$63,542",
          country: "Malawi",
          city: "Feldkirchen in Kārnten",
        },
        {
          name: "Mason Porter",
          salary: "$78,615",
          country: "Chile",
          city: "Gloucester",
        },
      ],
      headers: ["Name", "Country", "City", "Salary"],
    };
  },
};
</script>
