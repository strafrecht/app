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
// import Vue from "vue";
// import full Vue build
import LVue from 'vue/dist/vue.js';
global.LVue = LVue;

import '@riophae/vue-treeselect/dist/vue-treeselect.css';
import VTreeselect from '@riophae/vue-treeselect';
global.VTreeselect = VTreeselect;

import axios from "axios";
global.axios = axios;

import Swiper from 'swiper';

global.$ = require('jquery');
global.jQuery = $;

//import "slick-carousel";
import "bootstrap/dist/js/bootstrap.bundle";
import "popper.js";
// import moment from "moment";
import * as Chartist from 'chartist';
global.Chartist = Chartist;
require("chartist-plugin-fill-donut");

require("./urlify.js");

import { initEditor } from  './editor/index.js';
initEditor();

import DeckApp from "./vue/flashcards/Deck.vue";
global.DeckApp = DeckApp;

import CaseApp from "./vue/casetraining/Case.vue";
global.CaseApp = CaseApp;

import { initBookmarks } from  './bookmarks.js';

// menu resize
//
$(document).ready(function () {
  $(document).ready(sizing);
  $(window).resize(sizing);
  initBookmarks();
  fixCustomBootstrapForms();
});

function fixCustomBootstrapForms() {
  var elements = document.getElementsByClassName("custom-file-input");
  for (var i = 0; i < elements.length; i++) {
    var element = elements[i];
    element.onchange = function (e) {
      var filenames = "";
      for (let i=0;i<e.target.files.length;i++) {
	filenames+=(i>0?", ":"")+e.target.files[i].name;
      }
      e.target.parentNode.querySelector('.custom-file-label').textContent=filenames;
    };
  };
}

function sizing() {
  var win = $(this).width();
  console.log(win);
  if (win > 973) {
    $('.navbar-nav > .nav-item .dropdown-menu').hide();
    $('.navbar-nav > .nav-item').hover(function() {
      $(this).find('.dropdown-menu').first().stop(true, true).delay(230).show(0);
    }, function() {
      $(this).find('.dropdown-menu').first().stop(true, true).delay(500).hide(0);
    });
    $('.navbar-nav:nth-child(1) > .nav-item > a').click(function() {
      location.href = this.href;
    });
  } else {
    $('.navbar-nav > .nav-item').off('hover');
    $('.navbar-nav > .nav-item .dropdown-menu').show();
    $('.navbar-nav:nth-child(1) > .nav-item > a').click(function() {
      location.href = this.href;
    });
  }
};

// show quizz chart
//
function quizz_chart(dom_id, score, total) {
  var chart = Chartist.Pie(dom_id, {
    series: [score, total-score],
    labels: ['', '']
  }, {
    donut: true,
    donutWidth: 15,
    startAngle: 210,
    total: total,
    showLabel: false,
    plugins: [
      Chartist.plugins.fillDonut({
	items: [{ //Item 1
	  content: '<i class="fa fa-tachometer text-muted"></i>',
	  position: 'bottom',
	  offsetY : 10,
	  offsetX: -2
	}, { //Item 2
	  content: `<h3 class='donut-inner-text'>${score}/${total}<span class="small"></span></h3>`
	}]
      })
    ],
  });
  //Animation for the first series
  chart.on('draw', function(data) {
    if(data.type === 'slice' && data.index == 0) {
      var pathLength = data.element._node.getTotalLength();

      data.element.attr({
	'stroke-dasharray': pathLength + 'px ' + pathLength + 'px'
      });

      var animationDefinition = {
	'stroke-dashoffset': {
	  id: 'anim' + data.index,
	  dur: 1200,
	  from: -pathLength + 'px',
	  to:  '0px',
	  easing: Chartist.Svg.Easing.easeOutQuint,
	  fill: 'freeze'
	}
      };
      data.element.attr({
	'stroke-dashoffset': -pathLength + 'px'
      });
      data.element.animate(animationDefinition, true);
    }
  });
};
global.quizz_chart = quizz_chart;

// polls
//
function init_poll(post_url) {
  $("#poll > label").empty();
  $("#poll").submit(function(e) {
    e.preventDefault()

    $.ajax({
      type:'POST',
      url: post_url,
      data:{
	question: parseInt($('input[name="question"]:checked').val()),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
      },
      success: function(json){
        const total = json.total_votes

	$("#poll").empty();
	let elements = Object.entries(json.votes).map((vote) => {
	  let question = vote[0]
	  let votes = vote[1]
	  let ratio = Math.round((votes / total) * 100)

	  return `
		<div class="answer">
			<div class="bar">
				<div style="width: ${ratio}%;"></div><span>${votes} (${ratio}%)</span>
			</div>
			<div>${question}</div>
		</div>
		`
	})

	$("#poll").append(`
			<div class="answers">
				${elements.join('')}
			</div>
			`)
      },
      error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  });
};
global.init_poll = init_poll;
