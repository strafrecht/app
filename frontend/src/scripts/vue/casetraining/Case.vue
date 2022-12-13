<template>
<div v-if="dataReady" class="casetraining">

  <div class="case-timer">
    {{ timerMinSec() }}
    <button class="btn btn-success" @click="timerPause()" v-if="timerRun">Pause</button>
    <button class="btn btn-success" @click="timerPause()" v-if="!timerRun">Resume</button>
    <button class="btn btn-success" @click="timerReset()">Reset</button>
  </div>

  <h1>Step: {{ currentStepNo }} / {{ steps() }}</h1>
  <p>{{ currentStep }}</p>
  <h2>{{ currentCase.name }} (Niveau: {{ currentCase.difficulty }})</h2>

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

  <div v-if="currentStep.step_type == 'gap_text'">
    <StepGap :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
  </div>

  <div v-if="currentStep.step_type == 'free_text'">
    <StepFreeText :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
  </div>

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
    this.currentCase.steps.forEach(element => {
      element.answers = [];
      // if (!element.config)
      // 	element.config = [{}];

      // element.config.forEach(element => {
      // 	element.answer = "";
      // });

      if (element.step_type == "mark_sections")
       	element.answers[0] = this.currentCase.facts;
    });
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
