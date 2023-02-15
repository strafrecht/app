<template>
<step-template type="free-text" :key="componentKey">
  <template #left>
    <div>
      <div style="position: relative">
	<div id="user-mark-area-content-outer">
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

      <div v-if="$parent.showDiff && $parent.diffConfigToParentDeleted()" class="text-danger mb-3">
	<strong>{{ $parent.diffConfigToParentDeleted() }} Frage(n) gelöscht!</strong>
      </div>

      <div class="row" v-for="(question, qindex) in currentStep.config">
	<div class="col-sm-12">
	  <h6>
	    <i @click="delFreeText(qindex)" class="fa fa-trash text-danger" role="button" title="Aufgabe löschen"></i>
	    <strong v-if="$parent.showDiff && $parent.diffConfigToParentNew(qindex)" class="small text-danger">Neu!</strong>
	    Aufgabe {{ qindex + 1 }}
	  </h6>
	  <div class="form-group">
	    <div v-if="$parent.showDiff && $parent.diffConfigToParent(qindex, 'text')" class="small text-danger">
	      <strong>Vorherige Version:</strong>
	      <div>{{ $parent.diffConfigToParent(qindex, "text") }}</div>
	    </div>

	    <textarea class="form-control form-control-sm" v-model="question.text" placeholder="Neue Aufgabe …"/>
	  </div>
	</div>
      </div>
      <button class="btn btn-primary" @click="addFreeText">neue Aufgabe</button>
    </div>
    <div v-else>
      <p>{{ currentStep.intro }}</p>
      <div v-for="(discussion, index) in currentStep.config">
	<h6 v-html="discussion.text" class="mt-3"></h6>
	<vue-editor v-model="currentStep.answers[index]" :editorToolbar="customToolbar"></vue-editor>
      </div>
      <div class="mt-4">
	<div class="form-check">
	  <input class="form-check-input" type="checkbox" value="" id="email-ok" v-model="emailOk">
	  <label class="form-check-label" for="email-ok">
	    Ich möchte eine Korrektur meiner Antworten per E-Mail erhalten!
	  </label>
	</div>
	<form id="mail-form" v-if="emailOk" class="mt-2" @submit.prevent="mailStep()">
	  <div class="form-group">
	    <label>E-Mail <sup class="text-danger">*</sup></label>
	    <input class="form-control" v-model="$parent.userEmail" placeholder="E-Mail Adresse" type="email">
	  </div>
	  <div v-if="emailOk" class="form-check">
	    <input class="form-check-input" type="checkbox" value="" id="email-privacy" v-model="emailPrivacy" required>
	    <label class="form-check-label" for="email-privacy">
	      Ich willige ein, dass ich für die Rücksendung der korrigierten Freitextantworten sowie für ein kurzes Feedback zur erhaltenen Korrektur per Mail kontaktiert werde. Eine Weitergabe der Mailadresse an Dritte erfolgt nicht. <sup class="text-danger">*</sup>
	    </label>
	  </div>
	  <div class="text-right"><sup class="text-danger">*</sup> Pflichtfelder</div>
	</form>
      </div>
    </div>
  </template>
  <template #buttons-right>
    <input v-if="emailOk && emailPrivacy && $parent.userEmail" form="mail-form" class="btn btn-primary" type="submit" value="E-Mail absenden und zum nächsten Schritt"/>
    <div v-if="!emailOk">
      <button class="btn btn-primary" @click="nextStep()">Schritt überspringen</button>
    </div>
  </template>
</step-template>
</template>

<script>
import axios from "axios";
import StepTemplate from "./StepTemplate.vue";
import { VueEditor } from "vue2-editor";

const axios_config = {
  headers: {
    'X-CSRFToken': csrf_token,
  },
  withCredentials: true,
}

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
      emailOk: false,
      emailPrivacy: false,
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
      this.currentStep.intro = "Bearbeite die folgenden Aufgaben.";
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
    async mailStep() {
      await axios
	.post("/falltraining/api/free_text_mail/" + this.$parent.currentCase.id + "/", {
	  answers: this.currentStep.answers,
	  config:  this.currentStep.config,
	  email:   this.$parent.userEmail,
	}, axios_config)
	.then(response => {
	  this.nextStep();
	})
	.catch(error => alert(error));
    },
  },
}
</script>
<style lang="scss">
</style>
