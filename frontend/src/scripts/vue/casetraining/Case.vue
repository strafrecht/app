<template>
<div v-if="dataReady" class="casetraining">

  <button v-if="editMode" @click="editModeOff" class="btn btn-success">Bearbeitung beenden</button>
  <button v-else @click="editModeOn" class="btn btn-success">bearbeiten</button>
  <button v-if="editMode && !caseId" class="btn btn-success" @click="createCase()">Erstellen</button>
  <button v-if="editMode && caseId" class="btn btn-success" @click="saveCase()">Speichern</button>
  <div class="bg-dark px-2 text-uppercase">
    <span
       class="text-white btn"
       :class="editConfig ? 'text-success' : 'text-light'"
       v-if="editMode"
       @click="setEditConfig">
      <small>Konfiguration</small>
    </span>
    <span
       class="text-white btn"
       v-for="(step, index) in currentCase.steps"
       :class="(index + 1) == currentStepNo && !editConfig ? 'text-success' : 'text-light'"
       @click="setStep(index + 1)">
      <small>{{ stepName(step.step_type) }}</small>
    </span>
  </div>

  <div v-if="editConfig">
    <div class="row">
      <div class="col-sm-6">
	<div class="form-group">
	  <label>Titel</label>
	  <input class="form-control" v-model="currentCase.name" placeholder="Titel des Falltrainings">
	</div>
      </div>
      <div class="col-sm-6">
	<div class="form-group">
	  <label>Niveau</label>
	  <select class="form-control" v-model="currentCase.difficulty">
	    <option disabled value="">Bitte wählen</option>
	    <option v-for="(name, value) in difficulties" :value="value">
	      {{ name }}
	    </option>
	  </select>
	</div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
	<div class="form-group">
	  <label>Sachverhalt</label>
	  <vue-editor id="facts-editor" v-model="currentCase.facts" :editorToolbar="factsToolbar"></vue-editor>
	</div>
      </div>
      <div class="col-sm-6">
	<div class="form-group">
	  <label>Falltrainigsschritte</label>
	  <SlickList axis="y" v-model="currentCase.steps">
	    <SlickItem v-for="(step, index) in currentCase.steps" :key="step.step_type" :index="index">
	      <div class="border my-1 px-2 py-1 bg-white">
		<span style="pointer-events: none; user-select: none;">
		  <i class="mr-2 fa fa-bars"></i>
		  {{ stepName(step.step_type) }}
		</span>
		<button @click="delStep(index)" class="btn btn-sm text-danger float-right"><i style="pointer-events: none;" class="fa fa-trash"></i></button>
	      </div>
	    </SlickItem>
	  </SlickList>
	</div>
	<div v-if="availableStepTypes.length > 0" class="form-group">
	  <label>Neuen Schritt hinzufügen</label>
	  <select class="form-control" v-model="newStepType" @change="addStep()">
	    <option disabled value="">Bitte wählen</option>
	    <option v-for="(value) in availableStepTypes" :value="value">
	      {{ stepName(value) }}
	    </option>
	  </select>
	</div>
      </div>
    </div>
  </div>

  <div v-if="!editConfig">

    <div v-if="!editMode" class="case-timer bg-light border float-right p-1 rounded-pill" style="margin-top: 20px;">
      <strong>{{ timerMinSec() }}</strong>
      <button class="btn btn-success btn-sm rounded-circle" @click="timerPause()">
	<i v-if="timerRun" class="fa fa-pause" />
	<i v-else class="fa fa-play" />
      </button>
      <button class="btn btn-success btn-sm rounded-circle" @click="timerReset()">
	<i class="fa fa-undo" />
      </button>
    </div>

    <h2>{{ currentCase.name }} (Niveau: {{ difficulties[currentCase.difficulty] }})</h2>

    <div class="clearfix mb-4"></div>

    <div v-if="currentStep.step_type == 'read'">
      <StepRead :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
    </div>

    <div v-if="currentStep.step_type == 'mark_sections'">
      <StepSections :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
    </div>

    <div v-if="currentStep.step_type == 'penalties'">
      <StepPenalties :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
    </div>

    <div v-if="currentStep.step_type == 'problem_areas'">
      <StepProblems :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
    </div>

    <div v-if="currentStep.step_type == 'weights'">
      <StepWeights :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
    </div>

    <div v-if="currentStep.step_type == 'gap_text'">
      <StepGap :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
    </div>

    <div v-if="currentStep.step_type == 'free_text'">
      <StepFreeText :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
    </div>
  </div>

  <hr/>
  <p>{{ currentStep }}</p>
  <hr/>
  <p>{{ currentCase }}</p>

