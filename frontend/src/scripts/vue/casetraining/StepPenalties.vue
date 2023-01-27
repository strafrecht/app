<template>
<step-template type="penalties" :key="componentKey">
  <template #left>
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
	<textarea class="form-control" v-model="currentStep.intro" />
      </div>
    </div>
    <div v-else>
      <p>{{ currentStep.intro }}</p>
    </div>

    <div v-if="editMode">
      <div class="row" v-for="(penalty, qindex) in currentStep.config">
	<div class="col-sm-12">
	  <h5>
	    <i @click="delPerson(qindex)" class="fa fa-trash text-danger" role="button" title="Person löschen"></i>
	    Person {{ qindex + 1 }}
	  </h5>
	  <div class="form-group">
	    <input class="form-control" v-model="penalty.text">
	  </div>
	  <div class="form-group">
	    <div class="row mb-2" v-for="(answer, index) in currentStep.config[qindex].correct">
	      <div class="col-6">
		<label class="small">
		  <i @click="delPersonAnswer(qindex, index)" class="fa fa-trash text-danger" role="button" title="Antwort löschen"></i>
		  Antwort {{ index + 1 }}
		</label>
		<input class="form-control form-control-sm" v-model="currentStep.config[qindex].correct[index]" placeholder="§ ...">
	      </div>
	      <div class="col-6">
		<label class="small">Alternative Schreibweisen</label>
		<textarea class="form-control form-control-sm" v-model="currentStep.config[qindex].alternatives[index]" />
		<small class="form-text text-muted">
		   Eine pro Zeile
		</small>
	      </div>
	    </div>
	    <button class="btn btn-secondary btn-sm" @click="addPersonAnswer(qindex)">neue Strafbarkeit</button>
	  </div>
	</div>
      </div>
      <button class="btn btn-primary" @click="addPerson">neue Person</button>
    </div>

    <div v-if="!editMode && myStep == 1">
      <div v-for="(penalty, qindex) in currentStep.config">
	<h5>{{ penalty.text }}</h5>
	<SlickList axis="y" v-model="currentStep.answers[qindex]" @sort-end="reRender()">
    	  <SlickItem v-for="(answer, index) in currentStep.answers[qindex]" :key="answer" :index="index">
    	    <div class="mb-1">
	      <div class="input-group">
    		<input class="form-control border-top-0 border-right-0 border-left-0 rounded-0" v-model="currentStep.answers[qindex][index]" @change="handleChange(qindex, index)" :ref="'input_' + qindex + '_' + index" :class="'input_' + qindex + '_' + index" placeholder="§ ...">
		<div v-if="currentStep.answers[qindex].length != index + 1" class="input-group-append">
		  <button class="btn" @click="delAnswer(qindex, index)"><i style="pointer-events: none; user-select: none;" class="fa fa-trash"></i></button>
		  <span class="input-group-text border-0 bg-white"><i class="fa fa-bars"></i></span>
		</div>
	      </div>

    	    </div>
    	  </SlickItem>
	</SlickList>
      </div>
    </div>
    <div v-if="!editMode && myStep == 2">
      <div v-for="(penalty, qindex) in currentStep.config">
	<h5>{{ penalty.text }}</h5>
	<div class="row" v-for="(solution, index) in solutions(qindex)">
	  <div class="col-sm-6 border-bottom py-2" :class="solution[2] ? 'text-success' : 'text-danger'">
	    <strong>{{ solution[0] }}</strong>
	  </div>
	  <div class="col-sm-6 border-bottom py-2" :class="solution[3] ? 'text-danger' : ''">
	    {{ solution[1] }}
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
    editMode() {
      return this.$parent.editMode;
    },
  },
  beforeMount() {
    if (typeof this.currentStep.answers === "undefined")
      this.currentStep.answers = [];

    if (!this.currentStep.config)
      this.currentStep.config = [];

    if (!this.currentStep.intro)
      this.currentStep.intro = "Ermitteln Sie die zu prüfenden Strafbarkeiten in der für die Lösungsskizze korrekten Reihenfolge.";

    for (let i = 0; i < this.currentStep.config.length; i++) {
      if (typeof this.currentStep.answers[i] === "undefined")
	this.currentStep.answers[i] = [];

      if (this.currentStep.answers[i].slice(-1)[0] != "")
	this.currentStep.answers[i].push("")
    }
  },
  mounted() {
    // FIXME: error in edit mode
    try {
      this.$refs.input_0_0[0].focus();
    } catch {
      console.log("not found");
    }
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
    delPerson(index) {
      this.currentStep.config.splice(index, 1);
    },
    delPersonAnswer(qindex, index) {
      this.currentStep.config[qindex].correct.splice(index, 1);
      this.currentStep.config[qindex].alternatives.splice(index, 1);
    },
    addPerson() {
      this.currentStep.config.push({
	text: "Strafbarkeit von X",
	correct: [""],
	alternatives: [""],
      })
    },
    addPersonAnswer(index) {
      this.currentStep.config[index].correct.push("")
      this.currentStep.config[index].alternatives.push("")
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
      let l = left.replace(/\s/g, "").replace("§", "").toLowerCase()
      let answers = right.split("\n").map(
	answer => answer.replace(/\s/g, "").replace("§", "").toLowerCase()
      );
      return answers.includes(l);
    },
    xdiff(qindex) {
      let combined = this.currentStep.config[qindex].correct.map(
	(answer, index) => [answer, this.currentStep.config[qindex].alternatives[index]].join("\n")
      );
      return diffArrays(combined,
			this.currentStep.answers[qindex],
			{ comparator: this.diffCmp });
    },
    async handleChange(qindex, index) {
      console.log("change");
      this.currentStep.answers[qindex] = this.currentStep.answers[qindex].filter(n => n);
      this.currentStep.answers[qindex].push("");
      this.componentKey += 1;
      await nextTick();
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
