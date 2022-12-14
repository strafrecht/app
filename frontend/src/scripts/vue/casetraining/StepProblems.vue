<template>
<step-template type="problems" :key="componentKey">
  <template #left>
    <div v-html="currentCase.facts"></div>
  </template>
  <template #right>
    <p>
      Ermitteln Sie die Problemfelder der Sachverhaltsabschnitte.
    </p>
    <div v-for="(answer, index) in currentStep.answers">
      <div>{{ answer.title }}</div>
      <div><button class="btn btn-danger" @click="delArticle(index)">-</button></div>
    </div>
    <input v-model="wikiSearch">
    <div v-for="(article, index) in wikiSearchArticles()">
      <div><small><i>{{ article.path.join(' &gt; ') }}</i></small></div>
      <div>{{ article.title }}</div>
      <div>{{ article }}</div>
      <div><a :href="article.url" target="_blank">zum Wiki</a></div>
      <div><button class="btn btn-success" @click="addArticle(article)">hinzufügen</button></div>
	  <hr/>
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
  name: "StepProblems",
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
  },
  methods: {
    prevStep() {
      this.$parent.prevStep();
    },
    nextStep() {
      this.$parent.nextStep();
    },
    async getWikiTree() {
      await axios
        .get("/falltraining/api/wiki_categories")
        .then((response) => this.wikiTree = response.data);

      this.makeWikiEntry(this.wikiTree.children, []);
    },
    makeWikiEntry(articles, path) {
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
