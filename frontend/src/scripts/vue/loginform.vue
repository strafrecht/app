<template>
  <v-app>
    <v-card width="400" class="mx-auto mt-5">
      <v-card-title class="pb-0">Login</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field label="Nutzername" prepend-icon="mdi-account-circle" />
          <v-text-field
            :type="showPassword ? 'text' : 'password'"
            label="Passwort"
            prepend-icon="lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
          />
        </v-form>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-col>
          <v-btn color="success">Registrieren</v-btn>
        </v-col>
        <v-col class="text-right">
          <v-btn color="info">Login</v-btn>
        </v-col>
      </v-card-actions>
    </v-card>
  </v-app>
</template>


<script>
export default {
  name: "loginform",
  data() {
    return {
      showPassword: false,
    };
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap");
@import url("https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css");
</style>