<template>
<step-template type="problems" :key="componentKey">
  <template #left>
    <!-- wiki browser modal -->
    <modal v-if="showModal" @close="showModal = false">
      <template #header>Problemfeldwiki</template>
      <template #body>
	<div v-html="modalBody"></div>
      </template>
      <template #footer>
	<button class="btn btn-secondary" @click="showModal = false">
          Schließen
	</button>
	<button v-if="myStep != 2" class="btn btn-success" @click="addSelectedWikiUrl">
          Hinzufügen
	</button>
      </template>
    </modal>

    <div>
      <div style="position: relative">
	<div style="position: absolute; top: 0; left: 0; color: transparent; pointer-events: none;">
	  <div id="user-mark-area-content" v-html="currentCase.userFacts"></div>
	</div>
	<div id="mark-area-content" v-html="currentCase.facts"></div>
      </div>
    </div>
  </template>
  <template #right>
    <div v-if="editMode">
      <div class="mb-3">
	<label>Einleitungstext</label>
	<div class="small text-danger" v-if="$parent.showDiff && $parent.diffIntroToParent()">
	  <strong>Vorherige Version</strong>
	  <div>{{ $parent.diffIntroToParent() }}</div>
	</div>
	<textarea class="form-control" v-model="currentStep.intro" />
      </div>
      <div v-if="editMode">
	<p>Weisen Sie Problemfelder den einzelnen Sachverhaltsabschnitten zu.</p>
      </div>
    </div>
    <div v-else>
      <p>{{ currentStep.intro }}</p>
    </div>

    <div class="mb-3" v-for="(marker, cindex) in sectionMarkers">
      <h5 class="section" :class="marker">Abschnitt {{ cindex + 1 }}</h5>

      <div v-if="$parent.showDiff && $parent.diffConfigToParentDeleted(cindex)" class="text-danger mb-3">
	<strong>{{ $parent.diffConfigToParentDeleted(cindex) }} Problemfeld(er) gelöscht!</strong>
      </div>

      <div v-if="myStep == 1">

	<div v-for="(article, index) in stepTarget[cindex]" class="border-bottom my-1 px-2 py-1">
	  <div class="mb-2">
	    <small>
	      <i @click="delArticle(cindex, index)" class="ml-2 float-right fa fa-trash text-danger" role="button" title="Artikel löschen"></i>
	      <span class="ml-2 float-right text-link" @click.stop="openWikiBrowser(cindex, article.url)">zum Wiki</span>
	      <i class="text-muted">{{ urlToText(article.url) }}</i>
	    </small>
	    <div>{{ article.title }}</div>
	    <div v-if="$parent.showDiff && $parent.diffConfigToParent(cindex, index, 'title')" class="small text-danger">
	      <strong>Vorherige Version:</strong>
	      <div style="white-space: pre-wrap">{{ $parent.diffConfigToParent(cindex, index, 'title') }}</div>
	    </div>
	  </div>
	</div>
	<div class="search-form form-group mt-2">
	  <input v-if="problemIndex == cindex" class="form-control" v-model="wikiSearch" placeholder="Problemfeldwiki durchsuchen">
	  <input v-else class="form-control" @focus="setProblemIndex(cindex)" placeholder="Problemfeldwiki durchsuchen">
	  <span class="small float-right text-link" @click="openWikiBrowser(cindex)">Systematische Suche</span>
	  <div v-if="wikiSearch.length > 0 && problemIndex == cindex" class="search-results shadow">
	    <div v-if="!wikiReady" class="mb-2">
	      <i class="fa fa-sync fa-spin text-info mr-2"></i>
	      Einen Augenblick bitte – Lade Daten …
	    </div>
	    <div class="mb-2" v-for="(article, index) in wikiSearchArticles(cindex)" @click="addArticle(cindex, article)">
	      <small>
		<span class="float-right text-link" @click.stop="openWikiBrowser(cindex, article.url)">zum Wiki</span>
		<i class="text-muted">{{ urlToText(article.url) }}</i>
	      </small>
	      <div>{{ article.title }}</div>
	    </div>
	  </div>
	</div>

      </div>
      <div v-else>

	<div v-for="(article, index) in currentStep.answers[cindex]" class="border-bottom my-1 px-2 py-1">
	  <div class="mb-2" :class="correctAnswerClass(cindex, article)">
	    <small>
	      <span class="ml-2 small float-right text-link" @click="openWikiBrowser(cindex, article.url)">zum Wiki</span>
	      <i class="text-muted">{{ urlToText(article.url) }}</i>
	    </small>
	    <div>{{ article.title }}</div>
	  </div>
	</div>

	<div v-for="(article, index) in otherArticles(cindex)" class="border-bottom my-1 px-2 py-1">
	  <div class="mb-2 text-muted">
	    <small>
	      <span class="ml-2 small float-right text-link" href="" @click.stop="openWikiBrowser(cindex, article.url)">zum Wiki</span>
	      <i class="text-black-50">{{ urlToText(article.url) }}</i>
	    </small>
	    <div>{{ article.title }}</div>
	  </div>
	</div>

      </div>
    </div>
  </template>
  <template #buttons-right v-if="!editMode">
    <button v-if="myStep == 1" class="btn btn-primary" @click="nextStep()">zur Auswertung</button>
    <button v-if="myStep == 2" class="btn btn-primary" @click="nextStep()">nächster Schritt</button>
  </template>
