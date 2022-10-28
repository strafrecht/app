import "../styles/index.scss"
// FIXME: check sizes and styles of fonts
// @import url("https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap");
// <link href="https://fonts.googleapis.com/css?family=Source+Serif+Pro:400,500|Roboto:400,500,600,700&display=swap" rel="stylesheet">
// <link href="https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&display=swap" rel="stylesheet">
// <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap" rel="stylesheet">

import "@fontsource/crimson-text";
import "@fontsource/roboto";
import "@fontsource/roboto-slab";
import "@fontsource/source-serif-pro";

import Vue from "vue";
import vSelect from "vue-select";
import VTreeselect from 'vue-treeselect'
import axios from "axios";
import Swiper from 'swiper';

import $ from "jquery";
import "slick-carousel";
import "bootstrap/dist/js/bootstrap.bundle";
// import moment from "moment";
import "chartist/dist/chartist.js";

import { initEditor } from  './editor/index.js';
initEditor();

import deck from "./vue/flashcards/Deck.vue";
new Vue({
  render: (h) => h(deck),
}).$mount("deck");

$(document).ready(function () {
  // window.console.log("dom ready");
});

window.jQuery = window.$ = $;
