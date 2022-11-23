<template>
<div v-if="dataReady" class="deckspace">

  <!-- edit deck modal -->
  <modal v-if="deckToEdit" @close="deckToEdit = null">
    <template #header>Deck bearbeiten </template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Name</label>
          <input class="form-control" :class="errors['name'] && 'form-control is-invalid'" type="text" v-model="new_name" maxlength="100" />
	  <div v-if="errors['name']" class="invalid-feedback">
	    {{ errors['name'].join(' ') }}
	  </div>

        </div>
        <div class="form-group">
          <label>Kategorie</label>
          <select class="custom-select" v-model="newSelectedCategory">
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
	  <label class="label">Wiki Kategorie</label>
	  <treeselect
             class="treeselect"
             v-model="selectedWikiCategory"
             :multiple="false"
	     :disable-branch-nodes="true"
             :options="wiki_categories"
	     />
	</div>
      </form>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="deckToEdit = null">Abbrechen</button>
      <button class="btn btn-success" @click="saveDeck()">Speichern</button>
    </template>
  </modal>

  <!-- new deck modal -->
  <modal v-if="showModal" @close="showModal = false">
    <template #header>Neues Deck</template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Name</label>
          <input class="form-control" type="text" v-model="name" maxlength="100" />
        </div>
        <div class="form-group">
          <label>Kategorie</label>
          <select class="custom-select" v-model="selectedCategory">
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>Wiki Kategorie</label>
          <treeselect
	     class="treeselect"
	     v-model="selectedWikiCategory"
	     :multiple="false"
	     :disable-branch-nodes="true"
	     :options="wiki_categories"
	     />
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="showModal = false">Abbrechen</button>
      <button class="btn btn-success" @click="createDeck()">Speichern</button>
    </template>
  </modal>

  <!-- delete deck modal -->
  <modal v-if="deckToDelete" @close="deckToDelete = null">
    <template #header> Deck löschen </template>
    <template #body>
      <p>Sicher?</p>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="deckToDelete = null">Abbrechen</button>
      <button class="btn btn-success" @click="deleteDeck">
        Löschen
      </button>
    </template>
  </modal>

  <!-- edit category modal -->
  <modal v-if="categoryToEdit" @close="categoryToEdit = null">
    <template #header> Kategorie bearbeiten </template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Name</label>
          <input class="form-control" type="text" v-model="new_category" maxlength="100" />
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

  <!-- delete category modal -->
  <modal v-if="categoryToDelete" @close="categoryToDelete = null">
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

  <!-- new category modal -->
  <modal v-if="showCatModal" @close="showCatModal = false">
    <template #header>Neue Kategorie</template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Name</label>
          <input class="form-control" type="text" v-model="category_name" maxlength="100" />
        </div>
      </form>
    </template>
    <template #footer>
      <button @click="showCatModal = false">Abbrechen</button>
      <button @click="createCategory()" class="button is-link">
        Speichern
      </button>
    </template>
  </modal>

  <!-- deck -->
  <div v-if="flashcardsOpen" class="flashcards">
    <flashcard :selectedDeckId="selectedDeck" @close="onCloseFlashcards"></flashcard>
  </div>
  <div v-else>
    <div>
      <button class="neu btn btn-success" v-show="!flashcardsOpen" @click="showModal = true">neues Deck</button>
    </div>
    <h2>Alle Decks</h2>
    <br />
    <div class="row">
      <div class="col-9">
	<div class="card-columns">
	  <div class="shadow-sm card deck" v-for="(deck, index) in filteredDecks" :key="deck.id">
            <div class="card-body" @click="openDeck(deck.id)">
              <h5 class="card-title">{{ deck.name }}</h5>
	      <p class="deck-category">
		<span v-if="categoriesById[deck.category]">{{ categoriesById[deck.category].name }}</span>
		<span v-else>keine Kategorie</span>
	      </p>
	      <p class="deck-wiki-category">
		<span v-if="wiki_category_label(deck.wiki_category)">{{ wiki_category_label(deck.wiki_category) }}</span>
		<span v-else>keine Wiki-Kategorie</span>
	      </p>
            </div>
            <div class="card-footer">
              <i class="bi bi-pencil-square tooltips" @click="openDeckEditModal(deck.id)">
		<small class="tooltiptexts">Bearbeiten</small>
              </i>
              &nbsp; &nbsp;
              <i class="bi bi-trash tooltips" @click="deckToDelete = deck.id">
		<small class="tooltiptexts">Löschen</small>
              </i>
            </div>
	  </div>
	</div>
      </div>
      <div class="col-3">
	<div class="mb-4">
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

	<div class="mb-4">
          <label>Kategorien</label>
	  <br/>
	  <span class="btn-link" @click="openCategory(null)">Alle</span>
	  <div class="category" v-for="(category, index) in categories" :key="category.id">
            <span class="btn-link" @click="openCategory(category.id)">{{ category.name }}</span>

            <i class="bi bi-trash tooltips float-right" @click="categoryToDelete = category.id">
              <small class="tooltiptexts">Löschen</small>
            </i>
            <i class="bi bi-pencil-square tooltips float-right mr-2" @click="openEditCategory(index)">
              <small class="tooltiptexts">Bearbeiten</small>
            </i>
	  </div>
	  <br />
	  <div>
            <a href="#" class="neu btn btn-primary btn-sm" @click="showCatModal = true">neue Kategorie</a>
	  </div>
	</div>
    </div>
    </div>
  </div>
