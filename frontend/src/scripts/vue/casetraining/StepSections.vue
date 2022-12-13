<template>
<step-template type="sections" :key="componentKey">
  <template #left>
    <div :class="markColorStyle">
      <div id="mark-area-content" v-html="currentStep.answers[0]" @mouseup="markUp()"></div>
    </div>
  </template>
  <template #right>
    <p>
      Markieren Sie die Sachverhaltsabschnitte in unterschiedlichen Farben.
    </p>
    <div style="background: red" @click="setColor('red')">xxx</div>
    <div style="background: blue" @click="setColor('blue')">xxx</div>
    <div style="background: yellow" @click="setColor('yellow')">xxx</div>
    <div style="background: green" @click="setColor('green')">xxx</div>
    <div style="background: pink" @click="setColor('pink')">xxx</div>
    <button class="btn btn-success" @click="markReset()">Reset</button>
  </template>
  <template #buttons>
    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
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
      markColor: null,
    }
  },
  computed: {
    markColorStyle() {
      return "mark-area mark-" + this.markColor;
    },
  },
  methods: {
    prevStep() {
      this.$parent.prevStep();
    },
    nextStep() {
      this.$parent.nextStep();
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
	document.execCommand("BackColor", false, this.markColor);
	document.designMode = "off";
	sel.removeAllRanges();
	this.currentStep.answers[0] = document.getElementById("mark-area-content").innerHTML;
	this.componentKey += 1;
      }
    },
  },
}
</script>
<style lang="scss">
  @import './styles/step-sections.scss';
</style>
