<template>
  <div class="cards">
    <h5 v-text="this.selectedDeckName"></h5>
    <div>
      <button class="btn btn-success" :class="gameFinished && 'hide'" @click="showModal = true">
        neue Karte
      </button>
      <button class="btn btn-primary" :class="gameFinished && 'hide'" @click="toggleMode">Spielmodus</button>
      <button class="btn btn-secondary" @click.prevent="$emit('close')">
        Zurück
      </button>
      <modal v-if="showModal" @close="showModal = false">
        <template #header>Neue Karte</template>
        <template #body>
          <form>
            <div class="field">
              <label class="label">Vorderseite</label>
              <div class="control">
                <textarea
                  class="input"
                  type="text"
                  v-model="front_side"
                ></textarea>
              </div>
            </div>
            <br />
            <div class="field">
              <label class="label">Rückseite</label>
              <div class="control">
                <textarea
                  class="input"
                  type="text"
                  v-model="back_side"
                ></textarea>
              </div>
            </div>
            <br />
            <div class="field">
              <label class="label">Deck</label>
              <div class="control">
                <select class="select" v-model="selectedDeck">
                  <option v-for="deck in decks" :key="deck.id" :value="deck.id">
                    {{ deck.name }}
                  </option>
                </select>
              </div>
            </div>
            <br />
          </form>
        </template>
        <template #footer>
          <button class="btn btn-secondary" @click="showModal = false">
            Abbrechen
          </button>
          <button class="btn btn-success" @click="addFlashcard()">
            Speichern
          </button>
        </template>
      </modal>
    </div>
    <br />
    <div class="cards-container">
      <div v-if="showCards == true" class="flashcards col-10">
        <div
          class="card"
          v-for="{ front_side, back_side, deck_name, id } in sortedCards"
          :key="id"
        >
          <div class="flip-card">
            <div class="flip-card-inner">
              <div class="flip-card-front">
                <br />
                <small>{{ front_side }}</small>
                <br />
                <small><i>{{ deck_name }}</i></small>
              </div>
              <div class="flip-card-back">
                <br />
                <small>{{ back_side }}</small>
                <br />
                <small><i>{{ deck_name }}</i></small>
              </div>
            </div>
          </div>
          <div>
            <p></p>
            <i
              class="bi bi-pencil-square tooltips"
              v-on:click="openEditModal(id)"
            >
              <small class="tooltiptexts">Bearbeiten</small>
            </i>
            <modal v-if="cardToEdit" @close="cardToEdit = undefined">
              <template #header> Karte bearbeiten </template>
              <template #body>
                <form>
                  <div class="field">
                    <label class="label">Vorderseite bearbeiten</label>
                    <div class="control">
                      <textarea
                        class="input"
                        type="text"
                        v-model="new_front_side"
                      ></textarea>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Rückseite bearbeiten</label>
                    <div class="control">
                      <textarea
                        class="input"
                        type="text"
                        v-model="new_back_side"
                      ></textarea>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Deck bearbeiten</label>
                    <div class="control">
                      <select class="select" v-model="newSelectedDeck">
                        <option
                          v-for="deck in decks"
                          :key="deck.id"
                          :value="deck.id"
                        >
                          {{ deck.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </form>
              </template>
              <template #footer>
                <button
                  class="btn btn-secondary"
                  @click="cardToEdit = undefined"
                >
                  Abbrechen
                </button>
                <button class="btn btn-success" @click="editFlashcard()">
                  Speichern
                </button>
              </template>
            </modal>
            &nbsp;
            <i class="bi bi-trash tooltips" @click="cardToDelete = id">
              <small class="tooltiptexts">Löschen</small>
            </i>
          </div>
        </div>
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
      </div>
      <div v-if="showCards == true" class="sidemenu col-3">
        <label>Sortieren nach</label>
        <br />
        <select v-model="sortFilter">
          <option value="">Sortieren</option>
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
    <div v-if="showGameMod === true" class="gamemode">
      <div class="swiper-container">
        <div class="swiper-wrapper">
          <div
            class="swiper-slide"
            v-for="({ front_side, back_side, id }) in gameModeCards"
            :key="id"
          >
            <div
              :data-id="id"
              :class="[
                'swiper-flashcard'
              ]"
              :ref="`flashcard-${id}`"
              @click="onSlideClick(id)"
            >
              <div class="flashcard-front">
                <span class="card-content">{{ front_side }}</span>
                <br />  
              </div>
              <div class="flashcard-back">
                <span class="card-content"> {{ back_side }}</span>
                <br />  
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="swiper-controls">
        <!-- <div @click="swipePrev" class="swiper-button-prev"></div> -->
        <button @click.prevent="onCardLearned" class="btn btn-outline-success btn-sm"><small>Gelernt</small></button>
        <button @click.prevent="onCardNotLearned" class="btn btn-outline-danger btn-sm"><small>Nicht Gelernt</small></button>
        <!-- <div @click="swipeNext" class="swiper-button-next"></div> -->
      </div>
    </div>
    <!-- Results of the learning mode of flashcards -->
    <div v-if="gameFinished === true" class="results">
        <h5>Erfolg!</h5>
        <h5>Dies sind die Ergebnisse Ihrer Spielsitzungen:</h5>
        <br>
        <div v-for="result of Object.values(gameProgress)" :key="result.card.id">
          <div>Karte: {{result.card.front_side}}</div>
          <div>Gelernt: {{result.learned}}</div>
          <div>Nicht gelernt: {{result.notLearned}}</div>
          <br>
        </div>
    </div>
  </div>
</template>

<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
<script>
import axios from "axios";
import Modal from "./Modal.vue";
import Swiper from "swiper";

export default {
  name: "Flashcards",
  components: { Modal },
  props: {
    selectedDeckId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      flashcards: [],
      front_side: "",
      back_side: "",
      selectedDeck: 0,
      newSelectedDeck: -1,
      decks: [],
      cardToEdit: undefined,
      new_back_side: "",
      new_front_side: "",
      showModal: false,
      cardToDelete: null,
      showGameMod: false,
      showCards: true,
      sortFilter: "",
      selectedCardIndex: 0,
      rotatedCards:[],
      // gameModeCards: [],
      gameFinished: false,
      gameProgress: {}
    };
  },
  mounted() {
    this.getFlashcards();
    this.getDecks();
    window.addEventListener("keydown", this.onKeyDown);
  },
  beforeDestroy() {
    window.removeEventListener("keydown", this.onKeyDown);
  },
  watch: {
    async showGameMod(showGameMod) {
      if (showGameMod) {
        await this.$nextTick();
        this.initSwiper();
      } else {
        this.flashcardsSwiper && this.flashcardsSwiper.delete();
      }
    },
  },
  computed: {
    selectedFlashcards() {
      if (!this.selectedDeckId) return [];
      return this.flashcards?.filter(
        (flashcard) => flashcard.deck === this.selectedDeckId
      );
    },
    selectedDeckName() {
      return (
        this.decks.find((deck) => deck.id === this.selectedDeckId)?.name || ""
      );
    },
    gameModeCards() {
      const sessionCards = [...this.selectedFlashcards].filter(card => !this.gameProgress[card.id]?.learned).sort((a, b) => {
        return b.probability - a.probability
      })
      return sessionCards
    },
    sortedCards() {
      let cards = [...this.selectedFlashcards];

      if (this.sortFilter) {
        cards.sort((a, b) => {
          let aCreatedTimestamp = new Date(a.created).getTime();
          let bCreatedTimestamp = new Date(b.created).getTime();
          let aUpdatedTimestamp = new Date(a.updated).getTime();
          let bUpdatedTimestamp = new Date(b.updated).getTime();
          if (this.sortFilter === "created-newest") {
            if (aCreatedTimestamp < bCreatedTimestamp) {
              return -1;
            }
            if (aCreatedTimestamp > bCreatedTimestamp) {
              return 1;
            }
          }
          if (this.sortFilter === "created-oldest") {
            if (aCreatedTimestamp > bCreatedTimestamp) {
              return -1;
            }
            if (aCreatedTimestamp < bCreatedTimestamp) {
              return 1;
            }
          }

          if (this.sortFilter === "updated-newest") {
            if (aUpdatedTimestamp < bUpdatedTimestamp) {
              return -1;
            }
            if (aUpdatedTimestamp > bUpdatedTimestamp) {
              return 1;
            }
          }

          if (this.sortFilter === "updated-oldest") {
            if (aUpdatedTimestamp > bUpdatedTimestamp) {
              return -1;
            }
            if (aUpdatedTimestamp < bUpdatedTimestamp) {
              return 1;
            }
          }

          if (this.sortFilter === "name-asc") {
            if (a.front_side < b.front_side) {
              return -1;
            }
            if (a.front_side > b.front_side) {
              return 1;
            }
          }

          if (this.sortFilter === "name-desc") {
            if (a.front_side > b.front_side) {
              return -1;
            }
            if (a.front_side < b.front_side) {
              return 1;
            }
          }
          return 0;
        });
      }
      return cards;
    },
  },
  methods: {
    // in learning mode: if a card is learned it gets removed from the slider
    // if is not learned (click in not learned). it reduces its probabilty of 
    // showing up again in the learnin' mode slider.
    // when you finally clicked 'learned' in all cards, the results of how 
    // many times you did not remember a card content is shown!
    updateCardProbability(modifier = 0) {
      const selectedCardId = this.gameModeCards[this.selectedCardIndex]?.id
      const flashcardIndex = this.flashcards.findIndex(card => card.id === selectedCardId)
      const flashcard = this.flashcards[flashcardIndex];
      const range = (min, max) => Math.floor(Math.random() * (max - min + 1) + min)
      const probability = range(0, 100) + modifier
      const updatedCard = {
        ...flashcard,
        probability: probability < 0 ? 0 : probability
      }
      this.$set(this.flashcards, flashcardIndex, updatedCard)
    },
    onCardLearned() {
      const card = this.gameModeCards[this.selectedCardIndex]    
      if (!(card.id in this.gameProgress)) {
        this.$set(this.gameProgress, card.id, {
          card,
          learned: 0,
          notLearned: 0
        })
      }
      this.$set(this.gameProgress[card.id], 'learned', 1)
      if (this.gameModeCards.length == 0) {
        this.showGameMod = false
        this.gameFinished = true
      }
    },
    onCardNotLearned() {
      const card = this.gameModeCards[this.selectedCardIndex]
      if (!(card.id in this.gameProgress)) {
        this.$set(this.gameProgress, card.id, {
          card,
          learned: 0,
          notLearned: 0
        })
      }
      // this.gameProgress[card.id].notLearned++
      this.$set(this.gameProgress[card.id], 'notLearned', this.gameProgress[card.id].notLearned + 1)
      this.updateCardProbability(-33)
    },
    // onKeyDown(e) {
    //   if (!this.flashcardsSwiper) return;
    //   if (e.key === "ArrowRight") this.swipeNext();
    //   else if (e.key === "ArrowLeft") this.swipePrev();
    // },
    swipeNext() {
      this.selectedCardIndex += 1;
      if (!this.flashcardsSwiper) return;
      this.flashcardsSwiper.slideNext();
    },
    swipePrev() {
      this.selectedCardIndex -= 1;
      if (!this.flashcardsSwiper) return;
      this.flashcardsSwiper.slidePrev();
    },
    onSlideClick(id) {
      const $flashcard = this.$refs[`flashcard-${id}`]?.[0]
      if (!$flashcard) return

      const rotatedCardIndex = this.rotatedCards.findIndex((el) => el === id);
      if (rotatedCardIndex < 0){
        $flashcard.classList.add('swiper-slide-rotate')
        this.rotatedCards.push(id)
      } else {
        $flashcard.classList.remove('swiper-slide-rotate')
        this.rotatedCards.splice(rotatedCardIndex,1);
      }
    },
    initSwiper() {
      this.flashcardsSwiper = new Swiper(".swiper-container", {
        keyboard: {
          enabled: true,
          onlyInViewport: false,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      });
    },
    getFlashcards() {
      axios
        .get("http://127.0.0.1:8000/profile/flashcards/cards")
        .then((response) => (this.flashcards = response.data));
    },
    addFlashcard() {
      axios
        .post("http://127.0.0.1:8000/profile/flashcards/cards", {
          front_side: this.front_side,
          back_side: this.back_side,
          deck: this.selectedDeck,
        })
        .then((response) => {
          let newFlashcard = {
            id: response.data.id,
            front_side: this.front_side,
            back_side: this.back_side,
            deck: this.selectedDeck,
          };
          this.flashcards.push(newFlashcard);
          this.front_side = "";
          this.back_side = "";
          this.selectedDeck = null;
          this.getFlashcards();
          this.showModal = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    editFlashcard() {
      axios
        .put(
          "http://127.0.0.1:8000/profile/flashcards/cards/" +
            this.cardToEdit.id,
          {
            front_side: this.new_front_side,
            back_side: this.new_back_side,
            deck: this.newSelectedDeck,
          }
        )
        .then(this.getFlashcards);
      this.new_front_side = "";
      this.new_back_side = "";
      this.newSelectedDeck = null;
      this.cardToEdit = null;
    },
    deleteFlashcard() {
      axios
        .delete(
          "http://127.0.0.1:8000/profile/flashcards/cards/" + this.cardToDelete
        )
        .then(this.getFlashcards);
      this.flashcards = this.flashcards.filter(
        (flashcard) => flashcard.id !== this.cardToDelete
      );
      this.cardToDelete = null;
    },
    getDecks() {
      axios
        .get("http://127.0.0.1:8000/profile/flashcards/decks")
        .then((response) => (this.decks = response.data));
    },
    openEditModal(cardToEditId) {
      this.cardToEdit = this.flashcards.find(({ id }) => id === cardToEditId);
      if (!this.cardToEdit) {
        return;
      }
      this.new_front_side = this.cardToEdit.front_side;
      this.new_back_side = this.cardToEdit.back_side;
      this.newSelectedDeck = this.cardToEdit.deck;
    },
    toggleMode() {
      if (this.gameModeCards.length > 0) {
        this.showGameMod = !this.showGameMod;
        this.showCards = !this.showCards;
      }
      else {
        alert("Zuerst eine Karte erstellen");
      }
      
    },
  },
};
</script>

<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css");
@import url("https://unpkg.com/swiper/swiper-bundle.min.css");

.gamemode {
  overflow: hidden; 
  width: 270px;
  margin: 0 auto;
}

.swiper-controls {
  width: 12rem;
  height: 2.1rem;
  margin: 1rem auto;
  display: flex;
  justify-content: space-between;
}

.swiper-controls .swiper-button-next,
.swiper-controls .swiper-button-prev {
  position: relative;
  margin-top: 0;
  inset: initial;
}

.swiper-container {
  width: 18rem;
  height: 25rem;
}

.swiper-slide {
  perspective: 1000px;
}

.swiper-flashcard {
  background: #fff;
  border-radius: 1em;
  width: 16rem;
  height: 24rem;
  transition: 0.5s;
  transform-style: preserve-3d;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.flashcard-back {
  transform: rotateY(180deg);
}

.swiper-slide-rotate {
  transform: rotateY(180deg);
}

.flashcard-front,
.flashcard-back {
  border-radius: 1em;
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: small;
}

.flashcard-front {
  background: #e9e9e9;
}

.flashcard-back {
  background: #cfe6d4;
}

.flashcards {
  display: flex;
  flex-wrap: wrap;
}

.card {
  margin: 5px;
  padding: 4px;
  background-color: #fff;
  color: #2c3e50;
  height: fit-content;
  border: none;
}

.flip-card {
  border-radius: 1em;
  background-color: transparent;
  width: 150px;
  height: 220px;
  perspective: 1000px;
}

.flip-card-inner {
  border-radius: 1em;
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s;
  transform-style: preserve-3d;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  padding: 0px 10px 0px 10px;
  border-radius: 1em;
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}

.flip-card-front {
  background-color: rgb(233, 233, 233);
  color: black;
}

.flip-card-back {
  background-color: rgb(233, 233, 233);
  color: black;
  transform: rotateY(180deg);
}

i:hover {
  cursor: pointer;
}

.tooltips {
  position: relative;
  display: inline-block;
}

.tooltips .tooltiptexts {
  visibility: hidden;
  width: 80px;
  top: 100%;
  left: 50%;
  margin-left: -60px; /* Use half of the width (120/2 = 60), to center the tooltip */
  background-color: rgba(0, 0, 0, 0.639);
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;
  position: absolute;
  z-index: 1;
}

.tooltips:hover .tooltiptexts {
  visibility: visible;
}

.sidemenu {
  position: relative;
  float: right;
}

.cards-container {
  display: inline-flex;
  width: 850px;
}

.swiper-button-next:after,
.swiper-button-prev:after {
  color: #6c757d;
  font-size: 28px;
}

.card-content {
  margin: 20px;
  text-align: center;
}

.hide {
  display: none;
}

</style>