<template>
<step-template v-else type="gap" :key="componentKey">
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
	<strong>{{ $parent.diffConfigToParentDeleted() }} Lückentext(e) gelöscht!</strong>
      </div>

      <div class="row" v-for="(question, qindex) in currentStep.config">
	<div class="col-sm-12">
	  <h6>
	    <i @click="delGapText(qindex)" class="fa fa-trash text-danger" role="button" title="Lückentext löschen"></i>
	    <strong v-if="$parent.showDiff && $parent.diffConfigToParentNew(qindex)" class="small text-danger">Neu!</strong>
	    <strong>Lückentext {{ qindex + 1 }}</strong>
	  </h6>

	  <div class="form-group">
	    <div v-if="$parent.showDiff && $parent.diffConfigToParent(qindex, 'question')" class="small text-danger">
	      <strong>Vorherige Version:</strong>
	      <div>{{ $parent.diffConfigToParent(qindex, "question") }}</div>
	    </div>

	    <textarea class="form-control form-control-sm" v-model="question.question" placeholder="Das [ist] ein [neuer] Lückentext."/>
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
      <p style="white-space: pre-line">{{ currentStep.intro }}</p>
      <p class="mt-2 mb-2 d-lg-none">
	<em>Hinweis für mobile Geräte: Klicke zunächst auf eine Lücke und anschließend auf einen Satzbaustein.</em>
      </p>
      <div v-for="(question, qindex) in currentStep.config" class="mt-3 mb-4">
	<h6><strong>Lückentext {{ qindex + 1 }}</strong></h6>
	<div v-if="myStep == 1">
	  <span v-for="(word, index) in words(question.question)">
	    <span>{{ word }}</span>
	    <span v-if="index !== words(question.question).length - 1">
	      <span class="gap-drop" :class="gapMarker(qindex, index)" @click="markGap(qindex, index)" @drop="onDrop($event, qindex, index)" @dragover.prevent @dragenter.prevent>
		{{ gapWordAt(question, qindex, index) }}
	      </span>
	    </span>
	  </span>
	  <div class="draggables border mt-3">
	    <div v-for="(answer, index) in reorderedTexts[qindex]" @click="fillGap(qindex, answer)" draggable @dragstart="startDrag($event, qindex, answer)">
	      <div class="gap-drag"><div class="section-marker-5">{{ answer }}</div></div>
	    </div>
	  </div>
	</div>

	<div v-if="myStep == 2">
	  <div>
	    <strong v-if="isCorrect(question,qindex)" class="text-success">Richtig!</strong>
	    <strong v-else class="text-danger">Deine Antwort</strong>
	    <br/>
	    <span v-for="(word, index) in words(question.question)">
	      <span>{{ word }}</span>
	      <span v-if="index !== words(question.question).length - 1">
		<span class="gap-drop" :class="gapWordClass(question, qindex, index)">
		  {{ gapWordAt(question, qindex, index) }}
		</span>
	      </span>
	    </span>
	  </div>
	  <div v-if="!isCorrect(question,qindex)">
	    <strong>Richtige Antwort</strong><br/>
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
      reorderedTexts: {},
      myStep: 1,
      markedGap: [],
    }
  },
  beforeMount() {
    if (typeof this.currentStep.answers === "undefined")
      this.currentStep.answers = [];

    if (!this.currentStep.config)
      this.currentStep.config = [];

    if (!this.currentStep.intro)
      this.currentStep.intro = "Fülle die Lücken in den Texten mit den korrekten vorgegebenen Satzbausteinen.";

    this.currentStep.config.forEach((question, index) => {
      this.reorderedTexts[index] = this.gapTexts(question);
    });
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
      return this._shuffle(this.correctAnswers(question).concat(question.other.split("\n")));
    },
    _shuffle(a) {
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
    gapMarker(qindex, index) {
      if (this.markedGap[0] === qindex && this.markedGap[1] === index)
	return "section-marker-3";

      return "section-marker-5";
    },
    markGap(qindex, index) {
      this.markedGap = [qindex, index];
    },
    fillGap(qindex, answer) {
      if (this.markedGap[0] !== qindex)
	return;

      this.setGap(qindex, this.markedGap[1], answer);
    },
    onDrop(evt, qindex, index) {
      if (qindex != evt.dataTransfer.getData('qindex'))
	  return false;
      const answer = evt.dataTransfer.getData('item');
      this.setGap(qindex, index, answer);
    },
    setGap(qindex, index, answer) {
      if (typeof this.currentStep.answers[qindex] === 'undefined')
	this.currentStep.answers[qindex] =
	Array(this.words(this.currentStep.config[qindex].question).length - 1);
      this.currentStep.answers[qindex][index] = answer;
      this.componentKey += 1;
    },
    startDrag(evt, qindex, item) {
      evt.dataTransfer.dropEffect = 'move'
      evt.dataTransfer.effectAllowed = 'move'
      evt.dataTransfer.setData('item', item)
      evt.dataTransfer.setData('qindex', qindex)
    },
    isCorrect(question,index) {
      /* WARNING: arrays must not contain {objects} or behavior may be undefined */
      return JSON.stringify(this.correctAnswers(question)) ===
	JSON.stringify(this.currentStep.answers[index]);
    }
  },
}
</script>
<style lang="scss">
  @import './styles/step-gap.scss';
</style>
