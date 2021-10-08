import "../styles/index.scss"
import Vue from "vue"
import $ from "jquery/dist/jquery.slim"
import "bootstrap/dist/js/bootstrap.bundle"
import { initEditor } from  './editor/index'
import moment from "moment"

initEditor()

// import Vuetify from "vuetify";
//import calendar from "./vue/calendar.vue";

// Vue.config.productionTip = true;

/*
new Vue({
  render: (h) => h(calendar),
}).$mount("calendar");
*/


$(document).ready(function () {
  window.console.log("dom ready");
});
