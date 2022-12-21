<template>
<div v-if="editMode">
  <div class="row" v-for="(question, qindex) in currentStep.config">
    <div class="col-sm-12">
      <h5>Frage {{ qindex + 1 }}</h5>
      <div class="form-group">
	<input class="form-control" v-model="question.text">
      </div>
    </div>
  </div>
  <button class="btn btn-primary" @click="addFreeText">neue Frage</button>
</div>
<step-template v-else type="free-text" :key="componentKey">
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
      <h5 v-html="discussion.text"></h5>
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

    if (!this.currentStep.config)
      this.currentStep.config = [];

    this.currentStep.answers = [];
  },
  computed: {
    editMode() {
      return this.$parent.editMode;
    },
  },
  methods: {
    addFreeText() {
      this.currentStep.config.push({
	text: "Neue Frage?",
      })
    },
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
