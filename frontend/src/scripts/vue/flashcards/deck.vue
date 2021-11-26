<template>
  <div class="deckspace">
    <div>
      <button class="neu btn btn-success" v-show="!flashcardsOpen" @click="showModal = true">neues Deck</button>
      <modal v-if="showModal" @close="showModal = false">
        <template #header>Neues Deck</template>
        <template #body>
          <form>
            <div class="field">
              <label class="label">Name</label>
              <div class="control">
                <textarea class="input" type="text" v-model="name"></textarea>
              </div>
            </div>
            <div class="field">
              <label class="label">Kategorie</label>
              <div class="control">
                <select class="select" v-model="selectedCategory">
                  <option
                    v-for="category in categories"
                    :key="category.id"
                    :value="category.id"
                  >
                    {{ category.name }}
                  </option>
                </select>
              </div>
            </div>
            <!-- 

              DISCLAIMER: use this code to add wiki category per deck
              (possible future feature), vue treeselect is used to 
              show the wiki category dropdown (as it is in 
              add_question.html). wiki category field also should
              be added in models.py in case is gonna be used


              <div class="wiki-category">  
              <label class="label">Wiki Kategorie</label>
            </div>
            <div>
              <treeselect
                class="treeselect"
                v-model="selectedWikiCategory"
                :multiple="true"
                :options="wiki_categories"
              />
            </div> -->
          </form>
        </template>
        <template #footer>
          <button class="btn btn-secondary" @click="showModal = false">Abbrechen</button>
          <button class="btn btn-success" @click="addDeck()">Speichern</button>
        </template>
      </modal>
    </div>
    <br />
    <div class="deckwrap">
      <div class="decks col-10" style="padding: 0" v-show="!flashcardsOpen">
        <div class="deck" v-for="(deck, index) in filteredDecks" :key="deck.id">
          <div class="deckarea" @click="openDeck(deck.id)">
            <h5>{{ deck.name }}</h5>
            <br>
            <br>
            <p v-if="categoriesById[deck.category]">{{ categoriesById[deck.category].name }}</p> 
          </div>
          <div class="buttons">
            <i
              class="bi bi-pencil-square tooltips"
              v-on:click="openEditModal(index)"
            >
              <small class="tooltiptexts">Bearbeiten</small>
            </i>
            <modal v-if="deckToEdit !== null" @close="deckToEdit = null">
              <template #header> Deck bearbeiten </template>
              <template #body>
                <form>
                  <div class="field">
                    <label class="label">Name bearbeiten</label>
                    <div class="control">
                      <textarea class="input" type="text" v-model="new_name"></textarea>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Kategorie bearbeiten</label>
                    <div class="control">
                      <select class="select" v-model="newSelectedCategory">
                        <option
                          v-for="category in categories"
                          :key="category.id"
                          :value="category.id"
                        >
                          {{ category.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </form>
              </template>
              <template #footer>
                <button class="btn btn-secondary" @click="deckToEdit = null">Abbrechen</button>
                <button class="btn btn-success" @click="editDeck()">Speichern</button>
              </template>
            </modal>
            &nbsp; &nbsp;
            <i class="bi bi-trash tooltips" @click="deckToDelete = deck.id">
              <small class="tooltiptexts">Löschen</small>
            </i>
            <modal v-if="deckToDelete !== null" @close="deckToDelete = null">
              <template #header> Deck löschen </template>
              <template #body>
                <p>Sicher?</p>
              </template>
              <template #footer>
                <button class="btn btn-secondary" @click="deckToDelete = null">Abbrechen</button>
                <button class="btn btn-success" @click="deleteDecks">
                  Löschen
                </button>
              </template>
            </modal>
          </div>
        </div>
      </div>
      <div
        class="sidemenu col-3"
        v-show="!flashcardsOpen"
      >
        <div>
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
        <br />
        <h5>Kategorien</h5>
        <a href="/profile/flashcards">Alle</a>
        <div
          class="category"
          v-for="(category, index) in categories"
          :key="category.id"
        >
          <a href="#" @click="openCategory(category.id)">{{ category.name }}</a>
          &nbsp;
          <i
            class="bi bi-pencil-square tooltips"
            v-on:click="openEditCategory(index)"
          >
            <small class="tooltiptexts">Bearbeiten</small>
          </i>
          &nbsp;
          <modal v-if="categoryToEdit !== null" @close="categoryToEdit = null">
            <template #header> Kategorie bearbeiten </template>
            <template #body>
              <form>
                <div class="field">
                  <label class="label">Name bearbeiten</label>
                  <div class="control">
                    <textarea class="input" type="text" v-model="new_category"></textarea>
                  </div>
                </div>
              </form>
            </template>
            <template #footer>
              <button class="btn btn-secondary" @click="categoryToEdit = null">Abbrechen</button>
              <button class="btn btn-success" @click="editCategory()">
                Speichern
              </button>
            </template>
          </modal>
          <i
            class="bi bi-trash tooltips"
            @click="categoryToDelete = category.id"
          >
            <small class="tooltiptexts">Löschen</small>
          </i>
          <modal
            v-if="categoryToDelete !== null"
            @close="categoryToDelete = null"
          >
            <template #header> Kategorie löschen </template>
            <template #body>
              <p>Sicher?</p>
            </template>
            <template #footer>
              <button class="btn btn-secondary" @click="categoryToDelete = null">Abbrechen</button>
              <button class="btn btn-success" @click="deleteCategory">
                Löschen
              </button>
            </template>
          </modal>
        </div>
        <br />
        <div>
          <a href="#" @click="showCatModal = true">+ neue Kategorie</a>
          <modal v-if="showCatModal" @close="showCatModal = false">
            <template #header>Neue Kategorie</template>
            <template #body>
              <form>
                <div class="field">
                  <label class="label">Name</label>
                  <div class="control">
                    <textarea class="input" type="text" v-model="category_name"></textarea>
                  </div>
                </div>
              </form>
            </template>
            <template #footer>
              <button @click="showCatModal = false">Abbrechen</button>
              <button @click="addKategorie()" class="button is-link">
                Speichern
              </button>
            </template>
          </modal>
        </div>
      </div>
    </div>
    <div>
      <div class="flashcards" v-if="flashcardsOpen">
        <flashcard
          :selectedDeckId="selectedDeck"
          @close="onCloseFlashcards"
        ></flashcard>
      </div>
    </div>
  </div>
</template>

<script src="https://unpkg.com/axios/dist/axios.min.js"></script>

<script>
import axios from "axios";
import Modal from "./Modal.vue";
// import Treeselect from "@riophae/vue-treeselect";
import Flashcard from "./flashcard.vue";
// import '@riophae/vue-treeselect/dist/vue-treeselect.css';

export default {
  name: "Decks",
  components: {
    Modal,
    Flashcard,
  },
  data() {
    return {
      decks: [],
      // filteredDecks: [],
      categoryFilter: '',
      sortFilter: '',
      categories: [],
      wiki_categories: [],
      name: "",
      category_name: "",
      deckToEdit: null,
      categoryToEdit: null,
      new_name: "",
      selectedCategory: null,
      newSelectedCategory: null,
      selectedWikiCategory: null,
      showModal: false,
      showCatModal: false,
      deckToDelete: null,
      categoryToDelete: null,
      flashcardsOpen: false,
      selectedDeck: null,
      categoriesById: {}
    };
  },
  created() {
    // to generate the specific url per each deck and category
    const queryParams = new URLSearchParams(window.location.search); 
    const deckId = queryParams.get("deck");
    const categoryId = queryParams.get("category");
    if (deckId) {
      this.selectedDeck = parseInt(deckId);
      this.flashcardsOpen = true;
    }
    if (categoryId) {
      this.selectedCategory = parseInt(categoryId);
    }
  },
  mounted() {
    this.getDecks();
    this.getCategories();
  },
  computed: {
    filteredDecks() {
      let decks = this.categoryFilter ? this.filterByCategory(this.decks, this.categoryFilter) : [...this.decks]

      if (this.sortFilter) {
        decks.sort((a, b) => {
          // sorting by created and updated
          // console.log(new Date(a.created).getTime(), new Date(b.created).getTime())
          let aCreatedTimestamp = new Date(a.created).getTime()
          let bCreatedTimestamp =  new Date(b.created).getTime()
          let aUpdatedTimestamp = new Date(a.updated).getTime()
          let bUpdatedTimestamp =  new Date(b.updated).getTime()
          if (this.sortFilter === 'created-newest') {
            if (aCreatedTimestamp < bCreatedTimestamp) {
              return -1;
            }
            if (aCreatedTimestamp > bCreatedTimestamp) {
              return 1;
            }
          }
          if (this.sortFilter === 'created-oldest') {
            if (aCreatedTimestamp > bCreatedTimestamp) {
              return -1;
            }
            if (aCreatedTimestamp < bCreatedTimestamp) {
              return 1;
            }
          }

           if (this.sortFilter === 'updated-newest') {
            if (aUpdatedTimestamp < bUpdatedTimestamp) {
              return -1;
            }
            if (aUpdatedTimestamp > bUpdatedTimestamp) {
              return 1;
            }
          }
          if (this.sortFilter === 'updated-oldest') {
            if (aUpdatedTimestamp > bUpdatedTimestamp) {
              return -1;
            }
            if (aUpdatedTimestamp < bUpdatedTimestamp) {
              return 1;
            }
          }

          if (this.sortFilter === 'name-asc') {
             if (a.name < b.name) {
              return -1;
            }
            if (a.name > b.name) {
              return 1;
            }
          }

           if (this.sortFilter === 'name-desc') {
             if (a.name > b.name) {
              return -1;
            }
            if (a.name < b.name) {
              return 1;
            }
          }
           
          return 0;
        })
      }

      return decks
    }
  },
  methods: {
    filterByCategory(decks, category) {
      // this.decks?.filter((deck) => deck.category === id);
      return decks.filter((deck) => deck.category === category)
    },
    getDecks() {
      axios
        .get("http://127.0.0.1:8000/profile/flashcards/decks")
        .then((response) => {
          this.decks = response.data;
          // this.filteredDecks = this.decks;
        });
    },
    getCategories() {
      axios
        .get("http://127.0.0.1:8000/profile/flashcards/categories")
        .then((response) => {
          this.categories = response.data

          this.categoriesById = response.data.reduce((acc, cat) => {
            acc[cat.id] = cat
            return acc
          }, {})
        });
    },
    addDeck() {
      axios
        .post("http://127.0.0.1:8000/profile/flashcards/decks", {
          name: this.name,
          category: this.selectedCategory,
          wiki_category: this.selectedWikiCategory,
        })
        .then((response) => {
          let newDeck = {
            id: response.data.id,
            name: this.name,
            category: this.selectedCategory,
            wiki_category: this.selectedWikiCategory,
          };
          this.decks.push(newDeck);
          this.name = "";
          this.selectedCategory = null;
          this.selectedWikiCategory = null;
        })
        .catch((error) => {
          console.log(error);
        });
      this.showModal = false;
    },
    addKategorie() {
      axios
        .post("http://127.0.0.1:8000/profile/flashcards/categories", {
          name: this.category_name,
        })
        .then((response) => {
          let newCategory = {
            id: response.data.id,
            name: this.category_name,
          };
          this.categories.push(newCategory);
          this.categoriesById[newCategory.id] = newCategory;
          this.name = "";
        })
        .catch((error) => {
          console.log(error);
        });
      this.showCatModal = false;
    },
    deleteDecks() {
      axios
        .delete(
          "http://127.0.0.1:8000/profile/flashcards/decks/" + this.deckToDelete
        )
        .then(this.getDecks);
      this.decks = this.decks.filter((deck) => deck.id !== this.deckToDelete);
      this.deckToDelete = null;
    },
    deleteCategory() {
      axios
        .delete(
          "http://127.0.0.1:8000/profile/flashcards/categories/" +
            this.categoryToDelete
        )
        .then(this.getCategories);
      this.categories = this.categories.filter(
        (category) => category.id !== this.categoryToDelete
      );
      this.categoryToDelete = null;
    },
    editDeck() {
      axios
        .put(
          "http://127.0.0.1:8000/profile/flashcards/decks/" +
            this.decks[this.deckToEdit].id,
          {
            name: this.new_name,
            category: this.newSelectedCategory,
          }
        )
        .then(this.getDecks);
      this.new_name = "";
      this.newSelectedCategory = null;
      this.deckToEdit = null;
    },
    editCategory() {
      axios
        .put(
          "http://127.0.0.1:8000/profile/flashcards/categories/" +
            this.categories[this.categoryToEdit].id,
          {
            name: this.new_category,
          }
        )
        .then(this.getCategories);
      this.new_category = "";
      this.categoryToEdit = null;
    },
    openEditModal(id) {
      this.deckToEdit = id;
      this.new_name = this.decks[id].name;
      this.newSelectedCategory = this.decks[id].category;
    },
    openEditCategory(id) {
      this.categoryToEdit = id;
      this.new_category = this.categories[id].name;
    },
    getWikiCategories() {
      axios
        .get("http://127.0.0.1:8000/quiz/api/category_tree/")
        .then((response) => this.wiki_categories.push(response.data));
    },
    onCloseFlashcards() {
      this.flashcardsOpen = false;
      var queryParams = new URLSearchParams(window.location.search);
      queryParams.delete("deck");
      history.pushState(null, null, "?" + queryParams.toString());
    },
    openDeck(deckId) {
      this.flashcardsOpen = true;
      this.selectedDeck = deckId;
      var queryParams = new URLSearchParams(window.location.search);
      queryParams.set("deck", deckId);
      history.pushState(null, null, "?" + queryParams.toString());
    },
    selectCategory(id) {
      this.categoryFilter = id
      // this.filteredDecks = this.decks?.filter((deck) => deck.category === id);
    },
    openCategory(categoryId) {
      this.selectedCategory = categoryId;
      this.selectCategory(categoryId);
      var queryParams = new URLSearchParams(window.location.search);
      queryParams.set("category", categoryId);
      history.pushState(null, null, "?" + queryParams.toString());
    },
  },
};
</script>


<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css");

.decks {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
}

.deckspace {
  padding: 10px;
  background-color: #fff;
  color: #2c3e50;
  height: fit-content;
}

.deck {
  margin: 10px;
  padding: 10px;
  width: 150px;
  height: 200px;
  box-shadow: 5px 5px #a7a7a7;
  background-color: #fff;
  color: #2c3e50;
  height: fit-content;
}

.deck:hover {
  box-shadow: 5px 5px #787878;
}

.deckarea:hover,
.bi:hover {
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

.deckwrap {
  display: inline-flex;
  width: 850px;
}

.sidemenu {
  position: relative;
  float: right;
  flex-direction: column;
}

.neu {
  margin-left: 15px;
}
</style>