<template>
  <div id="app">
    <v-app id="inspire">
      <v-card class="mx-auto" max-width="344">
        <v-list-item three-line>
          <v-list-item-content>
            <div class="overline mb-4">PROFILE</div>
            <v-list-item-title class="headline mb-1">
              Roland Hefendehl
            </v-list-item-title>
            <v-list-item-subtitle>Criminal Law Master</v-list-item-subtitle>
          </v-list-item-content>
          <!--<v-avatar-uploader
            size="80"
            color="primary"
            :url="url"
            :request="request"
          />-->
          <v-avatar size="80" color="primary">
            <img
              src="http://strafrecht-online.org/personen/roland.hefendehl/IMG_8066.jpg"
              alt="Roland Hefendehl"
          /></v-avatar>
        </v-list-item>
        <v-card-actions>
          <v-btn outlined rounded text> Edit </v-btn>
        </v-card-actions>
      </v-card>
    </v-app>
  </div>
</template>
<script>
import VAvatarUploader from "../../../node_modules/vuetify-avatar-uploader/dist/vuetify-avatar-uploader.js";

export default {
  name: "userprofilecard",
  components: {
    VAvatarUploader,
  },
  computed: {
    // Determine the URL to show, typically from an object representing a user
    url() {
      return "http://strafrecht-online.org/personen/jakob.bach/IMG_8058.jpg";
    },
  },
  methods: {
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
    request(form, config) {
      return this.$http.post("/api/avatars", form, config);
    },
  },
};
</script>