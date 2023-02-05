<template>
<div v-if="!dataReady">
  <h4><i class="fa fa-sync fa-spin text-info mr-2"></i> Lade Fall…</h4>
</div>
<div v-else class="casetraining" :key="componentKey">

  <div v-if="debugMode">
    admin: {{ isAdmin }} |
    user id: {{ userId }} |
    user email: {{ userEmail }} |
    caseId: {{ caseId }} |
    case.id: {{ currentCase.id }} |
    case.user: {{ currentCase.user }} |
    case.approved: {{ currentCase.approved }} |
    case.parent: {{ currentCase.parent }} |
    newCase: {{ newCase }} |
    submission: {{ submissionId }} |
  </div>

  <div v-if="editMode" class="alert alert-primary">
    <button class="btn btn-primary float-right ml-2" @click="editModeOff">Bearbeitung beenden</button>
    <div v-if="isAdmin">
      <div v-if="newCase">
	<button class="btn btn-success float-right ml-2" @click="saveCase">Erstellen</button>
	Du erstellst einen neuen Fall.
      </div>
      <div v-else>
	<button class="btn btn-success float-right ml-2" @click="saveCase">Speichern</button>
	Du bearbeitest einen bestehenden Fall.
      </div>
    </div>
    <div v-else>
      <button v-if="currentCase.id" class="btn btn-info float-right ml-2" @click="doSubmit">Einreichen</button>
      <div v-if="newCase">
	<button class="btn btn-success float-right ml-2" @click="saveCase">Erstellen</button>
	Du erstellst einen neuen Fall. Wenn du fertig bist, kannst du den Fall speichern und anschließend einreichen. Nach einer Prüfung werden wir Deinen Fall freigeben.
      </div>
      <div v-else>
	<button class="btn btn-success float-right ml-2" @click="saveCase">Speichern</button>
	Du bearbeitest einen bestehenden Fall. Wenn du fertig bist, kannst du den Fall speichern und anschließend einreichen. Nach einer Prüfung werden wir Deine Überarbeitung freigeben.
      </div>
    </div>
    <div class="clearfix"></div>
  </div>

  <div v-if="caseErrors" class="alert alert-danger">
    <strong>Bitte korrigiere folgende Fehler:</strong><br/>
    <div v-for="(errors, name) in caseErrors">
      {{ translate(name) }}: {{ errors.join(" ") }}
    </div>
  </div>

  <div v-if="apiErrors" class="alert alert-danger">
    <strong>Es ist ein Fehler aufgetreten:</strong><br/>
    {{ apiErrors }}
  </div>

  <div v-if="userMessage" class="alert alert-info">
    {{ userMessage }}
  </div>

  <div class="bg-dark px-2 text-uppercase">
    <span
       class="text-white btn"
       :class="editConfig ? 'text-success' : 'text-light'"
       v-if="editMode"
       @click="editModeOn">
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

  <div v-if="editConfig" class="mt-4">
    <div v-if="isAdmin" class="row mb-4">
      <div class="col-sm-6">
	<div class="form-check">
	  <input class="form-check-input" type="checkbox" value="" id="case-approved" v-model="currentCase.approved">
	  <label class="form-check-label" for="case-approved">
	    Freigegeben
	  </label>
	</div>
      </div>
      <div class="col-sm-6" v-if="showDiff">
	<a :href="parentUrl()" target="_blank">Original Falltraining öffnen</a>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
	<div class="form-group">
	  <label>Titel <sup class="text-danger">*</sup></label>

	  <div v-if="showDiff && diffNameToParent" class="small text-danger">
	    <strong>Vorheriger Name</strong>
	    <div v-html="diffNameToParent"></div>
	  </div>

	  <input class="form-control" v-model="currentCase.name" placeholder="Titel des Falltrainings" required>
	</div>
      </div>
      <div class="col-sm-6">
	<div class="form-group">
	  <label>Niveau <sup class="text-danger">*</sup></label>
	  <select class="form-control" v-model="currentCase.difficulty" required>
	    <option disabled value="">Bitte wählen</option>
	    <option v-for="(name, value) in difficulties" :value="value">
	      {{ name }}
	    </option>
	  </select>
	</div>
	<div class="small text-danger" v-if="showDiff && diffDifficultyToParent">
	  <strong>Vorherige Version</strong>
	  <div v-html="diffDifficultyToParent"></div>
	</div>
      </div>
    </div>

    <div class="row">
      <div class="col-sm-12">
	<label>Falltrainingsschritte</label>
      </div>
    </div>

    <div class="row">
      <div class="col-sm-6">
	<div class="form-group">
          <div v-model="currentCase.steps">
            <div v-for="(step, index) in currentCase.steps" :key="step.step_type" :index="index">
              <div class="border my-1 px-2 py-1 bg-white">
		<span style="pointer-events: none; user-select: none;">
		  <span class="text-danger" v-if="showDiff && diffStepAdded(step.step_type)">Neu!</span>
		  <span class="text-danger" v-else-if="showDiff && diffStepToCurrent(step.step_type)">Geändert!</span>
                  {{ stepName(step.step_type) }}
		</span>
		<button v-if="stepOptional(step.step_type)" @click="delStep(index)" class="btn btn-sm text-danger float-right"><i style="pointer-events: none;" class="fa fa-trash"></i></button>
              </div>
            </div>
          </div>
	</div>
      </div>
      <div class="col-sm-6">
	<div v-if="availableStepTypes.length > 0" class="form-group">
          <label>Neuen Schritt hinzufügen</label>
          <select class="form-control" v-model="newStepType" @change="addStep()">
            <option disabled value="">Bitte wählen</option>
            <option v-for="(value) in availableStepTypes" :value="value">
              {{ stepName(value) }}
            </option>
          </select>
	</div>
	<div class="small" v-if="showDiff">
	  <label class="text-danger">Vorherige Version</label>
	  <div v-for="(step, index) in parentCase.steps">
	    <div class="border my-1 px-2 py-1 bg-white">
	      <span class="text-danger" v-if="diffStepDeleted(step.step_type)">Gelöscht!</span>
	      {{ stepName(step.step_type) }}
	    </div>
	  </div>
	</div>
      </div>
    </div>

    <div class="row">
      <div class="col-sm-6">
	<div class="form-group">
	  <label>Sachverhalt <sup class="text-danger">*</sup></label>
	  <vue-editor id="facts-editor" v-model="currentCase.facts" :editorToolbar="factsToolbar"></vue-editor>
	</div>
      </div>
      <div class="col-sm-6">
	<div v-if="showDiff && diffFactsToParent"><label>Änderungen</label>
	  <div class="hide-sections" v-html="diffFactsToParent"></div>
	</div>
      </div>
    </div>
    <sup class="text-danger">*</sup> Pflichtfelder
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

    <h2>{{ currentCase.name }}</h2>
    <strong>Niveau: {{ difficulties[currentCase.difficulty] }}</strong>
    <div class="clearfix mb-4"></div>

    <div v-if="currentStep.step_type == 'read'">
      <StepRead :currentCase="currentCase" :currentStep="currentStep" :currentStepNo="currentStepNo" />
    </div>

    <StepSolution v-if="currentStep.step_type == 'solution'" />

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

  <div v-if="!editMode && caseEditable" style="min-height: 200px; margin-top: 50px;">
    <div class="illustration-container">
      <div class="contribute-small" style="margin-top: -30px"></div>
    </div>
    <div class="contribution-area">
      <p style="margin-bottom: 0px !important;">
	<a href="#">
          <span @click.stop="editModeOn" class="underlined green hover">Fall bearbeiten</span>
	  <i class="bi bi-arrow-right"></i>
	  <br/>
	</a>
      </p>
    </div>
  </div>

  <div v-if="debugMode">
    <hr/>
    <p>{{ currentStep }}</p>
    <hr/>
    <p>{{ currentCase }}</p>
  </div>

