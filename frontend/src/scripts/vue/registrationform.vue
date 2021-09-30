<template>
  <v-app id="inspire">
    <v-card width="600" class="mx-auto mt-5">
      <v-card-title class="pb-0">Registrierung</v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-text-field
            v-model="email"
            :rules="emailRules"
            prepend-icon="mdi-email"
            label="E-Mail-Adresse"
            required
          ></v-text-field>

          <v-text-field
            v-model="name"
            :counter="20"
            :rules="nameRules"
            prepend-icon="mdi-account-circle"
            label="Nutzername"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            :rules="passwordRules"
            :type="showPassword ? 'text' : 'password'"
            label="Passwort"
            prepend-icon="lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
            required
          />

          <v-checkbox
            v-model="checkbox"
            :rules="[
              (v) => !!v || 'Du musst zustimmen, um dich zu registrieren.',
            ]"
            label="Ich stimme den Nutzungsbedingungen und der Datenschutzerklärung zu."
            required
          ></v-checkbox>
          <!--
          <v-btn
            :disabled="!valid"
            color="success"
            class="mr-4"
            @click="validate"
          >
            Validate
          </v-btn>

          <v-btn color="error" class="mr-4" @click="reset"> Reset Form </v-btn>

          <v-btn color="warning" @click="resetValidation">
            Reset Validation
          </v-btn>
        -->
        </v-form>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-col class="text-right">
          <v-btn color="success">Registrieren</v-btn>
        </v-col>
      </v-card-actions>
    </v-card>
  </v-app>
</template>

<script>
export default {
  name: "registrationform",

  data: () => ({
    showPassword: false,
    valid: true,
    name: "",
    nameRules: [
      (v) => !!v || "Bitte gib einen Nutzernamen ein.",
      (v) =>
        (v && v.length <= 20) ||
        "Der Nutzername darf maximal 20 Zeichen lang sein.",
    ],
    password: "",
    passwordRules: [
      (v) => !!v || "Bitte gib ein Passwort ein.",
      (v) =>
        (v && v.length >= 6) || "Das Passwort muss länger als 6 Zeichen sein.",
      (v) =>
        (v && v.length <= 40) ||
        "Das Passwort muss kürzer als 40 Zeichen sein.",
    ],
    email: "",
    emailRules: [
      (v) => !!v || "Bitte gib eine E-Mail-Adresse ein.",
      (v) =>
        /.+@.+\..+/.test(v) || "Bitte gib eine gültige E-Mail-Adresse ein.",
    ],
  }),

  methods: {
    validate() {
      this.$refs.form.validate();
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap");
@import url("https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css");
</style>