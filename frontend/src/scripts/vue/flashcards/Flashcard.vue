<template>
<div class="cards">

  <!-- new card modal -->
  <modal v-if="showModal" @close="showModal = false">
    <template #header>Neue Karte</template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Vorderseite</label>
          <textarea class="form-control" type="text" v-model="front_side"></textarea>
        </div>
        <div class="form-group">
          <label>Rückseite</label>
          <textarea class="form-control" type="text" v-model="back_side"></textarea>
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="showModal = false">
        Abbrechen
      </button>
      <button class="btn btn-success" @click="createFlashcard()">
        Speichern
      </button>
    </template>
  </modal>

  <!-- edit card modal -->
  <modal v-if="cardToEdit" @close="cardToEdit = undefined">
    <template #header> Karte bearbeiten </template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Vorderseite</label>
          <textarea class="form-control" type="text" v-model="new_front_side"></textarea>
        </div>
        <div class="form-group">
          <label>Rückseite</label>
          <textarea class="form-control" type="text" v-model="new_back_side"></textarea>
        </div>
        <div class="form-group">
          <label>Deck</label>
          <select class="custom-select" v-model="newSelectedDeck">
            <option v-for="deck in $parent.decks.filter(d => !d.submission)" :key="deck.id" :value="deck.id">
              {{ deck.name }}
            </option>
          </select>
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="cardToEdit = undefined">
        Abbrechen
      </button>
      <button class="btn btn-success" @click="saveFlashcard()">
        Speichern
      </button>
    </template>
  </modal>

  <!-- delete card modal -->
  <modal v-if="cardToDelete !== null" @close="cardToDelete = null">
    <template #header>Karte löschen</template>
    <template #body>
      <p>Sicher?</p>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="cardToDelete = null">
        Abbrechen
      </button>
      <button class="btn btn-success" @click="deleteFlashcard">
        Löschen
      </button>
    </template>
  </modal>

  <!-- flashcards -->
  <h3>Deck: {{ selectedDeck.name }}</h3>
  <div class="my-3">
    <div v-if="showGameMod">
      <button v-if="showGameMod" class="btn btn-secondary" @click="stopGameMode">
	Beenden
      </button>
    </div>
    <div v-if="!showGameMod">
      <button class="btn btn-secondary" @click.prevent="$emit('close')">
	Zurück
      </button>
      <button v-if="!selectedDeck.submission && $parent.editMode" class="btn btn-success" @click="showModal = true">
	neue Karte
      </button>
      <button class="btn btn-primary" @click="startGameMode">
	Spiel starten
      </button>
    </div>
  </div>

  <!-- Results of the learning mode of flashcards -->
  <div v-if="gameFinished" class="results">
    <strong>Fertig! Dies sind die Ergebnisse Ihrer Spielsitzung:</strong>
    <div class="row mt-2">
      <div class="col-9">
	<div class="row">
	  <div class="col-md-4 col-sm-6 col-12 mb-3" v-for="result of Object.values(gameProgress)" :key="result.card.id">
            <div class="flip-card">
              <div class="flip-card-inner">
		<div class="flip-card-front">
		  <div class="flip-card-content"><small>{{ result.card.front_side }}</small></div>
		</div>
		<div class="flip-card-back">
		  <div class="flip-card-content"><small>{{ result.card.back_side }}</small></div>
		</div>
              </div>
            </div>
            <div class="flip-card-buttons mt-1">
	      <div v-if="result.notLearned == 0" class="text-success">Gelernt!</div>
	      <div v-if="result.notLearned > 0" class="text-danger">Nicht gelernt: {{ result.notLearned }}</div>
            </div>
	  </div>
	</div>
      </div>
    </div>
  </div>

  <div v-if="!showGameMod" class="row">
    <div class="col-9">
      <div class="row">
	<div class="col-md-4 col-sm-6 col-12 mb-3" v-for="{ front_side, back_side, id } in sortedCards" :key="id">
          <div class="flip-card">
            <div class="flip-card-inner">
              <div class="flip-card-front">
		<div class="flip-card-content"><small>{{ front_side }}</small></div>
              </div>
              <div class="flip-card-back">
		<div class="flip-card-content"><small>{{ back_side }}</small></div>
              </div>
            </div>
          </div>
          <div v-if="!selectedDeck.submission && $parent.editMode" class="flip-card-buttons mt-1">
            <i style="cursor: pointer" class="fa fa-edit tooltips" @click="openEditModal(id)">
              <small class="tooltiptexts">Bearbeiten</small>
            </i>
            &nbsp;
            <i style="cursor: pointer" class="fa fa-trash text-danger tooltips" @click="cardToDelete = id">
              <small class="tooltiptexts">Löschen</small>
            </i>
          </div>
	</div>
      </div>
    </div>
    <div v-if="$parent.editMode" class="col-3">
      <label>Sortierung</label>
      <br />
      <select class="custom-select" v-model="sortFilter">
        <option value="updated-newest">Aktualisiert (älteste)</option>
        <option value="updated-oldest">Aktualisiert (neueste)</option>
        <option value="created-newest">Erstellt (älteste)</option>
        <option value="created-oldest">Erstellt (neueste)</option>
        <option value="name-asc">Name (absteigend)</option>
        <option value="name-desc">Name (aufsteigend)</option>
      </select>
    </div>
  </div>

  <!-- swiper.js used for learning mode transitions -->
  <div v-if="showGameMod && !gameFinished" class="gamemode">
    <div class="swiper-container">
      <div class="swiper-wrapper">
        <div class="swiper-slide" v-for="({ front_side, back_side, id }) in gameModeCards" :key="id">
          <div :data-id="id" :class="['swiper-flashcard']" :ref="`flashcard-${id}`" @click="onSlideClick(id)" title="Klick um die andere Seite zu sehen">
            <div class="flip-card-inner">
              <div class="flip-card-front">
		<div class="flip-card-content">{{ front_side }}</div>
              </div>
              <div class="flip-card-back">
		<div class="flip-card-content">{{ back_side }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="swiper-controls">
      <button @click.prevent="onCardLearned" class="btn btn-success btn-sm">Gelernt</button>
      <button @click.prevent="onCardNotLearned" class="btn btn-danger btn-sm">Nicht Gelernt</button>
    </div>
  </div>

</div>
</template>

<script>
import axios from "axios";
import Modal from "./Modal.vue";
import Swiper from "swiper";
const axios_config = {
  headers: {
    'X-CSRFToken': csrf_token,
  },
  withCredentials: true,
}

export default {
  name: "Flashcards",
  components: { Modal },
  props: {
    selectedDeck: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      flashcards: [],
      front_side: "",
      back_side: "",
      newSelectedDeck: null,
      cardToEdit: undefined,
      new_back_side: "",
      new_front_side: "",
      showModal: false,
      cardToDelete: null,
      showGameMod: false,
      sortFilter: "name-asc",
      gameFinished: false,
      gameProgress: {},
      gameModeCards: [],
    };
  },
  async mounted() {
    await this.getFlashcards();
  },
  watch: {
    async showGameMod(showGameMod) {
      if (showGameMod) {
        await this.$nextTick();
        this.initSwiper();
      } else {
        this.flashcardsSwiper && this.flashcardsSwiper.delete;
      }
    },
  },
  computed: {
    sortedCards() {
      let cards = this.flashcards;

      cards.sort((a, b) => {
        let aCreatedTimestamp = new Date(a.created).getTime();
        let bCreatedTimestamp = new Date(b.created).getTime();
        let aUpdatedTimestamp = new Date(a.updated).getTime();
        let bUpdatedTimestamp = new Date(b.updated).getTime();
        if (this.sortFilter === "created-newest") {
          if (aCreatedTimestamp < bCreatedTimestamp) return -1;
          if (aCreatedTimestamp > bCreatedTimestamp) return 1;
        }
        if (this.sortFilter === "created-oldest") {
          if (aCreatedTimestamp > bCreatedTimestamp) return -1;
          if (aCreatedTimestamp < bCreatedTimestamp) return 1;
        }
        if (this.sortFilter === "updated-newest") {
          if (aUpdatedTimestamp < bUpdatedTimestamp) return -1;
          if (aUpdatedTimestamp > bUpdatedTimestamp) return 1;
        }
        if (this.sortFilter === "updated-oldest") {
          if (aUpdatedTimestamp > bUpdatedTimestamp) return -1;
          if (aUpdatedTimestamp < bUpdatedTimestamp) return 1;
        }
        if (this.sortFilter === "name-asc") {
          if (a.front_side < b.front_side) return -1;
          if (a.front_side > b.front_side) return 1;
        }
        if (this.sortFilter === "name-desc") {
          if (a.front_side > b.front_side) return -1;
          if (a.front_side < b.front_side) return 1;
        }
        return 0;
      });
      return cards;
    },
  },
  methods: {
    onCardLearned() {
      const card = this.gameModeCards[0]
      if (!this.gameProgress[card.id])
        this.gameProgress[card.id] = { card, learned: 0, notLearned: 0 };
      this.gameProgress[card.id].learned++;

      // remove card from game
      this.gameModeCards.shift();

      if (this.gameModeCards.length == 0)
        this.gameFinished = true;
    },
    onCardNotLearned() {
      const card = this.gameModeCards[0]

      // unrotate card if it was rotated
      const $flashcard = this.$refs[`flashcard-${card.id}`]?.[0]
      $flashcard.classList.remove('swiper-slide-rotate');

      if (!this.gameProgress[card.id])
        this.gameProgress[card.id] = { card, learned: 0, notLearned: 0 };
      this.gameProgress[card.id].notLearned++

      // move card to end of game
      this.gameModeCards.push(this.gameModeCards.shift());

      // finish the game if the last card was not learned
      if (this.gameModeCards.length == 1)
        this.gameFinished = true;
    },
    onSlideClick(id) {
      const $flashcard = this.$refs[`flashcard-${id}`]?.[0]
      $flashcard.classList.toggle('swiper-slide-rotate');
    },
    initSwiper() {
      this.flashcardsSwiper = new Swiper(".swiper-container", {
	allowSlideNext: false,
	allowSlidePrev: false,
	allowTouchMove: false,
        keyboard: {
          enabled: false,
          onlyInViewport: false,
        },
      });
    },
    async getFlashcards() {
      await axios
        .get("/flashcards/api/cards?deck_id=" + this.selectedDeck.id)
        .then((response) => (this.flashcards = response.data));
    },
    createFlashcard() {
      axios
        .post("/flashcards/api/cards", {
          front_side: this.front_side,
          back_side: this.back_side,
          deck: this.selectedDeck.id, // FIXME: check that deck belongs to user
        }, axios_config)
        .then((response) => {
          let newFlashcard = {
            id: response.data.id,
            front_side: this.front_side,
            back_side: this.back_side,
            deck: this.selectedDeck.id,
          };
          this.flashcards.push(newFlashcard);
          this.front_side = "";
          this.back_side = "";
          this.showModal = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    saveFlashcard() {
      axios
        .put(
          "/flashcards/api/cards/" + this.cardToEdit.id,
          {
            front_side: this.new_front_side,
            back_side: this.new_back_side,
            deck: this.newSelectedDeck,
          }
        , axios_config)
        .then(this.getFlashcards);
      this.new_front_side = "";
      this.new_back_side = "";
      this.newSelectedDeck = null;
      this.cardToEdit = null;
    },
    deleteFlashcard() {
      axios
        .delete(
          "/flashcards/api/cards/" + this.cardToDelete
        , axios_config)
        .then(this.getFlashcards);
      this.cardToDelete = null;
    },
    openEditModal(cardToEditId) {
      this.cardToEdit = this.flashcards.find(({ id }) => id === cardToEditId);
      this.new_front_side = this.cardToEdit.front_side;
      this.new_back_side = this.cardToEdit.back_side;
      this.newSelectedDeck = this.cardToEdit.deck;
    },
    startGameMode() {
      if (this.flashcards.length > 0) {
        this.showGameMod = true;
	this.gameFinished = false;
	this.gameProgress = {};
	this.gameModeCards = [...this.flashcards];
	// shufle cards before playing?
	// this.gameModeCards = this.flashcards.sort((a, b) => 0.5 - Math.random());
      } else {
        alert("Zuerst eine Karte erstellen");
      }
    },
    stopGameMode() {
      this.showGameMod = false;
      this.gameFinished = false;
    }
  },
};
</script>
<style lang="scss" scoped>
  @import './styles/flashcard.scss';
</style>
