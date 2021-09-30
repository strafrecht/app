<template>
  <div id="app">
    <v-card class="mx-auto text-center" width="100%">
      <v-card-text class="title text-center font-weight-bold">
        Points per week
      </v-card-text>
      <v-card-text>
        <v-sheet>
          <v-sparkline
            :labels="labels"
            color="grey"
            :value="value"
            :gradient="gradient"
            :smooth="radius || false"
            :padding="padding"
            :line-width="width"
            :stroke-linecap="lineCap"
            :gradient-direction="gradientDirection"
            :fill="fill"
            :type="type"
            :auto-line-width="autoLineWidth"
            auto-draw
          ></v-sparkline>
        </v-sheet> </v-card-text
      ><!--
      <v-card-text class="subtitle-3 text-center font-weight-bold">
        7 days trend
      </v-card-text>-->
    </v-card>
  </div>
</template>

<script>
import moment from "../../../node_modules/moment/moment.js";
import localization from "../../../node_modules/moment/locale/de";
moment.updateLocale("de", localization);

const gradients = [
  ["#222"],
  ["#42b3f4"],
  ["red", "orange", "yellow"],
  ["purple", "violet"],
  ["#00c6ff", "#F0F", "#FF0"],
  ["#f72047", "#ffd200", "#1feaea"],
];

export default {
  name: "trendline",
  data() {
    return {
      width: 2,
      radius: 10,
      padding: 8,
      lineCap: "round",
      gradient: gradients[5],
      gradientDirection: "top",
      gradients,
      fill: false,
      type: "trend",
      autoLineWidth: false,
      labels: [
        "6. KW",
        "7. KW",
        "8. KW",
        "9. KW",
        "10. KW",
        "11. KW",
        "12. KW",
      ],
      value: [200, 675, 410, 390, 310, 460, 250],
    };
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap");
</style>