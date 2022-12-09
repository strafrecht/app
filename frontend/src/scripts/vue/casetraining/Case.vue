<template>
<div v-if="dataReady" class="casetraining">

  <div class="case-timer">
    {{ timerMinSec() }}
    <button class="btn btn-success" @click="timerPause()" v-if="timerRun">Pause</button>
    <button class="btn btn-success" @click="timerPause()" v-if="!timerRun">Resume</button>
    <button class="btn btn-success" @click="timerReset()">Reset</button>
  </div>

  <h1>Step: {{ currentStepNo }} / {{ steps() }}</h1>
  <p>{{ currentStep() }}</p>
  <h2>{{ currentCase.name }} (Niveau: {{ currentCase.difficulty }})</h2>

  <div v-if="currentStep().step_type == 'read'">
    <div class="row">
      <div class="col-sm-6">
	<div v-html="currentCase.facts"></div>
      </div>
      <div class="col-sm-6 border">
	<h4>Step {{ currentStepNo }}</h4>
	<p>
	  Lesen Sie den Sachverhalt.
	</p>
      </div>
    </div>
    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
  </div>

  <div v-if="currentStep().step_type == 'mark_sections'">
    <div class="row">
      <div class="col-sm-6" :class="markColorStyle">
	<div id="mark-area-content" v-html="currentStep().config[0].answer" @mouseup="markUp()"></div>
      </div>
      <div class="col-sm-6 border">
	<h4>Step {{ currentStepNo }}</h4>
	<p>
	  Markieren Sie die Sachverhaltsabschnitte in unterschiedlichen Farben.
	</p>
	<div style="background: red" @click="setMarkColor('red')">xxx</div>
	<div style="background: blue" @click="setMarkColor('blue')">xxx</div>
	<div style="background: yellow" @click="setMarkColor('yellow')">xxx</div>
	<div style="background: green" @click="setMarkColor('green')">xxx</div>
	<div style="background: pink" @click="setMarkColor('pink')">xxx</div>
	<div @click="markReset()">Reset</div>
      </div>
    </div>
    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
  </div>

  <div v-if="currentStep().step_type == 'penalties'">
    <div class="row">
      <div class="col-sm-6">
	{{ currentCase.facts }}
      </div>
      <div class="col-sm-6 border">
	<h4>Step {{ currentStepNo }}</h4>
	<p>
	  Ermitteln Sie die zu prüfenden Strafbarkeiten in der für die Lösungsskizze korrekten Reihenfolge.
	</p>
	<div v-for="(penalty, index) in currentStep().config">
	  <h4>{{ penalty.text }}</h4>
	  <div v-for="(answer, index) in penalty.answers">
	    <input v-model="penalty.answers[index]">
	    <button v-if="penalty.answers.length > 1" class="btn btn-success" @click="penaltyDelAnswer(penalty, index)">-</button>
	  </div>
	  <button class="btn btn-success" @click="penaltyAddAnswer(penalty)">+</button>
	</div>
      </div>
    </div>
    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
  </div>

  <div v-if="currentStep().step_type == 'problem_areas'">
    <div class="row">
      <div class="col-sm-6">
	{{ currentCase.facts }}
      </div>
      <div class="col-sm-6 border">
	<h4>Step {{ currentStepNo }}</h4>
	<p>
	  Ermitteln Sie die Problemfelder des 1. Sachverhaltsabschnitts.
	</p>
	<input v-model="wikiSearch">
	<div v-for="(article, index) in wikiSearchArticles()">
	  <div><small><i>{{ article.path.join(' &gt; ') }}</i></small></div>
	  <div>{{ article.title }}</div>
	  <div><a :href="article.url" target="_blank">zum Wiki</a></div>
	  <hr/>
	</div>
      </div>
    </div>
    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
  </div>

  <div v-if="currentStep().step_type == 'gap_text'">
    <div class="row">
      <div class="col-sm-6">
      </div>
      <div class="col-sm-6 border">
	<h4>Step {{ currentStepNo }}</h4>
	<p>
	  Füllen Sie die Lücken auf der linken Seite mit den rechts vorgegebenen Satzbausteinen.
	</p>
      </div>
    </div>

    <div v-for="(question, index) in currentStep().config">
      <div class="row">
	<div class="col-sm-6">
	  <h4>Frage {{ index + 1 }}</h4>
	  <div>
	    <span v-for="(word, index) in words(question.question)">
	      <span>{{ word }}</span>
	      <span v-if="index !== words(question.question).length - 1">
		<span class="gap-drop" @drop="onDrop($event, question, index)" @dragover.prevent @dragenter.prevent>
		  {{ wordAt(question, index) }}
		</span>
	      </span>
	    </span>
	  </div>
	</div>
	<div class="col-sm-6">
	  <div v-for="(answer, index) in gapTexts(question)" draggable @dragstart="startDrag($event, answer)">
	    <div class="gap-drag">{{ answer }}</div>
	  </div>
	</div>
      </div>
      <hr/>
    </div>

    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
  </div>

  <div v-if="currentStep().step_type == 'free_text'">
    <div class="row">
      <div class="col-sm-6">
	<div v-html="currentCase.facts"></div>
      </div>
      <div class="col-sm-6 border">
	<h4>Step {{ currentStepNo }}</h4>
	<p>
	  Bearbeiten Sie die folgenden Aufgaben.
	</p>
	<div v-for="discussion in currentStep().config">
	  <div v-html="discussion.text"></div>
	  <textarea v-model="discussion.answer" ></textarea>
	</div>
      </div>
    </div>
    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
  </div>

