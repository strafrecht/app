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
    <div v-if="editMode">
      <div class="mb-3">
	<label>Einleitungstext</label>
	<textarea class="form-control" v-model="currentStep.intro" />
      </div>
      <div class="row" v-for="(question, qindex) in currentStep.config">
	<div class="col-sm-12">
	  <h5>
	    <i @click="delFreeText(qindex)" class="fa fa-trash text-danger" role="button" title="Aufgabe löschen"></i>
	    Aufgabe {{ qindex + 1 }}
	  </h5>
	  <div class="form-group">
	    <input class="form-control" v-model="question.text" placeholder="Neue Aufgabe …">
	  </div>
	</div>
      </div>
      <button class="btn btn-primary" @click="addFreeText">neue Aufgabe</button>
    </div>
    <div v-else>
      <p>{{ currentStep.intro }}</p>
      <div v-for="(discussion, index) in currentStep.config">
	<h5 v-html="discussion.text" class="mt-3"></h5>
	<vue-editor v-model="currentStep.answers[index]" :editorToolbar="customToolbar"></vue-editor>
      </div>
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
    if (typeof this.currentStep.answers === "undefined")
      this.currentStep.answers = [];

    if (!this.currentStep.config)
      this.currentStep.config = [];

    if (!this.currentStep.intro)
      this.currentStep.intro = "Bearbeiten Sie die folgenden Aufgaben.";
  },
  computed: {
    editMode() {
      return this.$parent.editMode;
    },
  },
  methods: {
    addFreeText() {
      this.currentStep.config.push({
	text: "",
      })
    },
    delFreeText(index) {
      this.currentStep.config.splice(index, 1);
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