</div>
</template>

<script>
import axios from "axios";
import { VueEditor, Quill } from "vue2-editor";
import { diffJson, diffChars } from "diff";

import StepRead from "./StepRead.vue";
import StepSections from "./StepSections.vue";
import StepPenalties from "./StepPenalties.vue";
import StepProblems from "./StepProblems.vue";
import StepWeights from "./StepWeights.vue";
import StepGap from "./StepGap.vue";
import StepFreeText from "./StepFreeText.vue";
import StepSolution from "./StepSolution.vue";

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
    VueEditor,
    StepRead,
    StepSections,
    StepPenalties,
    StepProblems,
    StepWeights,
    StepGap,
    StepFreeText,
    StepSolution,
  },
  props: {
    newCase: {
      type: Boolean,
    },
    caseId: {
      type: Number,
    },
    submissionId: {
      type: Number,
    },
    userId: {
      type: Number,
    },
    userEmail: {
      type: String,
    },
    isAdmin: {
      type: Boolean,
    },
  },
  data() {
    return {
      debugMode: false,
      editMode: false,
      dataReady: false,
      wikiReady: false,
      wikiArticles: [],
      wikiSolutions: [],
      currentStepNo: 1,
      currentCase: null,
      parentCase: null,
      timerStart: null,
      timerRun: true,
      timerCurrent: null,
      timerPauseStart: null,
      apiErrors: null,
      caseErrors: null,
      userMessage: null,
      factsToolbar: [
        ["bold", "italic"],
        [{ list: "ordered" }, { list: "bullet" }],
      ],
      stepTypes: {
	read: "Lesen",
	mark_sections: "Einteilen",
	penalties: "Strafbarkeit",
	problem_areas: "Probleme",
	weights: "Gewichtung",
	gap_text: "Lückentext",
	free_text: "Freitext",
	solution: "Lösungsskizze",
      },
      difficulties: {
	shortcase: "Kurzfälle",
	beginner: "Anfänger*innen",
	advanced: "Fortgeschrittene",
      },
      newStepType: "",
      editConfig: false,
      fields: {
	name: "Titel",
	difficulty: "Niveau",
      },
      componentKey: 0,
    }
  },
  async mounted() {
    if (this.caseId) {
      await this.getCase();
      if (this.currentCase.parent)
	await this.getParentCase();

    } else {
      this.editModeOn();
      this.currentCase = {
	facts: "<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p><p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>",
	name: "",
	difficulty: "",
	steps: [{ step_type: "read", config: null },
		{ step_type: "solution", config: null }]
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

    await this.getWikiArticles();
    this.wikiReady = true;
  },
  computed: {
    sectionMarkers() {
      var parts = this.currentCase.facts.split(/class=\"/);
      var classes = [];
      for (var i = 0; i < parts.length-1; i++) {
	classes[i] = parts[i+1].split(/\"/)[0].trim();
      }
      // return unique classes
      return classes.filter((v, i, a) => a.indexOf(v) === i);
    },
    diffFactsToParent() {
      return this.diffText(this.parentCase.facts, this.currentCase.facts);
    },
    diffNameToParent() {
      if (this.parentCase.name == this.currentCase.name)
	return false;

      return this.parentCase.name;
    },
    diffDifficultyToParent() {
      if (this.difficulties[this.parentCase.difficulty] ==
	  this.difficulties[this.currentCase.difficulty])
	return false;

      return this.difficulties[this.parentCase.difficulty];
    },
    currentStep() {
      return this.currentCase.steps[this.currentStepNo - 1];
    },
    parentStep() {
      return this.parentCase.steps.filter(x => x.step_type == this.currentStep.step_type)[0];
    },
    availableStepTypes() {
      let selected = this.currentCase.steps.map(x => x.step_type);
      return Object.keys(this.stepTypes).filter(x => !selected.includes(x));
    },
    caseEditable() {
      if (this.isAdmin)
	return true;

      return !this.currentCase.submission || this.currentCase.approved;
    },
    showDiff() {
      return this.isAdmin && this.currentCase.submission && !this.currentCase.approved && this.currentCase.parent;
    },
  },
  methods: {
    parentUrl() {
      return "/falltraining/show/" + this.currentCase.parent + "/";
    },
    diffStepDeleted(step_type) {
      var step = this.currentCase.steps.filter(x => x.step_type == step_type)[0];
      return !step;
    },
    diffStepAdded(step_type) {
      var step = this.parentCase.steps.filter(x => x.step_type == step_type)[0];
      return !step;
    },
    diffStepToCurrent(step_type) {
      var current = this.currentCase.steps.filter(x => x.step_type == step_type);
      var past = this.parentCase.steps.filter(x => x.step_type == step_type);
      return JSON.stringify(this.mapStepsToApi(current)) !==
	JSON.stringify(this.mapStepsToApi(past));
    },
    diffConfigToParentDeleted(index) {
      if (typeof index !== "undefined") {
	if (this.parentStep.config[index].length > this.currentStep.config[index].length)
	  return this.parentStep.config[index].length - this.currentStep.config[index].length;

	return false;
      }

      if (this.parentStep.config.length > this.currentStep.config.length)
	return this.parentStep.config.length - this.currentStep.config.length;

      return false
    },
    diffConfigToParentNew(index, field, index2) {
      if (!this.parentStep.config[index])
	return true;

      if (!this.parentStep.config[index][field])
	return true;

      if (typeof index2 !== "undefined") {
	if (!this.parentStep.config[index][field][index2])
	  return true;
      }

      return false;
    },
    diffIntroToParent() {
      if (this.parentStep.intro !== this.currentStep.intro)
	return this.parentStep.intro;

      return false;
    },
    diffConfigToParent(index, field, index2, index3) {
      if (this.diffConfigToParentNew(index, field, index2))
	return false;

      if (typeof index2 === "undefined") {
	if (this.parentStep.config[index][field] !=
	    this.currentStep.config[index][field])
	  return this.parentStep.config[index][field];
      } else {
	if (typeof index3 === "undefined") {
	  if (this.parentStep.config[index][field][index2] !=
	      this.currentStep.config[index][field][index2])
	    return this.parentStep.config[index][field][index2];
	} else {
	  if (this.parentStep.config[index][field][index2][index3] !=
	      this.currentStep.config[index][field][index2][index3])
	    return this.parentStep.config[index][field][index2][index3];
	}
      }

      return false;
    },
    diffSimple(a, b) {
      if (a === b)
	return false

      var text = "<span style='font-weight: bold; text-decoration: line-through; color: red'>" + a + "</span><br/>";
      text += "<span style='font-weight: bold; color: green'>" + b + "</span>";
      return text;
    },
    diffText(a, b) {
      if (a === b)
	return false

      const diff = diffChars(a, b);
      var text = "";
      diff.forEach((part) => {
	var color = part.added ? 'green' :
	      part.removed ? 'red' : '';

	var strike =  part.removed ? 'line-through' : 'none';
	if (color !== "")
	  text += "<span style='font-weight: bold; text-decoration: " + strike + "; color: " + color + "'>" + part.value + "</span>";
	else
	  text += "<span>" + part.value + "</span>";
      });
      return text;
    },
    async getCase() {
      await axios
	.get("/falltraining/api/case/" + this.caseId)
	.then((response) => {
	  this.currentCase = response.data;
	  this.currentCase.id = this.caseId;
	  this.currentCase.steps = JSON.parse(this.currentCase.steps);
	  this.updateSubmissionMessage();
	});
    },
    updateSubmissionMessage() {
      if (this.currentCase.submission && !this.currentCase.approved)
	if (this.isAdmin) {
	  this.userMessage = "Dieser Fall ist zur Prüfung eingereicht.";
	} else {
	  this.userMessage = "Deine Änderungen wurden eingereicht. Nach einer Prüfung werden wir die Überarbeitung freigeben.";
	}
    },
    async getParentCase() {
      await axios
	.get("/falltraining/api/case/" + this.currentCase.parent)
	.then(response => {
	  this.parentCase = response.data;
	  this.parentCase.steps = JSON.parse(this.parentCase.steps);
	});
    },
    async getWikiArticles() {
      await axios
        .get("/falltraining/api/wiki_categories")
        .then(response => {
	      this.wikiArticles = response.data.filter(x => !x.url.startsWith("/problemfelder/loesungsskizzen/"));
	      this.wikiSolutions = response.data.filter(x => x.url.startsWith("/problemfelder/loesungsskizzen/"));
	});
    },
    async getSolutionArticles() {
      await axios
        .get("/falltraining/api/wiki_solutions")
        .then((response) => this.wikiSolutions = response.data);
    },
    stepOptional(name) {
      if (name == "read") return false;
      if (name == "solution") return false;
      return true;
    },
    setStep(num) {
      this.editConfig = false;
      this.currentStepNo = num;
    },
    translate(name) {
      return this.fields[name] || name;
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
    editModeOn() {
      if (!this.isAdmin) {
	if (this.currentCase && this.currentCase.approved) {
	  // user is editing an approved case
	  // set id to null, so we create a new case on save
	  this.currentCase.id = null;
	  this.currentCase.parent = this.caseId;
	  this.currentCase.approved = false;
	}
      }

      this.editMode = true;
      this.editConfig = true;
      this.componentKey += 1;
    },
    editModeOff() {
      this.currentCase.userFacts = this.currentCase.facts
      this.editMode = false;
      this.editConfig = false;
      this.componentKey += 1;
    },
    addStep() {
      if (typeof this.newStepType == "undefined")
	return;

      this.currentCase.steps.push({ step_type: this.newStepType, config: null });
      this.sortSteps();
      this.newStepType = "";
    },
    sortSteps() {
      var steps = Object.keys(this.stepTypes);
      this.currentCase.steps.sort((a, b) => {
	if (steps.indexOf(a.step_type) > steps.indexOf(b.step_type)) return 1;
	if (steps.indexOf(a.step_type) < steps.indexOf(b.step_type)) return -1;
	return 0;
      });
    },
    delStep(index) {
      this.currentCase.steps.splice(index, 1);
    },
    wikiUrlToText(url) {
      var titles = [];
      var depth = url.split("/").length - 1;

      for(var i = 3; i < depth; i++) {
	var search_url = url.split("/").slice(0, i).join("/") + "/";
	var article = this.wikiArticles.filter(a => (a.url == search_url))[0]
	if (article)
	  titles.push(article.title);
      }

      return titles.join(" > ");
    },
    mapStepsToApi(steps) {
      // removes user answers
      return steps.map(step => ({
	step_type: step.step_type,
	config: step.config,
	intro: step.intro,
      }))
    },
    apiData() {
      return {
	steps:         JSON.stringify(this.mapStepsToApi(this.currentCase.steps)),
	facts:         this.currentCase.facts,
	name:          this.currentCase.name,
	user:          this.userId, // NULL is anonymous
	parent:        this.currentCase.parent,
	difficulty:    this.currentCase.difficulty,
	approved:      this.currentCase.approved,
	solution_slug: this.currentCase.solution_slug || URLify(this.currentCase.name),
      }
    },
    handleError(error) {
      if (error.response.status == 400) {
	this.caseErrors = error.response.data;
	this.editModeOn();
      } else
	this.apiErrors = error;
    },
    async doSubmit() {
      await axios
	.put("/falltraining/api/case/" + this.currentCase.id + "/submit", this.apiData(), axios_config)
	.then(response => {
	  this.currentCase.submission = response.data.submission;
	  this.userMessage = "Deine Änderungen wurden eingereicht. Nach einer Prüfung werden wir Deine Überarbeitung freigeben.";
	  this.editModeOff();
	})
	.catch(error => this.handleError(error));

      this.componentKey += 1;
    },
    async createCase() {
      await axios
	.post("/falltraining/api/case", this.apiData(), axios_config)
	.then(response => {
	  this.currentCase.id = response.data.id;
	  this.caseId = response.data.id;
	  this.currentCase.user = response.data.user;
	  this.currentCase.solution_slug = response.data.solution_slug;
	})
	.catch(error => this.handleError(error))
    },
    async updateCase() {
      await axios
	.put(
	  "/falltraining/api/case/" + this.currentCase.id, this.apiData(), axios_config)
	.then(response => {
	  this.updateSubmissionMessage();
	})
	.catch(error => this.handleError(error))
    },
    async saveCase() {
      this.apiErrors = null;
      this.caseErrors = null;

      if (this.currentCase.id) {
	await this.updateCase();
      } else {
	await this.createCase();
      }

      this.componentKey += 1;
    },
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
