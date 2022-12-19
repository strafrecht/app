<template>
<step-template type="problems" :key="componentKey">
  <template #left>
    <div>
      <div style="position: relative">
	<div style="position: absolute; top: 0; left: 0; color: transparent; pointer-events: none;">
	  <div id="user-mark-area-content" v-html="currentCase.userFacts"></div>
	</div>
	<div id="mark-area-content" v-html="currentCase.facts" @mouseup="markUp()"></div>
      </div>
    </div>
  </template>
  <template #right>
    {{ dataReady }}
    <div v-if="myStep == 1">
      <p>
	Ermitteln Sie die Gewichtung.
      </p>
      <div v-for="(article, index) in currentArticles()">
	{{ article.title }}
	<hr/>
      </div>
    </div>
    <div v-if="myStep == 2">
      <p>
	Ermitteln Sie die Gewichtung.
      </p>
      <div v-for="(article, index) in currentArticles()">
	{{ article.title }}: {{ article.weight }}
	<hr/>
      </div>
    </div>
  </template>
  <template #buttons>
    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
  </template>
</step-template>
</template>

<script>
import axios from "axios";
import StepTemplate from "./StepTemplate.vue";

export default {
  name: "StepWeights",
  components: {
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
      dataReady: false,
      myStep: 1,
      componentKey: 0,
      wikiSearch: "",
      wikiTree: null,
      wikiArticles: [],
    }
  },
  beforeMount() {
    if (typeof this.currentStep.answers !== "undefined")
      return;

    this.currentStep.answers = [];
  },
  async mounted() {
    await this.getWikiTree();
    this.dataReady = true;
  },
  methods: {
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
    async getWikiTree() {
      await axios
        .get("/falltraining/api/wiki_categories")
        .then((response) => this.wikiTree = response.data);

      await this.makeWikiEntry(this.wikiTree.children, []);
    },
    async makeWikiEntry(articles, path) {
      articles.forEach(article => {
	this.wikiArticles.push({
	  id: article.id,
	  title: article.title,
	  url: article.url,
	  path: path,
	});
	this.makeWikiEntry(article.children, path.concat([article.title]))
      });
    },
    currentArticles() {
      console.log("x");
      console.log(this.currentStep.config.map(x => x.article));
      console.log(this.wikiArticles[0]);
      let x = this.wikiArticles.filter(
	article =>
	  this.currentStep.config.map(x => x.article).includes(article.id)
      );
      console.log(x);
      return x;
    },
    correctAnswer(id) {
      return this.currentStep.config.map(x => x.article).includes(id);
    },
    addArticle(article) {
      this.currentStep.answers.push(article);
      this.wikiSearch = "";
      this.componentKey += 1;
    },
    delArticle(index) {
      this.currentStep.answers.splice(index, 1);
      this.componentKey += 1;
    },
    wikiSearchArticles() {
      if (this.wikiSearch.length < 3)
	return []

      var re = RegExp(this.wikiSearch, "i");

      return this.wikiArticles.filter(
	article =>
	  (article.title.search(re) >= 0)
      );
    },
  },
}
</script>
<style lang="scss">
</style>
