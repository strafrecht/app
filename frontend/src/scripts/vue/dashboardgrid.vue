<template>
  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-container class="py-0 fill-height">
        <v-avatar class="mr-10" color="grey darken-1" size="40">
          <img
            src="http://strafrecht-online.org/personen/roland.hefendehl/IMG_8066.jpg"
            alt="Roland Hefendehl"
        /></v-avatar>
        <v-btn v-for="link in links" :key="link" text>
          {{ link }}
        </v-btn>
        <v-spacer></v-spacer>
      </v-container>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col>
            <bignumbercard description="MCT Questions" number="293" />
          </v-col>
          <v-col>
            <bignumbercard description="Wiki Articles" number="125" />
          </v-col>
          <v-col>
            <bignumbercard description="Cases" number="0" />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <timeline />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <trendline />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <leaderboard />
          </v-col>
        </v-row>
      </v-container>
      <jurcoachcards />
    </v-main>
  </v-app>
</template>

<script>
import leaderboard from "./leaderboard";
import bignumbercard from "./bignumbercard";
import userprofilecard from "./userprofilecard";
import jurcoachcards from "./jurcoachcards";
import timeline from "./timeline";
import trendline from "./trendline";

export default {
  data: () => ({
    links: ["Dashboard", "Rewards", "Settings"],
  }),
  components: {
    leaderboard,
    bignumbercard,
    userprofilecard,
    jurcoachcards,
    timeline,
    trendline,
  },
};
</script>