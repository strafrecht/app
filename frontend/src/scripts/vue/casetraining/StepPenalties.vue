<template>
<step-template type="penalties" :key="componentKey">
  <template #left>
    <div v-html="currentCase.facts"></div>
  </template>
  <template #right>
    <p>
      Ermitteln Sie die zu prüfenden Strafbarkeiten in der für die Lösungsskizze korrekten Reihenfolge.
    </p>
    <div v-for="(penalty, qindex) in currentStep.config">
      <h4>{{ penalty.text }}</h4>
      <div v-for="(answer, index) in currentStep.answers[qindex]">
	<input v-model="currentStep.answers[qindex][index]">
	<button class="btn btn-success" @click="delAnswer(qindex, index)">-</button>
      </div>
      <button class="btn btn-success" @click="addAnswer(qindex)">+</button>
	</div>
  </template>
  <template #buttons>
    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
  </template>
</step-template>
</template>

<script>
import StepTemplate from "./StepTemplate.vue";

export default {
  name: "StepPenalties",
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
    }
  },
  computed: {
    markColorStyle() {
      return "mark-area mark-" + this.markColor;
    },
  },
  methods: {
    prevStep() {
      this.$parent.prevStep();
    },
    nextStep() {
      this.$parent.nextStep();
    },
    delAnswer(qindex, index) {
      this.currentStep.answers[qindex].splice(index, 1);
      this.componentKey += 1;
    },
    addAnswer(qindex) {
      if (typeof this.currentStep.answers[qindex] === 'undefined')
	this.currentStep.answers[qindex] = [];
      this.currentStep.answers[qindex].push("")
      this.componentKey += 1;
    },
  },
}
</script>
<style lang="scss">
</style>
