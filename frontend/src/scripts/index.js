import "../styles/index.scss"
import $ from "jquery/dist/jquery.slim"
import "bootstrap/dist/js/bootstrap.bundle"
import Editor from '@toast-ui/editor'
//import '@toast-ui/editor/dist/toastui-editor.css'
//import '@toast-ui/editor/dist/toastui-editor-viewer.css'
import moment from "moment";

/* Editor */
const editor = new Editor({
  el: document.querySelector('.editor'),
  height: '500px',
  initialEditType: 'markdown',
  previewStyle: 'vertical'
});

editor.getMarkdown()

import Vue from "vue";
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