</div>
<div v-else>
  <h3>Lade Fall…</h3>
</div>
</template>

<script>
import axios from "axios";
import { VueEditor, Quill } from "vue2-editor";
import { SlickList, SlickItem } from 'vue-slicksort';

import StepRead from "./StepRead.vue";
import StepSections from "./StepSections.vue";
import StepPenalties from "./StepPenalties.vue";
import StepProblems from "./StepProblems.vue";
import StepWeights from "./StepWeights.vue";
import StepGap from "./StepGap.vue";
import StepFreeText from "./StepFreeText.vue";

let Inline = Quill.import('blots/inline');

class MarkerBlock1 extends Inline {
  static create(value) {
    let node = super.create();
    node.setAttribute('class', 'section-marker-1');
    return node;
  }
  static formats(node) { return true; }
}
MarkerBlock1.blotName = 'section-marker-1';
MarkerBlock1.tagName = 'span';
Quill.register(MarkerBlock1);

class MarkerBlock2 extends Inline {
  static create(value) {
    let node = super.create();
    node.setAttribute('class', 'section-marker-2');
    return node;
  }
  static formats(node) { return true; }
}
MarkerBlock2.blotName = 'section-marker-2';
MarkerBlock2.tagName = 'span';
Quill.register(MarkerBlock2);

class MarkerBlock3 extends Inline {
  static create(value) {
    let node = super.create();
    node.setAttribute('class', 'section-marker-3');
    return node;
  }
  static formats(node) { return true; }
}
MarkerBlock3.blotName = 'section-marker-3';
MarkerBlock3.tagName = 'span';
Quill.register(MarkerBlock3);

class MarkerBlock4 extends Inline {
  static create(value) {
    let node = super.create();
    node.setAttribute('class', 'section-marker-4');
    return node;
  }
  static formats(node) { return true; }
}
MarkerBlock4.blotName = 'section-marker-4';
MarkerBlock4.tagName = 'span';
Quill.register(MarkerBlock4);

class MarkerBlock5 extends Inline {
  static create(value) {
    let node = super.create();
    node.setAttribute('class', 'section-marker-5');
    return node;
  }
  static formats(node) { return true; }
}
MarkerBlock5.blotName = 'section-marker-5';
MarkerBlock5.tagName = 'span';
Quill.register(MarkerBlock5);

const axios_config = {
  headers: {
    'X-CSRFToken': csrf_token,
  },
  withCredentials: true,
}

