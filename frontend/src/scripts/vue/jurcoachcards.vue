<template>
  <v-container>
    <v-row>
      <v-col>
        <v-dialog v-model="falltraining" width="500">
          <template v-slot:activator="{ on, attrs }">
            <v-card class="mx-auto jurcoach-card" v-bind="attrs" v-on="on">
              <v-card-text class="title text-center pb-0">
                Falltraining
              </v-card-text>
              <v-card-text
                class="display-2 pt-0 font-weight-bold text-center grey--text text--darken-3"
              >
                <img
                  src="http://strafrecht-online.org/stuff/falltraining.svg"
                  class="jurcoach-image"
                />
              </v-card-text>
            </v-card>
          </template>

          <v-card>
            <v-card-title class="headline lighten-2">
              Falltraining
            </v-card-title>

            <v-card-text>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
              enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
              reprehenderit in voluptate velit esse cillum dolore eu fugiat
              nulla pariatur. Excepteur sint occaecat cupidatat non proident,
              sunt in culpa qui officia deserunt mollit anim id est laborum.
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-col>
      <v-col>
        <v-card class="mx-auto jurcoach-card">
          <v-card-text class="title text-center pb-0"> Wiki </v-card-text>
          <v-card-text
            class="display-2 pt-0 font-weight-bold text-center grey--text text--darken-3"
          >
            <img
              src="http://strafrecht-online.org/stuff/wiki.png"
              class="jurcoach-image"
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-card class="mx-auto jurcoach-card">
          <v-card-text class="title text-center pb-0"> MCT </v-card-text>
          <v-card-text
            class="display-2 pt-0 font-weight-bold text-center grey--text text--darken-3"
          >
            <img
              src="http://strafrecht-online.org/stuff/mct.svg"
              class="jurcoach-image"
            />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-card class="mx-auto jurcoach-card">
          <v-card-text class="title text-center pb-0">
            User Profile
          </v-card-text>
          <v-card-text
            class="display-2 pt-0 font-weight-bold text-center grey--text text--darken-3"
          >
            <img
              src="http://strafrecht-online.org/stuff/account.svg"
              class="jurcoach-image"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "jurcoachcards",
  data() {
    return {
      falltraining: false,
      mct: false,
      userprofile: false,
      wiki: false,
    };
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap");
@import url("https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css");
.jurcoach-card {
  width: 100%;
  min-height: 200px;
}
.jurcoach-image {
  max-width: 150px;
}
.full-height {
  height: 100%;
}
</style>