</step-template>
</template>

<script>
import axios from "axios";
import { nextTick } from "vue";

import Modal from "./Modal.vue";
import StepTemplate from "./StepTemplate.vue";

export default {
  name: "StepProblems",
  components: {
    Modal,
    StepTemplate,
  },
  props: {
    currentCase: {
      type: Object,
    },
    currentStep: {
      type: Object,
    },
    currentStepNo: {
      type: Number,
    },
  },
  data() {
    return {
      myStep: 1,
      componentKey: 0,
      wikiSearch: "",
      problemIndex: null,
      showModal: false,
      selectedWikiUrl: null,
      modalBody: "Lade Problemfeldwiki…",
    }
  },
  computed: {
    wikiReady() {
      return this.$parent.wikiReady;
    },
    wikiArticles() {
      return this.$parent.wikiArticles;
    },
    editMode() {
      return this.$parent.editMode;
    },
    sectionMarkers() {
      var parts = this.currentCase.facts.split(/class=\"/);
      var classes = [];
      for (var i = 0; i < parts.length-1; i++) {
	classes[i] = parts[i+1].split(/\"/)[0].trim();
      }
      // return unique classes
      return classes.filter((v, i, a) => a.indexOf(v) === i);
    },
    stepTarget() {
      return this.editMode ? this.currentStep.config : this.currentStep.answers;
    },
  },
  beforeMount() {
    if (typeof this.currentStep.answers === "undefined")
      this.currentStep.answers = [];

    if (!this.currentStep.config)
      this.currentStep.config = [];

    if (!this.currentStep.intro)
      this.currentStep.intro = "Ermitteln Sie die Problemfelder der Sachverhaltsabschnitte.";
  },
  methods: {
    setProblemIndex(index) {
      if (this.problemIndex != index)
	this.wikiSearch = "";
      this.problemIndex = index;
    },
    prevStep() {
      this.$parent.prevStep();
    },
    nextStep() {
      if (this.myStep == 2) {
	this.myStep = 1;
	return this.$parent.nextStep();
      }

      this.myStep += 1;
    },
    otherArticles(index) {
      if (!this.currentStep.config[index])
	return false;

      if (!this.currentStep.answers[index])
	return this.currentStep.config[index];

      var answer_ids = this.currentStep.answers[index].map(x => x.id);
      return this.currentStep.config[index].filter(a => !answer_ids.includes(a.id));
    },
    correctAnswerClass(index, article) {
      if (!this.currentStep.config[index])
	return false;

      if (this.currentStep.config[index].map(x => x.id).includes(article.id))
	return "text-success";
      else
	return "text-danger"
    },
    addArticle(index, article) {
      var target = this.stepTarget;
      if (!target[index])
	target[index] = [];
      target[index].push(article);
      this.wikiSearch = "";
      this.componentKey += 1;
    },
    delArticle(cindex, index) {
      var target = this.stepTarget;
      target[cindex].splice(index, 1);
      this.componentKey += 1;
    },
    urlToText(url) {
      return this.$parent.wikiUrlToText(url);
    },
    addSelectedWikiUrl() {
      var url = this.selectedWikiUrl;
      var index = this.problemIndex;

      if (url.indexOf('http://') === 0 || url.indexOf('https://') === 0)
	url = (new URL(this.selectedWikiUrl)).pathname;

      var target = this.editMode ? this.currentStep.config : this.currentStep.answers;
      if (!target[index])
	target[index] = [];

      var article = this.wikiArticles.filter(a => (a.url == url))[0]
      target[index].push(article);

      this.showModal = false;
      this.selectedWikiUrl = null;
    },
    async openWikiBrowser(index, url) {
      this.showModal = true;
      this.problemIndex = index;
      await nextTick();
      this.loadWikiContent(url ? url : "/problemfelder/");
    },
    loadWikiContent(url) {
      var that = this;
      this.selectedWikiUrl = url;
      $(".modal-body").load(url + " #wiki-container", function() {
	$(".modal-body a[href^=\"/problemfelder/\"]").on('click', function() {
	  that.loadWikiContent(this.href)
	  return false;
	});
	$(".modal-body a:not([href^=\"/problemfelder/\"])").on('click', function() {
	  window.open(this.href, "_blank");
	  return false;
	});
      });
    },
    wikiSearchArticles(index) {
      if (this.problemIndex != index)
	return [];

      if (this.wikiSearch.length < 2)
	return []

      var results = this.wikiArticles;
      var searchTerms = this.wikiSearch.split(" ").map(str => str.trim());

      searchTerms.forEach(term => {
	var re = RegExp(term, "i");
	results = results.filter(article =>  (article.title.search(re) >= 0));
      });

      return results;
    },
  },
}
</script>
<style lang="scss">
  @import './styles/step-problems.scss';
</style>