</div>
<div v-else>
  <h3>Lade Fall…</h3>
</div>
</template>

<script>
import axios from "axios";

const axios_config = {
  headers: {
    'X-CSRFToken': csrf_token,
  },
  withCredentials: true,
}

export default {
  name: "CurrentCase",
  props: {
    caseId: {
      type: Number,
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
      markColor: null,
      wikiTree: null,
      wikiArticles: [],
      wikiSearch: "",
    }
  },
  async mounted() {
    await this.getWikiTree();
    await this.getCurrentCase();
    this.currentCase.steps.forEach(element => {
      if (!element.config)
	element.config = [{}];

      element.config.forEach(element => {
	element.answer = "";
	element.answers = [""];
      });

      if (element.step_type == "mark_sections")
	element.config[0].answer = this.currentCase.facts;
    });
    this.dataReady = true;
    this.timerStart = Date.now();
    setInterval(() => {
      if (this.timerRun) {
	this.timerCurrent = Date.now() - this.timerStart;
      }
    }, 250);
  },
  computed: {
    markColorStyle() {
      return "mark-area mark-" + this.markColor;
    },
  },
  methods: {
    async getCurrentCase() {
      await axios
	.get("/falltraining/api/case/" + this.caseId + "/")
	.then((response) => {
	  this.currentCase = response.data;
	});
    },
    async getWikiTree() {
      await axios
        .get("/falltraining/api/wiki_categories")
        .then((response) => this.wikiTree = response.data);

      this.makeWikiEntry(this.wikiTree.children, []);
    },
    makeWikiEntry(articles, path) {
      articles.forEach(article => {
	this.wikiArticles.push({
	  title: article.title,
	  url: article.url,
	  path: path,
	});
	this.makeWikiEntry(article.children, path.concat([article.title]))
      });
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
    currentStep() {
      return this.currentCase.steps[this.currentStepNo - 1];
    },
    wikiSearchArticles() {
      if (this.wikiSearch.length < 3)
	return []

      var re = RegExp(this.wikiSearch, "i");

      return this.wikiArticles.filter(
	article =>
	  (article.title.search(re) >= 0)
      );
    },
    penaltyDelAnswer(penalty, index) {
      penalty.answers.splice(index, 1);
      console.log(index)
      console.log(penalty.answers)
    },
    penaltyAddAnswer(penalty) {
      penalty.answers = penalty.answers.concat([""])
      console.log(penalty.answers)
    },
    gapTexts(question) {
      return question.correct.concat(question.other)
    },
    words(text) {
      return text.split("_");
    },
    wordAt(question, index) {
      if (typeof question.solution === 'undefined' ||
	  !question.solution[index])
	return "__________"

      return question.solution[index];
    },
    onDrop(evt, question, index) {
      const item = evt.dataTransfer.getData('item');
      if (typeof question.solution === 'undefined')
	question.solution = Array(this.words(question.question).length - 1);
      question.solution[index] = item;
    },
    startDrag(evt, item) {
      evt.dataTransfer.dropEffect = 'move'
      evt.dataTransfer.effectAllowed = 'move'
      evt.dataTransfer.setData('item', item)
    },
    setMarkColor(name) {
      this.markColor = name;
    },
    markReset() {
      this.currentStep().config[0].answer = this.currentCase.facts;
    },
    markUp() {
      var sel = window.getSelection();

      if (sel.type == "Range" && sel.getRangeAt) {
	var range = sel.getRangeAt(0);
	console.log(range);
	document.designMode = "on";
	sel.removeAllRanges();
	sel.addRange(range);
	document.execCommand("BackColor", false, this.markColor);
	document.designMode = "off";
	sel.removeAllRanges();
	this.currentStep().config[0].answer = document.getElementById("mark-area-content").innerHTML;
	//var span = document.createElement("span");
        //span.style.cssText = "background: " + this.markColor;
        //range.surroundContents(span);
      }
    },
  }
};
// https://learnvue.co/tutorials/vue-drag-and-drop
// https://learnvue.co/tutorials/computed-properties-guide
// https://www.npmjs.com/package/vue-text-selection
// https://stackoverflow.com/questions/14208054/change-the-color-of-text-on-selection
// https://stackoverflow.com/questions/17288964/how-to-change-color-of-the-selected-text-dynamically-on-click-of-button
</script>

<style lang="scss" scoped>
  @import './styles.scss';
</style>
