import "../styles/index.scss"
import Vue from "vue"
import $ from "jquery/dist/jquery.slim"
import "bootstrap/dist/js/bootstrap.bundle"
import { initEditor } from  './editor/index'
// import moment from "moment";
import deck from "./vue/flashcards/deck.vue";

initEditor()

// import Vuetify from "vuetify";
//import calendar from "./vue/calendar.vue";

// Vue.config.productionTip = true;

/*
new Vue({
  render: (h) => h(calendar),
}).$mount("calendar");
*/

new Vue({
  render: (h) => h(deck),
}).$mount("deck");

$(document).ready(function () {
  // window.console.log("dom ready");
});
