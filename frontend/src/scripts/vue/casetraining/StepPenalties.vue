<template>
<step-template type="penalties" :key="componentKey">
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
    <p>
      Ermitteln Sie die zu prüfenden Strafbarkeiten in der für die Lösungsskizze korrekten Reihenfolge.
    </p>
    <div v-if="myStep == 1">
      <div v-for="(penalty, qindex) in currentStep.config">
	<h4>{{ penalty.text }}</h4>
	<SlickList axis="y" v-model="currentStep.answers[qindex]" @sort-end="reRender()">
    	  <SlickItem v-for="(answer, index) in currentStep.answers[qindex]" :key="answer" :index="index">
    	    <div class="border">
    	      <input v-model="currentStep.answers[qindex][index]" @change="handleBlur(qindex, index)" :ref="'input_' + qindex + '_' + index" :class="'input_' + qindex + '_' + index">
    	      <button v-if="currentStep.answers[qindex].length != 1" class="btn btn-success" @click="delAnswer(qindex, index)">-</button>
    	    </div>
    	  </SlickItem>
	</SlickList>
      </div>
    </div>
    <div v-if="myStep == 2">
      <div v-for="(penalty, qindex) in currentStep.config">
	<h4>{{ penalty.text }}</h4>
	<div class="row" v-for="(solution, index) in solutions(qindex)">
	  <div class="col-sm-6" :class="solution[2] ? 'text-success' : 'text-danger'">
	    <strong>{{ solution[0] }}</strong>
	  </div>
	  <div class="col-sm-6" :class="solution[3] ? 'text-danger' : ''">
	    {{ solution[1] }}
	  </div>
	</div>
	<hr/>
      </div>
    </div>
  </template>
  <template #buttons-right>
    <button v-if="myStep == 1" class="btn btn-primary" @click="nextStep()">zur Auswertung</button>
    <button v-if="myStep == 2" class="btn btn-primary" @click="nextStep()">nächster Schritt</button>
  </template>
</step-template>
</template>

<script>
import StepTemplate from "./StepTemplate.vue";
import { nextTick } from "vue";
import { SlickList, SlickItem } from 'vue-slicksort';
import { diffArrays } from "diff";

export default {
  name: "StepPenalties",
  components: {
    StepTemplate,
    SlickList,
    SlickItem,
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
      myStep: 1,
    }
  },
  computed: {
  },
  beforeMount() {
    if (typeof this.currentStep.answers !== "undefined")
      return;

    this.currentStep.answers = [];
    for (let i = 0; i < this.currentStep.config.length; i++)
      this.currentStep.answers.push([""])
  },
  mounted() {
    this.$refs.input_0_0[0].focus();
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
    solutions(qindex) {
      // filter non empty lines
      this.currentStep.answers[qindex] = this.currentStep.answers[qindex].filter(n => n);
      var count = this.currentStep.answers[qindex].length;
      if (count < this.currentStep.config[qindex].correct.length)
	count = this.currentStep.config[qindex].correct.length;

      let diff = this.xdiff(qindex);
      let correct = diff.filter(x => !x["removed"]).filter(x => !x["added"]).map(x => x["value"]).flat();
      let removed = diff.filter(x => x["removed"]).map(x => x["value"]).flat();
      var solution = []
      for (let i = 0; i < count; i++) {
	solution.push([
	  this.currentStep.answers[qindex][i],
	  this.currentStep.config[qindex].correct[i],
	  correct.includes(this.currentStep.answers[qindex][i]),
	  removed.includes(this.currentStep.config[qindex].correct[i])
	]);
      }
      return solution;
    },
    diffCmp(left, right) {
      var l = left.replace(/\s/g, "").replace("§", "").toLowerCase()
      var r = right.replace(/\s/g, "").replace("§", "").toLowerCase()
      return l == r;
    },
    xdiff(qindex) {
      return diffArrays(this.currentStep.config[qindex].correct,
			this.currentStep.answers[qindex],
			{ comparator: this.diffCmp });
    },
    async handleBlur(qindex, index) {
      this.currentStep.answers[qindex] = this.currentStep.answers[qindex].filter(n => n);
      this.currentStep.answers[qindex].push("");
      this.componentKey += 1;
      await nextTick()
      var next_index = index + 1;
      if (next_index >= this.currentStep.answers[qindex].length)
	next_index = this.currentStep.answers[qindex].length - 1;

      console.log(next_index)
      this.$refs["input_" + qindex + "_" + next_index][0].focus();
    },
    delAnswer(qindex, index) {
      this.currentStep.answers[qindex].splice(index, 1);
      this.componentKey += 1;
    },
    reRender() {
      this.componentKey += 1;
    },
  },
}
</script>
<style lang="scss">
</style>