</div>
<div v-else class="deckspace">
  <h2>Lade Decks…</h2>
</div>
</template>

<script>
import axios from "axios";
import Modal from "./Modal.vue";
import Flashcard from "./Flashcard.vue";
import Treeselect from "@riophae/vue-treeselect";
import '@riophae/vue-treeselect/dist/vue-treeselect.css';

const axios_config = {
  headers: {
    'X-CSRFToken': csrf_token,
  },
  withCredentials: true,
}

export default {
  name: "Decks",
  components: {
    Modal,
    Flashcard,
    Treeselect,
  },
  data() {
    return {
      dataReady: false,
      decks: [],
      // filteredDecks: [],
      categoryFilter: '',
      sortFilter: 'name-asc',
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
      categoriesById: {},
      errors: {}
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
  async mounted() {
    await this.getWikiCategories();
    await this.getCategories();
    await this.getDecks();
    this.dataReady = true;
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
    wiki_category_label(id) {
      if (!this.wiki_categories[0])
	return false;

      var label = "";
      var branches = this.wiki_categories[0]["children"]
      for (let i = 0; i < branches.length; i++) {
	var children = branches[i]["children"];
	for (let j = 0; j < children.length; j++) {
	  if (children[j]["id"] == id)
	    label = children[j]["label"];
	}
      }
      return label;
    },
    async getDecks() {
      await axios
        .get("/flashcards/api/decks")
        .then((response) => {
          this.decks = response.data;
        });
    },
    async getCategories() {
      await axios
        .get("/flashcards/api/categories")
        .then((response) => {
          this.categories = response.data;
          this.categoriesById = response.data.reduce((acc, cat) => {
            acc[cat.id] = cat
            return acc
          }, {})
        });
    },
    createDeck() {
      axios
        .post("/flashcards/api/decks", {
          name: this.name,
          category: this.selectedCategory,
          wiki_category: this.selectedWikiCategory,
        }, axios_config)
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
    createCategory() {
      axios
        .post("/flashcards/api/categories", {
          name: this.category_name,
        }, axios_config)
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
    deleteDeck() {
      axios
        .delete(
          "/flashcards/api/decks/" + this.deckToDelete
          , axios_config)
        .then(this.getDecks);
      this.decks = this.decks.filter((deck) => deck.id !== this.deckToDelete);
      this.deckToDelete = null;
    },
    deleteCategory() {
      axios
        .delete(
          "/flashcards/api/categories/" +
            this.categoryToDelete
          , axios_config)
        .then(this.getCategories);
      this.categories = this.categories.filter(
        (category) => category.id !== this.categoryToDelete
      );
      this.categoryToDelete = null;
    },
    saveDeck() {
      axios
        .put(
          "/flashcards/api/decks/" + this.deckToEdit,
          {
            name: this.new_name,
            category: this.newSelectedCategory,
            wiki_category: this.selectedWikiCategory,
          }
          , axios_config)
        .then(this.getDecks)
	.catch(error => {
	  if (error.response.status == 400)
	    this.errors = error.response.data;
	})
      this.new_name = "";
      this.newSelectedCategory = null;
      this.selectedWikiCategory = null;
      this.deckToEdit = null;
    },
    editCategory() {
      axios
        .put(
          "/flashcards/api/categories/" +
            this.categories[this.categoryToEdit].id,
          {
            name: this.new_category,
          }
        , axios_config)
        .then(this.getCategories);
      this.new_category = "";
      this.categoryToEdit = null;
    },
    openDeckEditModal(id) {
      for (let i = 0; i < this.decks.length; i++) {
	if (this.decks[i].id == id) {
	  this.deckToEdit = id;
	  this.new_name = this.decks[i].name;
	  this.newSelectedCategory = this.decks[i].category;
	  this.selectedWikiCategory = this.decks[i].wiki_category;
	  return true;
	}
      }
      // FIXME: raise error?
      console.log("Deck not found:", id)
    },
    openEditCategory(id) {
      this.categoryToEdit = id;
      this.new_category = this.categories[id].name;
    },
    async getWikiCategories() {
      await axios
        .get("/quiz/api/category_tree/")
        .then((response) => this.wiki_categories.push(response.data));
    },
    onCloseFlashcards() {
      this.flashcardsOpen = false;
    },
    openDeck(deckId) {
      this.flashcardsOpen = true;
      this.selectedDeck = deckId;
    },
    openCategory(id) {
      this.selectedCategory = id;
      this.categoryFilter = id
    },
  },
};
</script>
<style lang="scss" scoped>
  @import './styles/deckspace.scss';
</style>
