<template>
<div v-if="editMode" type="read" :key="componentKey">
  Dieser Schritt muss nicht konfiguriert werden.
</div>
<step-template v-else type="read" :key="componentKey">
  <template #left>
    <div class="hide-sections mark-area" :class="markColorStyle">
      <div class="markers">
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
      <div style="position: relative">
	<div id="user-mark-area-content-outer">
	  <div id="user-mark-area-content" v-html="currentCase.userFacts"></div>
	</div>
	<div id="mark-area-content" class="user-markers" v-html="currentCase.userFacts" @mouseup="markUp()"></div>
      </div>
    </div>
  </template>
  <template #right>
    <p>
      Lese den Sachverhalt.
    </p>
    <p>
      Du kannst Wörter im Sachverhalt in unterschiedlichen Farben markieren. Diese werden in den nachfolgenden Schritten angezeigt.
    </p>
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
import { nextTick } from "vue";

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
      hltr: null,
      colors: {
	"marker-1": "rgb(101,255,255)",
	"marker-2": "rgb(102,255,255)",
	"marker-3": "rgb(103,255,255)",
	"marker-4": "rgb(104,255,255)",
	"marker-5": "rgb(105,255,255)",
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
  methods: {
    nextStep() {
      this.$parent.nextStep();
    },
    setColor(name) {
      this.markColor = name;
      this.markUp();
    },
    async markUp() {
      if (!this.markColor)
	return;

      var sel = window.getSelection();
      console.log(sel)
      console.log(sel.type)
      console.log(sel.getRangeAt)

      if (sel.type !== "Range" || !sel.getRangeAt)
	return;

      var range = sel.getRangeAt(0);
      console.log(range)
      document.designMode = "on";
      console.log("designMode on")
      sel.removeAllRanges();
      sel.addRange(range);
      console.log(sel)
      console.log(document.getElementById("mark-area-content").innerHTML);
      document.execCommand("removeFormat");
      console.log("removeFormat")
      console.log(document.getElementById("mark-area-content").innerHTML);
      if (this.markColor != "marker-erase")
	document.execCommand("BackColor", false, this.colors[this.markColor]);
      console.log("BackColor")
      console.log(document.getElementById("mark-area-content").innerHTML);
      document.designMode = "off";
      sel.removeAllRanges();
      let html = document.getElementById("mark-area-content").innerHTML;
      console.log(html);
      this.currentCase.userFacts = html;
      this.componentKey += 1;
      await nextTick();
    },
  },
}
function getSelectionHtml() {
    var html = "";
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection();
        if (sel.rangeCount) {
            var container = document.createElement("div");
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                container.appendChild(sel.getRangeAt(i).cloneContents());
            }
            html = container.innerHTML;
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            html = document.selection.createRange().htmlText;
        }
    }
    return html;
}
</script>
<style lang="scss" scoped>
  @import './styles/markers.scss';
</style>
