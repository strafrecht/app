<template>
<step-template type="gap" :key="componentKey">
  <template #right>
    <p>
      Füllen Sie die Lücken auf der linken Seite mit den rechts vorgegebenen Satzbausteinen.
    </p>
  </template>
  <template #bottom>
    <div v-if="myStep == 1">
      <div v-for="(question, qindex) in currentStep.config">
	<div class="row">
	  <div class="col-sm-6">
	    <h4>Frage {{ qindex + 1 }}</h4>
	  </div>
	</div>
	<div class="row">
	  <div class="col-sm-6">
	    <span v-for="(word, index) in words(question.question)">
	      <span>{{ word }}</span>
	      <span v-if="index !== words(question.question).length - 1">
		<span class="gap-drop gap-open" @drop="onDrop($event, question, qindex, index)" @dragover.prevent @dragenter.prevent>
		  {{ gapWordAt(question, qindex, index) }}
		</span>
	      </span>
	    </span>
	  </div>
	  <div class="col-sm-6">
	    <div v-for="(answer, index) in gapTexts(question)" draggable @dragstart="startDrag($event, qindex, answer)">
	      <div class="gap-drag gap-open">{{ answer }}</div>
	    </div>
	  </div>
	</div>
	<hr/>
      </div>
    </div>
    <div v-if="myStep == 2">
      <div v-for="(question, qindex) in currentStep.config">
	<div class="row">
	  <div class="col-sm-6">
	    <h4>Frage {{ qindex + 1 }}</h4>
	  </div>
	</div>
	<div class="row">
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
		<span class="gap-drop gap-correct">
		  {{ gapCorrectWordAt(question, qindex, index) }}
		</span>
	      </span>
	    </span>
	  </div>
	</div>
	<hr/>
      </div>
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

    this.currentStep.answers = [];
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
    gapTexts(question) {
      return question.correct.concat(question.other)
    },
    words(text) {
      return text.split("_");
    },
    gapWordClass(question, qindex, index) {
      if (typeof this.currentStep.answers[qindex] === 'undefined' ||
	  typeof this.currentStep.answers[qindex][index] === 'undefined')
	return "gap-incorrect";

      if (this.currentStep.config[qindex].correct[index] ==
	  this.currentStep.answers[qindex][index])
	return "gap-correct";

      return "gap-incorrect";
    },
    gapCorrectWordAt(question, qindex, index) {
      return this.currentStep.config[qindex].correct[index];
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
