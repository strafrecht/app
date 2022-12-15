<template>
  <div class="case-step" :class="stepClass" >
    <div class="row">
      <div class="col-sm-6">
	<div class="col-sm-12 bg-light shadow">
	  <slot name="left"> </slot>
	</div>
      </div>
      <div class="col-sm-6">
	<div class="col-sm-12 border">
	  <slot name="right"> </slot>
	</div>
      </div>
    </div>
    <slot name="bottom"> </slot>
    <slot name="buttons"> </slot>
  </div>
</template>

<script>
export default {
  name: "StepTemplate",
  props: ["type"],
  computed: {
    stepClass() {
      return "case-type-" + this.type;
    }
  },
}
</script>
