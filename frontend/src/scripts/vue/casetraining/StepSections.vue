<template>
<step-template type="sections" :key="componentKey">
  <template #left>
    <div v-if="editMode" class="mark-area" :class="markColorStyle">
      <div style="position: relative">
	<div id="mark-area-content" v-html="currentCase.facts" @mouseup="markUp()"></div>
      </div>
    </div>
    <div v-else class="hide-sections mark-area" :class="markColorStyle">
      <div style="position: relative">
	<div style="position: absolute; top: 0; left: 0; color: transparent; pointer-events: none;">
	  <div id="user-mark-area-content" v-html="currentCase.userFacts"></div>
	</div>
	<div id="mark-area-content" v-html="currentStep.answers[0]" @mouseup="markUp()"></div>
      </div>
    </div>
  </template>
  <template #right>
    <div v-if="myStep == 1">
      <p>
	Markieren Sie die Sachverhaltsabschnitte in unterschiedlichen Farben.
      </p>
      <span class="btn-marker btn-marker-1" :class="markColor == 'marker-1' ?  'border' : ''" @click="setColor('marker-1')">
	<img src="/assets/images/marker/textmarker-1.png">
      </span>
      <span class="btn-marker btn-marker-2" :class="markColor == 'marker-2' ?  'border' : ''" @click="setColor('marker-2')">
	<img src="/assets/images/marker/textmarker-2.png">
      </span>
      <span class="btn-marker btn-marker-3" :class="markColor == 'marker-3' ?  'border' : ''" @click="setColor('marker-3')">
	<img src="/assets/images/marker/textmarker-3.png">
      </span>
      <span class="btn-marker btn-marker-4" :class="markColor == 'marker-4' ?  'border' : ''" @click="setColor('marker-4')">
	<img src="/assets/images/marker/textmarker-4.png">
      </span>
      <span class="btn-marker btn-marker-5" :class="markColor == 'marker-5' ?  'border' : ''" @click="setColor('marker-5')">
	<img src="/assets/images/marker/textmarker-5.png">
      </span>
      <span class="btn-marker btn-marker-erase" :class="markColor == 'marker-erase' ?  'border' : ''" @click="setColor('marker-erase')">
	<img src="/assets/images/marker/eraser.png">
      </span>
    </div>
    <div v-if="myStep == 2">
      <div class="show-parts" v-html="currentCase.facts"></div>
    </div>
  </template>
  <template #buttons-right>
    <div v-if="!editMode">
      <button v-if="myStep == 1" class="btn btn-primary" @click="nextStep()">zur Auswertung »</button>
      <button v-if="myStep == 2" class="btn btn-primary" @click="nextStep()">nächster Schritt »</button>
    </div>
  </template>
</step-template>
</template>

<script>
import StepTemplate from "./StepTemplate.vue";

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
    if (typeof this.currentStep.answers !== "undefined")
      return;

    let html = this.currentCase.facts;
    this.currentStep.answers = [html];
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
    },
    markReset() {
      this.currentStep.answers[0] = this.currentCase.facts;
      // we need this, so text gets refreshed
      this.componentKey += 1;
    },
    markUp() {
      if (!this.markColor) return;

      var sel = window.getSelection();

      if (sel.type == "Range" && sel.getRangeAt) {
	var range = sel.getRangeAt(0);
	document.designMode = "on";
	sel.removeAllRanges();
	sel.addRange(range);
	if (this.markColor == "marker-erase")
	  document.execCommand("removeFormat");
	else
	  document.execCommand("BackColor", false, "black");
	document.designMode = "off";
	sel.removeAllRanges();
	let html = document.getElementById("mark-area-content").innerHTML;
	if (this.editMode) {
	  html = html.replace(/style="background-color: black;"/g, "class=\"section-" + this.markColor + "\"")
	  this.currentCase.facts = html;
	} else {
	  html = html.replace(/style="background-color: black;"/g, "class=\"user-section-" + this.markColor + "\"")
	  this.currentStep.answers[0] = html;
	}
	this.componentKey += 1;
      }
    },
  },
}
</script>
<style lang="scss">
  @import './styles/step-sections.scss';
</style>
