<template>
<step-template type="read">
  <template #left>
    <div v-html="currentCase.facts"></div>
  </template>
  <template #right>
    <p>
      Lesen Sie den Sachverhalt.
    </p>
  </template>
  <template #buttons>
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
    }
  },
  methods: {
    nextStep() {
      this.$parent.nextStep();
    },
  },
}
</script>
