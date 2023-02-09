<template>
<div v-if="editMode" type="read" :key="componentKey">
  Dieser Schritt muss nicht konfiguriert werden.
</div>
<step-template v-else type="read" :key="componentKey">
  <template #left>
    <div class="hide-sections mark-area" :class="markColorStyle">
      <div id="mark-area-content" v-html="currentCase.userFacts" @mouseup="markUp()"></div>
    </div>
  </template>
  <template #right>
    <p>
      Lese den Sachverhalt.
    </p>
    <p>
      Du kannst Wörter im Sachverhalt in unterschiedlichen Farben markieren. Diese werden in den nachfolgenden Schritten angezeigt.
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
    <p class="mt-2 mb-2 d-lg-none">
      <em>Hinweis für mobile Geräte: Markiere zunächst den Text und klicke anschließend auf einen Stift.</em>
    </p>
  </template>
  <template #buttons-right>
    <button class="btn btn-primary" @click="nextStep()">nächster Schritt »</button>
  </template>
</step-template>
</template>

<script>
import StepTemplate from "./StepTemplate.vue";

export default {
  name: "StepRead",
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
  methods: {
    nextStep() {
      this.$parent.nextStep();
    },
    setColor(name) {
      this.markColor = name;
      this.markUp();
    },
    markReset() {
      this.currentCase.userFacts = this.currentCase.facts;
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
	document.execCommand("removeFormat");
	if (this.markColor != "marker-erase")
	  document.execCommand("BackColor", false, "black");
	document.designMode = "off";
	sel.removeAllRanges();
	let html = document.getElementById("mark-area-content").innerHTML;
	html = html.replace(/style="background-color: black;"/g, "class=\"user-" + this.markColor + "\"")
	this.currentCase.userFacts = html;
	this.componentKey += 1;
      }
    },
  },
}
</script>
