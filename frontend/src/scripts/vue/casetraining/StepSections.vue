<template>
<step-template type="sections" :key="componentKey">
  <template #left>

    <div class="mark-area" :class="markColorStyle">
      <div v-if="myStep != 2" class="markers">
	<span class="btn-marker btn-marker-1" :class="markColor == 'marker-1' ?  'border' : ''" @mousedown="setColor('marker-1')">
	  <img src="/assets/images/marker/textmarker-1.png">
	</span>
	<span class="btn-marker btn-marker-2" :class="markColor == 'marker-2' ?  'border' : ''" @mousedown="setColor('marker-2')">
	  <img src="/assets/images/marker/textmarker-2.png">
	</span>
	<span class="btn-marker btn-marker-3" :class="markColor == 'marker-3' ?  'border' : ''" @mousedown="setColor('marker-3')">
	  <img src="/assets/images/marker/textmarker-3.png">
	</span>
	<span class="btn-marker btn-marker-4" :class="markColor == 'marker-4' ?  'border' : ''" @mousedown="setColor('marker-4')">
	  <img src="/assets/images/marker/textmarker-4.png">
	</span>
	<span class="btn-marker btn-marker-5" :class="markColor == 'marker-5' ?  'border' : ''" @mousedown="setColor('marker-5')">
	  <img src="/assets/images/marker/textmarker-5.png">
	</span>
	<span class="btn-marker btn-marker-erase" :class="markColor == 'marker-erase' ?  'border' : ''" @mousedown="setColor('marker-erase')">
	  <img src="/assets/images/marker/eraser.png">
	</span>
      </div>
      <div v-if="editMode" style="position: relative">
	<div id="mark-area-content" v-html="currentCase.facts" @mouseup="markUp()"></div>
      </div>
      <div v-else class="hide-sections">
	<div v-if="myStep == 2">
	  <strong>Deine Einteilung</strong>
	</div>
	<div style="position: relative">
	  <div id="user-mark-area-content-outer">
	    <div id="user-mark-area-content" v-html="currentCase.userFacts"></div>
	  </div>
	  <div id="mark-area-content" v-html="currentStep.answers[0]" @mouseup="markUp()"></div>
	</div>
      </div>
    </div>

  </template>
  <template #right>
    <div v-if="myStep == 1">
      <div v-if="editMode">
	<div class="mb-3">
	  <label>Einleitungstext</label>
	  <div class="small text-danger" v-if="$parent.showDiff && $parent.diffIntroToParent()">
	    <strong>Vorherige Version</strong>
	    <div>{{ $parent.diffIntroToParent() }}</div>
	  </div>
	  <textarea class="form-control" v-model="currentStep.intro" />
	</div>
	<p>
	  Markiere die unterschiedlichen Sachverhaltsabschnitte:
	</p>
      </div>
      <div v-else>
	<p>{{ currentStep.intro }}</p>
      </div>
      <p class="mt-2 mb-2 d-lg-none">
	<em>Hinweis für mobile Geräte: Markiere zunächst den Text und klicke anschließend auf einen Stift.</em>
      </p>
      <div v-if="editMode">
	<div v-if="$parent.showDiff && $parent.diffFactsToParent" class="mt-4">
	  <strong>Vorherige Einteilung</strong>
	  <div v-html="$parent.parentCase.facts"></div>
	</div>
      </div>
    </div>
    <div v-if="myStep == 2">
      <strong>Lösung</strong>
      <div class="show-parts" v-html="currentCase.facts"></div>
    </div>
  </template>
  <template #buttons-right v-if="!editMode && myStep == 1">
    <button class="btn btn-primary" @click="nextStep()">zur Auswertung »</button>
  </template>
  <template #buttons v-if="!editMode && myStep == 2">
    <button class="btn btn-primary" @click="nextStep()">nächster Schritt »</button>
  </template>
  </div>
</step-template>
</template>

<script>
import StepTemplate from "./StepTemplate.vue";
import { nextTick } from "vue";

export default {
  name: "StepSections",
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
      markColor: null,
      colors: {
	"marker-1": "rgb(1,255,255)",
	"marker-2": "rgb(2,255,255)",
	"marker-3": "rgb(3,255,255)",
	"marker-4": "rgb(4,255,255)",
	"marker-5": "rgb(5,255,255)",
      },
      userColors: {
	"marker-1": "rgb(201,255,255)",
	"marker-2": "rgb(202,255,255)",
	"marker-3": "rgb(203,255,255)",
	"marker-4": "rgb(204,255,255)",
	"marker-5": "rgb(205,255,255)",
      },
    }
  },
  computed: {
    markColorStyle() {
      return "mark-" + this.markColor;
    },
    editMode() {
      return this.$parent.editMode;
    },
  },
  beforeMount() {
    if (typeof this.currentStep.answers === "undefined")
      this.currentStep.answers = [this.currentCase.facts];

    if (!this.currentStep.config)
      this.currentStep.config = [];

    if (!this.currentStep.intro)
      this.currentStep.intro = "Markiere die Sachverhaltsabschnitte in unterschiedlichen Farben.";
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
    setColor(name) {
      this.markColor = name;
      this.markUp();
    },
    markReset() {
      this.currentStep.answers[0] = this.currentCase.facts;
      // we need this, so text gets refreshed
      this.componentKey += 1;
    },
    async markUp() {
      if (!this.markColor)
	return;

      var sel = window.getSelection();
      if (sel.type !== "Range" || !sel.getRangeAt)
	return;

      var range = sel.getRangeAt(0);
      document.designMode = "on";
      sel.removeAllRanges();
      sel.addRange(range);
      document.execCommand("removeFormat");
      if (this.markColor != "marker-erase") {
	let colors = this.editMode ? this.colors : this.userColors;
	document.execCommand("BackColor", false, colors[this.markColor]);
      }
      document.designMode = "off";
      sel.removeAllRanges();
      let html = document.getElementById("mark-area-content").innerHTML;
      if (this.editMode) {
	this.currentCase.facts = html;
      } else {
	this.currentStep.answers[0] = html;
      }
      this.componentKey += 1;
      await nextTick();
    },
  },
}
</script>
<style lang="scss">
  @import './styles/step-sections.scss';
</style>
<style lang="scss" scoped>
  @import './styles/markers.scss';
</style>
