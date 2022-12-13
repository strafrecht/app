<template>
<step-template type="free-text" :key="componentKey">
  <template #left>
    <div v-html="currentCase.facts"></div>
  </template>
  <template #right>
    <h4>Step {{ currentStepNo }}</h4>
    <p>
      Bearbeiten Sie die folgenden Aufgaben.
    </p>
    <div v-for="(discussion, index) in currentStep.config">
      <div v-html="discussion.text"></div>
      <textarea v-model="currentStep.answers[index]" ></textarea>
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
  name: "StepRead",
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
  methods: {
    nextStep() {
      this.$parent.nextStep();
    },
  },
}
</script>
