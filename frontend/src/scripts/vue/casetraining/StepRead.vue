<template>
<step-template type="read" :key="componentKey">
  <template #left>
    <div :class="markColorStyle">
      <div id="mark-area-content" v-html="currentCase.userFacts" @mouseup="markUp()"></div>
    </div>
  </template>
  <template #right>
    <p>
      Lesen Sie den Sachverhalt.
    </p>
    <p>
      Markieren Sie Wörter in unterschiedlichen Farben.
    </p>
    <span class="btn btn-sm btn-user-marker-1 rounded-circle" :class="markColor == 'user-marker-1' ?  'border' : ''" @click="setColor('user-marker-1')"><i class="fas fa-pencil-alt"></i></span>
    <span class="btn btn-sm btn-user-marker-2 rounded-circle" :class="markColor == 'user-marker-2' ?  'border' : ''" @click="setColor('user-marker-2')"><i class="fas fa-pencil-alt"></i></span>
    <span class="btn btn-sm btn-user-marker-3 rounded-circle" :class="markColor == 'user-marker-3' ?  'border' : ''" @click="setColor('user-marker-3')"><i class="fas fa-pencil-alt"></i></span>
    <span class="btn btn-sm btn-user-marker-4 rounded-circle" :class="markColor == 'user-marker-4' ?  'border' : ''" @click="setColor('user-marker-4')"><i class="fas fa-pencil-alt"></i></span>
    <span class="btn btn-sm btn-user-marker-5 rounded-circle" :class="markColor == 'user-marker-5' ?  'border' : ''" @click="setColor('user-marker-5')"><i class="fas fa-pencil-alt"></i></span>
    <span class="btn btn-sm btn-user-marker-6 rounded-circle" :class="markColor == 'user-marker-6' ?  'border' : ''" @click="setColor('user-marker-6')"><i class="fas fa-pencil-alt"></i></span>
    <button class="btn btn-sm btn-danger" @click="markReset()">Reset</button>
  </template>
  <template #buttons>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
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
      return "user-mark-area mark-" + this.markColor;
    },
  },
  methods: {
    nextStep() {
      this.$parent.nextStep();
    },
    setColor(name) {
      this.markColor = name;
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
	document.execCommand("BackColor", false, "black");
	document.designMode = "off";
	sel.removeAllRanges();
	let html = document.getElementById("mark-area-content").innerHTML;
	html = html.replace(/style="background-color: black;"/g, "class=\"" + this.markColor + "\"")
	this.currentCase.userFacts = html;
	this.componentKey += 1;
      }
    },
  },
}
</script>
