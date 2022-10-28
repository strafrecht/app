<template>
  <div id="app">
    <v-card class="mx-auto">
      <v-container style="max-width: 600px">
        <v-timeline dense clipped>
          <v-timeline-item
            class="mb-4"
            color="blue-grey lighten-1"
            small
            fill-dot
            v-for="item in items"
            :key="item.date"
          >
            <v-row justify="space-between">
              <v-col cols="7"
                ><span class="date">{{ item.date | formatDate }}</span> <br />{{
                  item.message
                }}</v-col
              >
              <v-col class="text-right" cols="5">
                <span v-if="item.points">
                  {{ item.points }}
                  <img
                    src="http://strafrecht-online.org/stuff/coin.svg"
                    style="height: 22px; vertical-align: top"
                  />
                </span>
              </v-col>
            </v-row>
          </v-timeline-item>
        </v-timeline>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import moment from "../../../node_modules/moment/moment.js";
import localization from "../../../node_modules/moment/locale/de";
moment.updateLocale("de", localization);

export default {
  name: "timeline",
  props: {
    date: String,
  },
  data() {
    return {
      items: [
        {
          message: "Wiki Article unlocked by staff.",
          date: "2021-02-17T11:40:46.928Z",
          points: "100",
        },
        {
          message:
            "Wiki Article 'Erlaubnistatumstandsirrtum' in category 'Rechtswidrigkeit' created.",
          date: "2021-02-17T10:34:46.928Z",
          points: "50",
        },
        {
          message: "Uploaded new profile picture.",
          date: "2021-02-17T08:40:46.928Z",
        },
        {
          message: "MCT-Questions in category 'Schuld' answered.",
          date: "2021-02-15T08:40:46.928Z",
          points: "30",
        },
      ],
    };
  },
  filters: {
    formatDate: function (value) {
      if (value) {
        return moment(String(value)).format("DD.MM.YYYY hh:mm ") + "Uhr";
      }
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap");

.date {
  font-size: 0.8em;
  color: grey;
}
</style>