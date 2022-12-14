<template>
<step-template type="penalties" :key="componentKey">
  <template #left>
    <div class="show-parts" v-html="currentCase.facts"></div>
  </template>
  <template #right>
    <p>
      Ermitteln Sie die zu prüfenden Strafbarkeiten in der für die Lösungsskizze korrekten Reihenfolge.
    </p>
    <div v-for="(penalty, qindex) in currentStep.config">
      <h4>{{ penalty.text }}</h4>
      <SlickList axis="y" v-model="currentStep.answers[qindex]" @sort-end="reRender()">
    	<SlickItem v-for="(answer, index) in currentStep.answers[qindex]" :key="answer" :index="index">
    	  <div class="border">
	    {{ currentStep.answers[qindex][index] }}
    	    <input v-model="currentStep.answers[qindex][index]" @change="handleBlur(qindex, index)" :ref="'input_' + qindex + '_' + index" :class="'input_' + qindex + '_' + index">
    	    <button v-if="currentStep.answers[qindex].length != 1" class="btn btn-success" @click="delAnswer(qindex, index)">-</button>
    	  </div>
    	</SlickItem>
      </SlickList>
    </div>
  </template>
  <template #buttons>
    <button class="btn btn-success" @click="prevStep()">Voriger Schritt</button>
    <button class="btn btn-success" @click="nextStep()">Nächster Schritt</button>
  </template>
</step-template>
</template>

<script>
import StepTemplate from "./StepTemplate.vue";
import { nextTick } from "vue";
import { SlickList, SlickItem } from 'vue-slicksort';

export default {
  name: "StepPenalties",
  components: {
    StepTemplate,
    SlickList,
    SlickItem,
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
    }
  },
  computed: {
  },
  beforeMount() {
    if (typeof this.currentStep.answers !== "undefined")
      return;

    this.currentStep.answers = [];
    for (let i = 0; i < this.currentStep.config.length; i++)
      this.currentStep.answers.push([""])
  },
  mounted() {
    this.$refs.input_0_0[0].focus();
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
    async handleBlur(qindex, index) {
      this.currentStep.answers[qindex] = this.currentStep.answers[qindex].filter(n => n);
      this.currentStep.answers[qindex].push("");
      this.componentKey += 1;
      await nextTick()
      var next_index = index + 1;
      if (next_index >= this.currentStep.answers[qindex].length)
	next_index = this.currentStep.answers[qindex].length - 1;

      console.log(next_index)
      this.$refs["input_" + qindex + "_" + next_index][0].focus();
    },
    delAnswer(qindex, index) {
      this.currentStep.answers[qindex].splice(index, 1);
      this.componentKey += 1;
    },
    reRender() {
      this.componentKey += 1;
    },
  },
}
</script>
<style lang="scss">
</style>
