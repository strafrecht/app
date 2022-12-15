<template>
<div v-if="dataReady" class="casetraining">

  <div class="bg-dark px-2 text-uppercase">
    <span
       class="text-white btn"
       v-for="(step, index) in currentCase.steps"
       :class="(index + 1) == currentStepNo ? 'text-success' : 'text-light'"
       @click="setStep(index + 1)">
      <small>{{ stepName(step.step_type) }}</small>
    </span>
  </div>

  <div class="case-timer bg-light border float-right p-1 rounded-pill" style="margin-top: 20px;">
    <strong>{{ timerMinSec() }}</strong>
    <button class="btn btn-success btn-sm rounded-circle" @click="timerPause()">
      <i v-if="timerRun" class="fa fa-pause" />
      <i v-else class="fa fa-play" />
    </button>
    <button class="btn btn-success btn-sm rounded-circle" @click="timerReset()">
      <i class="fa fa-undo" />
    </button>
  </div>

  <h2>{{ currentCase.name }} (Niveau: {{ currentCase.difficulty }})</h2>


  <h4>Step: {{ currentStepNo }} / {{ steps() }}</h4>

  <div v-if="currentStep.step_type == 'read'">
    <StepRead :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
  </div>

  <div v-if="currentStep.step_type == 'mark_sections'">
    <StepSections :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
  </div>

  <div v-if="currentStep.step_type == 'penalties'">
    <StepPenalties :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
  </div>

  <div v-if="currentStep.step_type == 'problem_areas'">
    <StepProblems :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
  </div>

  <div v-if="currentStep.step_type == 'weights'">
    <StepWeights :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
  </div>

  <div v-if="currentStep.step_type == 'gap_text'">
    <StepGap :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
  </div>

  <div v-if="currentStep.step_type == 'free_text'">
    <StepFreeText :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
  </div>

  <p>{{ currentStep }}</p>
  <hr/>
  <p>{{ currentCase }}</p>

</div>
<div v-else>
  <h3>Lade Fall…</h3>
</div>
</template>

<script>
import axios from "axios";
import StepRead from "./StepRead.vue";
import StepSections from "./StepSections.vue";
import StepPenalties from "./StepPenalties.vue";
import StepProblems from "./StepProblems.vue";
import StepWeights from "./StepWeights.vue";
import StepGap from "./StepGap.vue";
import StepFreeText from "./StepFreeText.vue";

const axios_config = {
  headers: {
    'X-CSRFToken': csrf_token,
  },
  withCredentials: true,
}

export default {
  name: "CurrentCase",
  components: {
    StepRead,
    StepSections,
    StepPenalties,
    StepProblems,
    StepWeights,
    StepGap,
    StepFreeText,
  },
  props: {
    caseId: {
      type: Number,
    },
  },
  data() {
    return {
      dataReady: false,
      currentStepNo: 1,
      currentCase: null,
      timerStart: null,
      timerRun: true,
      timerCurrent: null,
      timerPauseStart: null,
    }
  },
  async mounted() {
    await this.getCurrentCase();
    this.currentCase.userFacts = this.currentCase.facts
    this.dataReady = true;
    this.timerStart = Date.now();
    setInterval(() => {
      if (this.timerRun) {
	this.timerCurrent = Date.now() - this.timerStart;
      }
    }, 250);
  },
  computed: {
    currentStep() {
      return this.currentCase.steps[this.currentStepNo - 1];
    },
  },
  methods: {
    async getCurrentCase() {
      await axios
	.get("/falltraining/api/case/" + this.caseId + "/")
	.then((response) => {
	  this.currentCase = response.data;
	});
    },
    setStep(num) {
      this.currentStepNo = num;
    },
    stepName(id) {
      let name = {
	read: "Lesen",
	mark_sections: "Einteilen",
	gap_text: "Lückentext",
	free_text: "Freitext",
	penalties: "Strafbarkeit",
	problem_areas: "Probleme",
	weights: "Gewichtung",
      };

      return name[id];
    },
    timerPause() {
      if (this.timerRun)
	this.timerPauseStart = Date.now()
      else
	this.timerStart += Date.now() - this.timerPauseStart
      this.timerRun = !this.timerRun;
    },
    timerReset() {
      this.timerCurrent = 0;
      this.timerStart = Date.now();
      this.timerRun = true;
    },
    nextStep() {
      if (this.currentStepNo == this.steps()) return;

      this.currentStepNo += 1;
    },
    timerMinSec() {
      var total = Math.round(this.timerCurrent / 1000);
      var minutes = Math.floor(total / 60)
      var seconds = total % 60
      return minutes + ":" + ("0" + seconds).slice(-2)
    },
    prevStep() {
      if (this.currentStepNo == 1) return;

      this.currentStepNo -= 1;
    },
    steps() {
      return this.currentCase.steps.length;
    },
  },
};
// https://learnvue.co/tutorials/vue-drag-and-drop
// https://learnvue.co/tutorials/computed-properties-guide
// https://www.npmjs.com/package/vue-text-selection
// https://stackoverflow.com/questions/14208054/change-the-color-of-text-on-selection
// https://stackoverflow.com/questions/17288964/how-to-change-color-of-the-selected-text-dynamically-on-click-of-button
</script>

<style lang="scss">
  @import './styles.scss';
</style>
