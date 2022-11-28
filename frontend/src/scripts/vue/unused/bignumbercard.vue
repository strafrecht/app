<template>
  <div id="app">
    <v-card class="mx-auto" width="100%">
      <v-card-text class="subtitle-1 text-center pb-0">
        {{ description }}
      </v-card-text>
      <v-card-text
        class="display-2 pt-0 font-weight-bold text-center grey--text text--darken-3"
      >
        {{ number }}
      </v-card-text>
    </v-card>
  </div>
</template>
<script>
export default {
  name: "bignumbercard",
  props: {
    description: String,
    number: String,
  },
  data() {},
  methods: {},
};
</script>