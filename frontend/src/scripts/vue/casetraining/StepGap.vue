<template>
<div v-if="editMode">
  <div class="row" v-for="(question, qindex) in currentStep.config">
    <div class="col-sm-12">
      <h5>Frage {{ qindex + 1 }}</h5>
      <div class="form-group">
	<input class="form-control" v-model="question.question">
	<small class="form-text text-muted">
	  Lückentexte in eckige Klammern "[Text]" einschließen
	</small>
      </div>
      <div class="form-group">
	<input class="form-control" v-model="question.other">
	<small class="form-text text-muted">
	  Liste von falschen Antworten mit Komma getrennt
	</small>
      </div>
    </div>
  </div>
  <button class="btn btn-primary" @click="addGapText()">neuer Lückentext</button>
</div>
<step-template v-else type="gap" :key="componentKey">
  <template #right>
    <p>
      Füllen Sie die Lücken auf der linken Seite mit den rechts vorgegebenen Satzbausteinen.
    </p>
  </template>
  <template #bottom>
    <div v-for="(question, qindex) in currentStep.config">
      <div class="row">
	<div class="col-sm-6">
	  <h5>Frage {{ qindex + 1 }}</h5>
	</div>
      </div>

      <div v-if="myStep == 1" class="row">
	<div class="col-sm-6">
	  <span v-for="(word, index) in words(question.question)">
	    <span>{{ word }}</span>
	    <span v-if="index !== words(question.question).length - 1">
	      <span class="gap-drop section-marker-5" @drop="onDrop($event, question, qindex, index)" @dragover.prevent @dragenter.prevent>
		{{ gapWordAt(question, qindex, index) }}
	      </span>
	    </span>
	  </span>
	</div>
	<div class="col-sm-6">
	  <div v-for="(answer, index) in gapTexts(question)" draggable @dragstart="startDrag($event, qindex, answer)">
	    <div class="gap-drag section-marker-5">{{ answer }}</div>
	  </div>
	</div>
      </div>

      <div v-if="myStep == 2" class="row">
	<div class="col-sm-6">
	  <span v-for="(word, index) in words(question.question)">
	    <span>{{ word }}</span>
	    <span v-if="index !== words(question.question).length - 1">
	      <span class="gap-drop" :class="gapWordClass(question, qindex, index)">
		{{ gapWordAt(question, qindex, index) }}
	      </span>
	    </span>
	  </span>
	</div>
	<div class="col-sm-6">
	  <span v-for="(word, index) in words(question.question)">
	    <span>{{ word }}</span>
	    <span v-if="index !== words(question.question).length - 1">
	      <span class="gap-drop section-marker-2">
		{{ gapCorrectWordAt(question, qindex, index) }}
	      </span>
	    </span>
	  </span>
	</div>
      </div>

      <hr/>
    </div>
  </template>
  <template #buttons>
    <button v-if="myStep == 1" class="btn btn-primary" @click="nextStep()">zur Auswertung</button>
    <button v-if="myStep == 2" class="btn btn-primary" @click="nextStep()">nächster Schritt</button>
  </template>
</step-template>
</template>

<script>
import StepTemplate from "./StepTemplate.vue";

export default {
  name: "StepGap",
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
      myStep: 1,
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
    addGapText() {
      this.currentStep.config.push({
	question: "Das ist [ein] [neuer] Lückentext.",
	other: "kein,Apfel",
      })
    },
    correctAnswers(question) {
      const regex = /\[.*?\]/g;
      return question.question.match(regex).map(w => w.substr(1, w.length - 2));
    },
    gapTexts(question) {
      return this.correctAnswers(question).concat(question.other.split(","))
    },
    words(text) {
      const regex = /\[.*?\]/g;
      return text.split(regex);
    },
    gapWordClass(question, qindex, index) {
      if (typeof this.currentStep.answers[qindex] === 'undefined' ||
	  typeof this.currentStep.answers[qindex][index] === 'undefined')
	return "section-marker-4";

      if (this.correctAnswers(this.currentStep.config[qindex])[index] ==
	  this.currentStep.answers[qindex][index])
	return "section-marker-2";

      return "section-marker-4";
    },
    gapCorrectWordAt(question, qindex, index) {
      return this.correctAnswers(this.currentStep.config[qindex])[index];
    },
    gapWordAt(question, qindex, index) {
      if (typeof this.currentStep.answers[qindex] === 'undefined' ||
	  typeof this.currentStep.answers[qindex][index] === 'undefined' ||
	  !this.currentStep.answers[qindex][index])
	return "__________"

      return this.currentStep.answers[qindex][index];
    },
    onDrop(evt, question, qindex, index) {
      if (qindex != evt.dataTransfer.getData('qindex'))
	  return false;
      const item = evt.dataTransfer.getData('item');
      if (typeof this.currentStep.answers[qindex] === 'undefined')
	this.currentStep.answers[qindex] = Array(this.words(question.question).length - 1);
      this.currentStep.answers[qindex][index] = item;
      this.componentKey += 1;
    },
    startDrag(evt, qindex, item) {
      evt.dataTransfer.dropEffect = 'move'
      evt.dataTransfer.effectAllowed = 'move'
      evt.dataTransfer.setData('item', item)
      evt.dataTransfer.setData('qindex', qindex)
    },
  },
}
</script>
<style lang="scss">
  @import './styles/step-gap.scss';
</style>
