<template>
<step-template type="free-text" :key="componentKey">
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
      Bearbeiten Sie die folgenden Aufgaben.
    </p>
    <div v-for="(discussion, index) in currentStep.config">
      <div v-html="discussion.text"></div>
      <vue-editor v-model="currentStep.answers[index]" :editorToolbar="customToolbar"></vue-editor>
    </div>
  </template>
  <template #buttons-right>
    <button class="btn btn-primary" @click="nextStep()">nächster Schritt</button>
  </template>
</step-template>
</template>

<script>
import StepTemplate from "./StepTemplate.vue";
import { VueEditor } from "vue2-editor";

export default {
  name: "StepRead",
  components: {
    StepTemplate,
    VueEditor,
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
      customToolbar: [
        ["bold", "italic"],
        [{ list: "ordered" }, { list: "bullet" }],
      ],
    }
  },
  beforeMount() {
    if (typeof this.currentStep.answers !== "undefined")
      return;

    this.currentStep.answers = [];
  },
  methods: {
    prevStep() {
      this.$parent.prevStep();
    },
    nextStep() {
      this.$parent.nextStep();
    },
  },
}
</script>
<style lang="scss">
</style>
