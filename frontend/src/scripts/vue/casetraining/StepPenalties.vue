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
	<div class="small text-danger" v-if="$parent.showDiff && $parent.diffIntroToParent()">
	  <strong>Vorherige Version</strong>
	  <div>{{ $parent.diffIntroToParent() }}</div>
	</div>
	<textarea class="form-control" v-model="currentStep.intro" />
      </div>
    </div>
    <div v-else>
      <p>{{ currentStep.intro }}</p>
    </div>

    <div class="mb-3" v-for="(marker, cindex) in $parent.sectionMarkers">
      <h5 class="section" :class="marker">Abschnitt {{ cindex + 1 }}</h5>

      <div v-if="editMode">

	<div v-if="$parent.showDiff && $parent.diffConfigToParentDeleted(cindex)" class="text-danger mb-3">
	  <strong>{{ $parent.diffConfigToParentDeleted(cindex) }} Person(en) gelöscht!</strong>
	</div>
	<div class="row" v-for="(penalty, qindex) in currentStep.config[cindex]">
	  <div class="col-sm-12">
	    <h6>
	      <i @click="delPerson(cindex, qindex)" class="fa fa-trash text-danger" role="button" title="Person löschen"></i>
	      <strong v-if="$parent.showDiff && $parent.diffConfigToParentNew(cindex, qindex)" class="small text-danger">Neu!</strong>
	      Person {{ qindex + 1 }}
	    </h6>
	    <div class="form-group">
	      <div v-if="$parent.showDiff && $parent.diffConfigToParent(cindex, qindex, 'text')" class="small text-danger">
		<strong>Vorherige Version:</strong>
		<div>{{ $parent.diffConfigToParent(cindex, qindex, "text") }}</div>
	      </div>

	      <input class="form-control" v-model="penalty.text">
	    </div>
	    <div class="form-group">
	      <div class="row mb-2" v-for="(answer, index) in currentStep.config[cindex][qindex].correct">
		<div class="col-6">
		  <label class="small">
		    <i @click="delPersonAnswer(cindex, qindex, index)" class="fa fa-trash text-danger" role="button" title="Antwort löschen"></i>
		    Antwort {{ index + 1 }}
		  </label>

		  <div v-if="$parent.showDiff && $parent.diffConfigToParent(cindex, qindex, 'correct', index)" class="small text-danger">
		    <strong>Vorherige Version:</strong>
		    <div>{{ $parent.diffConfigToParent(cindex, qindex, "correct", index) }}</div>
		  </div>

		  <input class="form-control form-control-sm" v-model="currentStep.config[cindex][qindex].correct[index]" placeholder="§ ...">
		</div>
		<div class="col-6">
		  <label class="small">Alternative Schreibweisen</label>
		  <div v-if="$parent.showDiff && $parent.diffConfigToParent(cindex, qindex, 'alternatives', index)" class="small text-danger">
		    <strong>Vorherige Version:</strong>
		    <div style="white-space: pre-wrap">{{ $parent.diffConfigToParent(cindex, qindex, "alternatives", index) }}</div>
		  </div>

		  <textarea class="form-control form-control-sm" v-model="currentStep.config[cindex][qindex].alternatives[index]" />
		  <small class="form-text text-muted">
		    Eine pro Zeile
		  </small>
		</div>
	      </div>
	      <button class="btn btn-secondary btn-sm" @click="addPersonAnswer(cindex, qindex)">neue Strafbarkeit</button>
	    </div>
	  </div>
	</div>
	<button class="btn btn-primary" @click="addPerson(cindex)">neue Person</button>
      </div>

      <div v-if="!editMode && myStep == 1">
	<div v-for="(penalty, qindex) in currentStep.config[cindex]">
	  <h6>{{ penalty.text }}</h6>
	  <SlickList axis="y" v-model="currentStep.answers[cindex][qindex]" @sort-end="reRender()">
    	    <SlickItem v-for="(answer, index) in currentStep.answers[cindex][qindex]" :key="answer" :index="index">
    	      <div class="mb-1">
		<div class="input-group">
    		  <input class="form-control border-top-0 border-right-0 border-left-0 rounded-0" v-model="currentStep.answers[cindex][qindex][index]" @change="handleChange(cindex, qindex, index)" :ref="'input_' + cindex + '_' + qindex + '_' + index" placeholder="§ ...">
		  <div v-if="currentStep.answers[cindex][qindex].length != index + 1" class="input-group-append">
		    <button class="btn" @click="delAnswer(cindex, qindex, index)"><i style="pointer-events: none; user-select: none;" class="fa fa-trash"></i></button>
		    <span class="input-group-text border-0 bg-white"><i class="fa fa-bars"></i></span>
		  </div>
		</div>
    	      </div>
    	    </SlickItem>
	  </SlickList>
	</div>
      </div>

      <div v-if="!editMode && myStep == 2">
	<div v-for="(penalty, qindex) in currentStep.config[cindex]">
	  <h6>{{ penalty.text }}</h6>
	  <div class="row" v-for="(solution, index) in solutions(cindex, qindex)">
	    <div class="col-sm-6 border-bottom py-2" :class="solution[2] ? 'text-success' : 'text-danger'">
	      <strong>{{ solution[0] }}</strong>
	    </div>
	    <div class="col-sm-6 border-bottom py-2" :class="solution[3] ? 'text-danger' : ''">
	      {{ solution[1] }}
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
      this.currentStep.config = [[]];

    if (!this.currentStep.intro)
      this.currentStep.intro = "Ermitteln Sie die zu prüfenden Strafbarkeiten in der für die Lösungsskizze korrekten Reihenfolge.";

    for (let i = 0; i < this.currentStep.config.length; i++) {
      if (typeof this.currentStep.answers[i] === "undefined")
	this.currentStep.answers[i] = [];

      for (let j = 0; j < this.currentStep.config[i].length; j++) {
	if (typeof this.currentStep.answers[i][j] === "undefined")
	  this.currentStep.answers[i][j] = [];

	if (this.currentStep.answers[i][j].slice(-1)[0] != "")
	  this.currentStep.answers[i][j].push("")
      }
    }
  },
  mounted() {
    // FIXME: error in edit mode
    try {
      this.$refs.input_0_0_0[0].focus();
    } catch {
      //console.log("not found");
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
    delPerson(cindex, index) {
      this.currentStep.config[cindex].splice(index, 1);
      this.componentKey += 1;
    },
    delPersonAnswer(cindex, qindex, index) {
      this.currentStep.config[cindex][qindex].correct.splice(index, 1);
      this.currentStep.config[cindex][qindex].alternatives.splice(index, 1);
      this.componentKey += 1;
    },
    addPerson(cindex) {
      if (!this.currentStep.config[cindex])
	this.currentStep.config[cindex] = [];

      this.currentStep.config[cindex].push({
	text: "Strafbarkeit von …",
	correct: [""],
	alternatives: [""],
      })
      this.componentKey += 1;
    },
    addPersonAnswer(cindex, index) {
      this.currentStep.config[cindex][index].correct.push("")
      this.currentStep.config[cindex][index].alternatives.push("")
      this.componentKey += 1;
    },
    delAnswer(cindex, qindex, index) {
      this.currentStep.answers[cindex][qindex].splice(index, 1);
      this.componentKey += 1;
    },
    solutions(cindex, qindex) {
      // filter non empty lines
      this.currentStep.answers[cindex][qindex] = this.currentStep.answers[cindex][qindex].filter(n => n);
      var count = this.currentStep.answers[cindex][qindex].length;
      if (count < this.currentStep.config[cindex][qindex].correct.length)
	count = this.currentStep.config[cindex][qindex].correct.length;
      let diff = this.xdiff(cindex, qindex);
      let correct = diff.filter(x => !x["removed"]).filter(x => !x["added"]).map(x => x["value"]).flat();
      let removed = diff.filter(x => x["removed"]).map(x => x["value"]).flat();
      var solution = []
      for (let i = 0; i < count; i++) {
	solution.push([
	  this.currentStep.answers[cindex][qindex][i],
	  this.currentStep.config[cindex][qindex].correct[i],
	  correct.includes(this.currentStep.answers[cindex][qindex][i]),
	  removed.includes(this.currentStep.config[cindex][qindex].correct[i])
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
    xdiff(cindex, qindex) {
      let combined = this.currentStep.config[cindex][qindex].correct.map(
	(answer, index) => [answer, this.currentStep.config[cindex][qindex].alternatives[index]].join("\n")
      );
      return diffArrays(combined,
			this.currentStep.answers[cindex][qindex],
			{ comparator: this.diffCmp });
    },
    async handleChange(cindex, qindex, index) {
      this.currentStep.answers[cindex][qindex] = this.currentStep.answers[cindex][qindex].filter(n => n);
      this.currentStep.answers[cindex][qindex].push("");
      await this.reRender();
      var next_index = index + 1;
      if (next_index >= this.currentStep.answers[cindex][qindex].length)
	next_index = this.currentStep.answers[cindex][qindex].length - 1;
      this.$refs["input_" + cindex + "_" + qindex + "_" + next_index][0].focus();
    },
    async reRender() {
      this.componentKey += 1;
      await nextTick();
    },
  },
}
</script>
<style lang="scss">
</style>
