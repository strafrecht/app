<template>
<step-template type="weights" :key="componentKey">
  <template #left>
    <div>
      <div style="position: relative">
	<div id="user-mark-area-content-outer">
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
	<p>Weise für alle Problemfelder zwischen einem und drei Gewichten zu.</p>
      </div>
    </div>
    <div v-else>
      <p>{{ currentStep.intro }}</p>
    </div>

    <div>
      <div v-for="(marker, cindex) in $parent.sectionMarkers" class="mb-3">
	<h5 class="section" :class="marker">Abschnitt {{ cindex + 1 }}</h5>
	<div v-for="(article, index) in problemsConfig(cindex)" class="border-bottom my-2 pb-2">
	  <div class="clearfix">
	    <div class="float-right weights-area">
	      <span @click="setWeight(cindex, index, 1)" class="weight" :class="weightOn(cindex, index, 1)"></span>
	      <span @click="setWeight(cindex, index, 2)" class="weight" :class="weightOn(cindex, index, 2)"></span>
	      <span @click="setWeight(cindex, index, 3)" class="weight" :class="weightOn(cindex, index, 3)"></span>
	    </div>
	    <i class="small">{{ urlToText(article.url) }}</i>
	    <div>
	      <a :href="article.url" target="_blank">{{ article.title }}</a>
	    </div>
	    <div v-if="$parent.showDiff && $parent.diffConfigToParent(cindex, index)" class="small text-danger">
	      <strong>Vorherige Gewichtung:</strong>
	      <div>{{ $parent.diffConfigToParent(cindex, index) }}</div>
	    </div>

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
      myStep: 1,
      componentKey: 0,
    }
  },
  computed: {
    wikiReady() {
      return this.$parent.wikiReady;
    },
    wikiArticles() {
      return this.$parent.wikiArticles;
    },
    problemsStep() {
      return this.$parent.currentCase.steps.filter(step => step.step_type == "problem_areas")[0];
    },
    editMode() {
      return this.$parent.editMode;
    },
  },
  beforeMount() {
    if (!this.currentStep.answers)
      this.currentStep.answers = this.problemsStep.config.map(a => a.map(b => 1));

    if (!this.currentStep.config)
      this.currentStep.config = this.problemsStep.config.map(a => a.map(b => 1));

    if (!this.currentStep.intro)
      this.currentStep.intro = "Gewichte die Problemfelder. Insgesamt sind X Gewichte zu vergeben.";
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
    setWeight(cindex, index, weight) {
      if (this.myStep == 2)
	return false;

      var target = this.editMode ? this.currentStep.config : this.currentStep.answers
      if (!target[cindex])
	target[cindex] = [];

      target[cindex][index] = weight;
      this.componentKey += 1;
    },
    problemsConfig(index) {
      return this.problemsStep.config[index];
    },
    weightOn(cindex, index, weight) {
      if (this.myStep == 2)
	return this.weightResult(cindex, index, weight);

      var target = this.editMode ? this.currentStep.config : this.currentStep.answers
      if (!target[cindex])
	target[cindex] = [];

      if (target[cindex][index] >= weight)
	return "on";

      return "";
    },
    weightResult(cindex, index, weight) {
      var config = this.currentStep.config[cindex][index];
      var answer = this.currentStep.answers[cindex][index];

      if (answer == config) {
	if (weight <= config)
	  return "on";
	else
	  return "";
      }

      if (answer > config) {
	if (weight <= config)
	  return "on";
	if (weight <= answer)
	  return "result-minus";
	return "";
      }

      if (answer < config) {
	if (weight <= answer)
	  return "on";
	if (weight <= config)
	  return "result-plus";
	return "";
      }
    },
    urlToText(url) {
      return this.$parent.wikiUrlToText(url);
    },
  },
}
</script>
<style lang="scss">
  @import './styles/step-weights.scss';
</style>
