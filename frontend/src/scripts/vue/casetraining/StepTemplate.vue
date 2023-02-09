<template>
  <div class="case-step" :class="stepClass" >
    <div class="row">
      <div class="col-md-6 order-md-2 col-sm-12 order-sm-1">
	<div class="col-sm-12 border py-3">
	  <slot name="right"></slot>
	</div>
	<div class="next-case-step mt-3 mb-3 text-right">
	  <slot name="buttons-right"></slot>
	</div>
      </div>
      <div class="col-md-6 order-md-1 col-sm-12 order-sm-2">
	<div  v-if="$slots.left" class="col-sm-12 bg-light shadow py-3">
	  <slot name="left"></slot>
	</div>
      </div>
    </div>
    <slot name="bottom"></slot>
    <div class="row">
      <div class="col text-right mt-3">
	<slot name="buttons"></slot>
      </div>
    </div>
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
