<template>
<div  class="case-step case-type-solution" :key="componentKey">
  <div v-if="editMode">
    <span @click="loadSolution" class="btn btn-secondary ml-2 float-right">Lösungskizze neu einlesen</span>
    <div v-if="solutionPresent">
      <a :href="wikiEditUrl" class="btn btn-primary float-right" target="_blank">Lösungsskizze bearbeiten</a>
    </div>
    <div v-else>
      <a :href="wikiCreateUrl" class="btn btn-primary float-right" target="_blank">Lösungsskizze erstellen</a>
    </div>
    <div class="clearfix mb-3"/>
  </div>
  <div id="case-solution">
    <i class="fa fa-sync fa-spin text-info mr-2"></i> Lade Lösungskizze…
  </div>
</div>
</template>

<script>
// Lösungskizzen werden im Problemfeld-Wiki unter /loesungsskizzen/ angelegt.
// Das Kürzel der Lösungskizze entspricht folgendem Schema:
// "falltraining_" + Id des Falltrainings
// Damit die Lösungskizze auch bei Überarbeitungen des Falltrainings bestehen bleibt,
// wird die Id der Lösungsskizze im Feld "solution_id" des Falltrainings gespeichert.

export default {
  name: "StepSolution",
  data() {
    return {
      componentKey: 0,
      solutionPresent: false,
    }
  },
  computed: {
    wikiUrl() {
      return "/problemfelder/loesungsskizzen/falltraining_" + this.$parent.currentCase.id + "/"
    },
    wikiEditUrl() {
      return this.wikiUrl + "_edit/"
    },
    wikiCreateUrl() {
      return "/problemfelder/loesungsskizzen/_create/?slug=falltraining_" + this.$parent.currentCase.id
    },
    editMode() {
      return this.$parent.editMode;
    },
  },
  mounted() {
    this.loadSolution();
  },
  methods: {
    loadSolution() {
      var that = this;
      $.get(this.wikiUrl, function(data) {
	var html = $(data).find("#article-container");
	if (html.length > 0) {
	  that.solutionPresent = true;
	  $("#case-solution").html(html);
	} else {
	  that.solutionPresent = false;
	  $("#case-solution").html("Keine Lösungskizze vorhanden");
	}
      });
    },
  },
}
</script>
