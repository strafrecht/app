<template>
<div v-if="dataReady">
  <h2>{{ currentCase.name }} (Niveau: {{ currentCase.difficulty }})</h2>
  <div class="row">
    <div class="col-sm-6">
      <h4>Sachverhalt</h4>
      {{ currentCase.facts }}
    </div>
    <div class="col-sm-6 border">
      <h4>Step 1</h4>
      <p>
	Lesen Sie den Sachverhalt.
      </p>
    </div>
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
  name: "Case",
  props: {
    caseId: {
      type: Number,
    },
  },
  data() {
    return {
      dataReady: false,
      currentCase: null,
    }
  },
  async mounted() {
    await this.getCase();
    this.dataReady = true;
  },
  methods: {
    async getCase() {
      await axios
	.get("/falltraining/api/case/" + this.caseId)
	.then((response) => {
	  this.currentCase = response.data;
	});
    }
  }
};
</script>
