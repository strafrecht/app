<template>
<step-template v-else type="gap" :key="componentKey">
  <template #left>
    <div>
      <div style="position: relative">
	<div style="position: absolute; top: 0; left: 0; color: transparent; pointer-events: none;">
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
	<strong>{{ $parent.diffConfigToParentDeleted() }} Lückentext(e) gelöscht!</strong>
      </div>

      <div class="row" v-for="(question, qindex) in currentStep.config">
	<div class="col-sm-12">
	  <h6>
	    <i @click="delGapText(qindex)" class="fa fa-trash text-danger" role="button" title="Lückentext löschen"></i>
	    <strong v-if="$parent.showDiff && $parent.diffConfigToParentNew(qindex)" class="small text-danger">Neu!</strong>
	    Lückentext {{ qindex + 1 }}
	  </h6>

	  <div class="form-group">
	    <div v-if="$parent.showDiff && $parent.diffConfigToParent(qindex, 'question')" class="small text-danger">
	      <strong>Vorherige Version:</strong>
	      <div>{{ $parent.diffConfigToParent(qindex, "question") }}</div>
	    </div>

	    <input class="form-control form-control-sm" v-model="question.question" placeholder="Das [ist] ein [neuer] Lückentext.">
	    <small class="form-text text-muted">
	      Lückentexte in eckige Klammern "[Text]" einschließen.
	    </small>
	  </div>

	  <div class="form-group">
	    <div v-if="$parent.showDiff && $parent.diffConfigToParent(qindex, 'other')" class="small text-danger">
	      <strong>Vorherige Version:</strong>
	      <div style="white-space: pre-wrap">{{ $parent.diffConfigToParent(qindex, "other") }}</div>
	    </div>

	    <textarea class="form-control form-control-sm" v-model="question.other"></textarea>
	    <small class="form-text text-muted">
	      Liste von falschen Antworten, jeweils eine pro Zeile.
	    </small>
	  </div>
	</div>
      </div>
      <button class="btn btn-primary" @click="addGapText()">neuer Lückentext</button>
    </div>
    <div v-else>
      <p>{{ currentStep.intro }}</p>
      <div v-for="(question, qindex) in currentStep.config">
	<div class="row">
	  <div class="col-sm-6">
	    <h6>Lückentext {{ qindex + 1 }}</h6>
	  </div>
	</div>

	<div v-if="myStep == 1" class="row">
	  <div class="col-sm-12">
	    <span v-for="(word, index) in words(question.question)">
	      <span>{{ word }}</span>
	      <span v-if="index !== words(question.question).length - 1">
		<span class="gap-drop section-marker-5" @drop="onDrop($event, question, qindex, index)" @dragover.prevent @dragenter.prevent>
		  {{ gapWordAt(question, qindex, index) }}
		</span>
	      </span>
	    </span>
	  </div>
	  <div class="col-sm-12 draggables">
	    <div v-for="(answer, index) in gapTexts(question)" draggable @dragstart="startDrag($event, qindex, answer)">
	      <div class="gap-drag"><div class="section-marker-5">{{ answer }}</div></div>
	    </div>
	  </div>
	</div>

	<div v-if="myStep == 2" class="row">
	  <div class="col-sm-12">
	    <span v-for="(word, index) in words(question.question)">
	      <span>{{ word }}</span>
	      <span v-if="index !== words(question.question).length - 1">
		<span class="gap-drop" :class="gapWordClass(question, qindex, index)">
		  {{ gapWordAt(question, qindex, index) }}
		</span>
	      </span>
	    </span>
	  </div>
	  <div class="col-sm-12">
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

    </div>
  </template>
  <template #buttons-right v-if="!editMode">
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
    if (typeof this.currentStep.answers === "undefined")
      this.currentStep.answers = [];

    if (!this.currentStep.config)
      this.currentStep.config = [];

    if (!this.currentStep.intro)
      this.currentStep.intro = "Füllen Sie die Lücken in den Texten mit den korrekten vorgegebenen Satzbausteinen.";
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
	question: "",
	other: "",
      })
    },
    delGapText(index) {
      this.currentStep.config.splice(index, 1);
    },
    correctAnswers(question) {
      const regex = /\[.*?\]/g;
      if (question.question.match(regex) === null)
	return [""];

      return question.question.match(regex).map(w => w.substr(1, w.length - 2));
    },
    gapTexts(question) {
      return this.shuffle(this.correctAnswers(question).concat(question.other.split("\n")));
    },
    shuffle(a) {
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
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