export default {
  name: "CurrentCase",
  components: {
    SlickList,
    SlickItem,
    VueEditor,
    StepRead,
    StepSections,
    StepPenalties,
    StepProblems,
    StepWeights,
    StepGap,
    StepFreeText,
  },
  props: {
    caseId: {
      type: Number,
    },
    editMode: {
      type: Boolean,
    },
  },
  data() {
    return {
      dataReady: false,
      currentStepNo: 1,
      currentCase: null,
      timerStart: null,
      timerRun: true,
      timerCurrent: null,
      timerPauseStart: null,
      factsToolbar: [
        ["bold", "italic"],
        [{ list: "ordered" }, { list: "bullet" }],
	["section-marker-1", "section-marker-2", "section-marker-3", "section-marker-4", "section-marker-5"],
	['clean'],
      ],
      stepTypes: {
	read: "Lesen",
	mark_sections: "Einteilen",
	gap_text: "Lückentext",
	free_text: "Freitext",
	penalties: "Strafbarkeit",
	problem_areas: "Probleme",
	weights: "Gewichtung",
      },
      difficulties: {
	shortcase: "Kurzfälle",
	beginner: "Anfänger*innen",
	advanced: "Fortgeschrittene",
      },
      newStepType: "",
      editConfig: false,
    }
  },
  async mounted() {
    if (this.caseId) {
      await this.getCase();
    } else {
      this.setEditConfig();
      this.currentCase = {
	facts: "<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p><p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>",
	name: "Neues Falltraining",
	difficulty: "beginner",
	steps: [{ step_type: "read", config: null }]
      };
    }
    this.currentCase.userFacts = this.currentCase.facts
    this.dataReady = true;

    this.timerStart = Date.now();
    setInterval(() => {
      if (this.timerRun) {
	this.timerCurrent = Date.now() - this.timerStart;
      }
    }, 250);
  },
  computed: {
    currentStep() {
      return this.currentCase.steps[this.currentStepNo - 1];
    },
    availableStepTypes() {
      let selected = this.currentCase.steps.map(x => x.step_type);
      console.log(this.stepTypes);
      return Object.keys(this.stepTypes).filter(x => !selected.includes(x));
    },
  },
  methods: {
    async getCase() {
      await axios
	.get("/falltraining/api/case/" + this.caseId)
	.then((response) => {
	  this.currentCase = response.data;
	  this.currentCase.steps = JSON.parse(this.currentCase.steps);
	});
    },
    setStep(num) {
      this.editConfig = false;
      this.currentStepNo = num;
    },
    stepName(id) {
      return this.stepTypes[id];
    },
    timerPause() {
      if (this.timerRun)
	this.timerPauseStart = Date.now()
      else
	this.timerStart += Date.now() - this.timerPauseStart
      this.timerRun = !this.timerRun;
    },
    timerReset() {
      this.timerCurrent = 0;
      this.timerStart = Date.now();
      this.timerRun = true;
    },
    nextStep() {
      if (this.currentStepNo == this.steps()) return;

      this.currentStepNo += 1;
    },
    timerMinSec() {
      var total = Math.round(this.timerCurrent / 1000);
      var minutes = Math.floor(total / 60)
      var seconds = total % 60
      return minutes + ":" + ("0" + seconds).slice(-2)
    },
    prevStep() {
      if (this.currentStepNo == 1) return;

      this.currentStepNo -= 1;
    },
    steps() {
      return this.currentCase.steps.length;
    },
    setEditConfig() {
      this.editConfig = true;
    },
    editModeOn() {
      this.editMode = true;
    },
    editModeOff() {
      this.currentCase.userFacts = this.currentCase.facts
      this.editMode = false;
      this.editConfig = false;
    },
    addStep() {
      if (typeof this.newStepType == "undefined")
	return;

      this.currentCase.steps.push({ step_type: this.newStepType, config: null })
    },
    delStep(index) {
      this.currentCase.steps.splice(index, 1);
    },
    createCase() {
      axios
	.post(
	  "/falltraining/api/case",
	  {
	    steps: JSON.stringify(this.currentCase.steps),
	    facts: this.currentCase.facts,
	    name:  this.currentCase.name,
	    user:  1, // FIXME
	    difficulty: this.currentCase.difficulty,
	  }
	  , axios_config)
	.then(response => {
	  var newId = response.data.id;
	  //window.location = "/falltraining/show/" + newId + "/";
	})
	.catch(error => {
	  console.log(error);
	  if (error.response.status == 400)
	    this.errors = error.response.data;
	})
    },
    saveCase() {
      axios
	.put(
	  "/falltraining/api/case/" + this.currentCase.id,
	  {
	    steps: JSON.stringify(this.currentCase.steps),
	    facts: this.currentCase.facts,
	    name:  this.currentCase.name,
	    user:  this.currentCase.user, // FIXME
	    difficulty: this.currentCase.difficulty,
	  }
	  , axios_config)
	.catch(error => {
	  console.log(error);
	  if (error.response.status == 400)
	    this.errors = error.response.data;
	})
    }
  },
};
// https://learnvue.co/tutorials/vue-drag-and-drop
// https://learnvue.co/tutorials/computed-properties-guide
// https://www.npmjs.com/package/vue-text-selection
// https://stackoverflow.com/questions/14208054/change-the-color-of-text-on-selection
// https://stackoverflow.com/questions/17288964/how-to-change-color-of-the-selected-text-dynamically-on-click-of-button
</script>

<style lang="scss">
  @import './styles.scss';
</style>
