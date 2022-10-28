<template>
  <div id="app">
    <v-data-table
      :headers="headers"
      :items="data"
      class="elevation-1"
      hide-default-footer
      :items-per-page="10"
      :loading="loadTable"
      loading-text="Loading Leaderboard... Please wait"
    >
      <template v-slot:item.avatar="{ item, index }">
        <v-badge avatar bordered overlap v-if="index < 3">
          <template v-slot:badge v-if="index < 3">
            <v-avatar>
              <v-img
                v-if="index == 0"
                src="http://strafrecht-online.org/stuff/trophy-gold.png"
              ></v-img>
              <v-img
                v-if="index == 1"
                src="http://strafrecht-online.org/stuff/trophy-silver.png"
              ></v-img>
              <v-img
                v-if="index == 2"
                src="http://strafrecht-online.org/stuff/trophy-bronze.png"
              ></v-img>
            </v-avatar>
          </template>
          <v-avatar :color="getRandomColor()" size="40"
            ><img v-if="item.avatar_url" :src="item.avatar_url" />
            <span v-else>{{ initials(item.name) }}</span>
          </v-avatar>
        </v-badge>
        <v-avatar v-else :color="getRandomColor()" size="40"
          ><img v-if="item.avatar_url" :src="item.avatar_url" />
          <span v-else>{{ initials(item.name) }}</span>
        </v-avatar>
      </template>
      <template v-slot:item.points30="{ item }">
        <v-chip :color="getColor(item.points30)">
          {{ item.points30 }}
        </v-chip>
      </template>
      <template v-slot:item.pointsalltime="{ item }">
        <v-chip :color="getColor(item.pointsalltime)">
          {{ item.pointsalltime }}
        </v-chip>
      </template>
      <template v-slot:item.trend="{ item }">
        <v-sparkline
          :value="item.trend_values"
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
      </template>
      <template v-slot:item.info="{ item, index }">
        <v-btn
          icon
          color="primary"
          small
          @click.stop="$set(dialogNote, item.name, true)"
        >
          <v-icon small>mdi-open-in-new</v-icon>
        </v-btn>
        <v-dialog
          v-model="dialogNote[item.name]"
          scrollable
          lazy
          max-width="500"
          :key="item.name"
        >
          <v-card>
            <v-card-title>
              <span>Statistik für {{ item.name }}</span>
              <v-spacer></v-spacer>
              <v-avatar :color="getRandomColor()" size="80"
                ><img v-if="item.avatar_url" :src="item.avatar_url" />
                <span v-else>{{ initials(item.name) }}</span>
              </v-avatar>
            </v-card-title>
            <v-card-text>
              Punkte in den letzten 30 Tagen: {{ item.points30 }}<br />
              Punkte insgesamt: {{ item.pointsalltime }}<br />
              Wiki Revisions: {{ item.points30 }}<br />
              MCT-Questions: {{ item.points30 }}<br />
              Cases solves: {{ item.points30 }}
            </v-card-text>
            <v-card-actions>
              <v-btn
                color="primary"
                flat
                @click.stop="$set(dialogNote, item.name, false)"
                >Close</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
    </v-data-table>
  </div>
</template>
<script>
const gradients = [
  ["#222"],
  ["#42b3f4"],
  ["red", "orange", "yellow"],
  ["purple", "violet"],
  ["#00c6ff", "#F0F", "#FF0"],
  ["#f72047", "#ffd200", "#1feaea"],
];

export default {
  name: "leaderboard",
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
      dialogNote: {},
      loadTable: false,
      headers: [
        {
          text: "",
          sortable: false,
          value: "avatar",
        },
        {
          text: "Name",
          align: "start",
          sortable: false,
          value: "name",
        },
        { text: "Points last 30 days", value: "points30" },
        { text: "Points Alltime", value: "pointsalltime" },
        { text: "30-days-Trend", value: "trend", sortable: false },
        { text: "", value: "info", sortable: false },
      ],
      data: [
        {
          name: "Roland Hefendehl",
          points30: 159,
          pointsalltime: 1000,
          avatar_url:
            "http://strafrecht-online.org/personen/roland.hefendehl/IMG_8066.jpg",
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Lucas Robinson",
          points30: 237,
          pointsalltime: 500,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Isabelle Hall",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Natalia Gonzales",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Nelson Rogers",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Mira Rosales",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Jack Spencer",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Benjamin Marsh",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Zac Moss",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Ellen Dodson",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Sabrina Thomas",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Danny Cunningham",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Tanner Lott",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
        {
          name: "Jude Pearson",
          points30: 262,
          pointsalltime: 300,
          trend_values: this.getRandomArray(15, 30),
        },
      ],
    };
  },
  methods: {
    getColor(points) {
      if (points > 500) return "green";
      else if (points > 300) return "orange";
      else return "transparent";
    },
    initials(fullName) {
      let arrName = fullName.split(" ");
      let iniName = fullName.charAt(0);
      let iniLname = arrName[arrName.length - 1].charAt(0);
      return iniName + iniLname;
    },
    getRandomColor() {
      let colors = ["#34686f", "#dfa288", "#fff5bc", "#9cccae", "#fbffd7"];
      let rand = Math.floor(Math.random() * colors.length);
      return colors[rand];
    },
    getRandomArray(length, max) {
      return Array.apply(null, Array(length)).map(function () {
        return Math.round(Math.random() * max);
      });
    },
  },
};
</script>
<style scoped>
@import url("https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css");
</style>