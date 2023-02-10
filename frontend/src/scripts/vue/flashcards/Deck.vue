<template>
<div v-if="dataReady" class="deckspace">

  <!-- edit deck modal -->
  <modal v-if="deckToEdit">
    <template #header>Deck bearbeiten </template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Name</label>
          <input class="form-control" :class="errors['name'] && 'form-control is-invalid'" type="text" v-model="deckToEdit.name" maxlength="100" />
	  <div v-if="errors['name']" class="invalid-feedback">
	    {{ errors['name'].join(' ') }}
	  </div>
        </div>

        <div v-if="categories.length > 0" class="form-group">
          <label>Kategorie</label>
          <select class="custom-select" v-model="deckToEdit.category">
	    <option value="">keine Kategorie</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
	  <label class="label">Wiki Kategorie</label>
	  <treeselect class="treeselect" v-model="deckToEdit.wiki_category" :multiple="false" :disable-branch-nodes="true" :options="wiki_categories" placeholder="Bitte wählen…" />
	  <small class="form-text text-muted">
	      Wenn Du dein Deck für andere freigeben willst, wähle hier eine Kategorie im Problemfeldwiki aus.
	  </small>
	</div>
      </form>
    </template>
    <template #footer>
      <button class="btn btn-success" @click="saveDeck()">Speichern</button>
    </template>
  </modal>

  <!-- submit deck modal -->
  <modal v-if="deckToSubmit">
    <template #header>Deck einreichen</template>
    <template #body>
      <p>
	Willst Du dein Deck »{{ deckToSubmit.name }}« im Problemfeldwiki
	unter »{{ wiki_category_label(deckToSubmit.wiki_category) }}« einreichen?
      </p>
      <p>
	Nach der Einreichung werden wir dein Deck prüfen und freigeben.
      </p>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="deckToSubmit = null">Abbrechen</button>
      <button class="btn btn-success" @click="submitDeck()">Einreichen</button>
    </template>
  </modal>

  <!-- new deck modal -->
  <modal v-if="newDeck">
    <template #header>Neues Deck</template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Name</label>
          <input class="form-control" :class="errors['name'] && 'form-control is-invalid'" type="text" v-model="newDeck.name" maxlength="100" />
	  <div v-if="errors['name']" class="invalid-feedback">
	    {{ errors['name'].join(' ') }}
	  </div>
        </div>

	<div v-if="categories.length > 0" class="form-group">
          <label>Kategorie</label>
          <select class="custom-select" v-model="newDeck.category">
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Wiki Kategorie</label>
          <treeselect class="treeselect" v-model="newDeck.wiki_category" :multiple="false" :disable-branch-nodes="true" :options="wiki_categories"/>
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="newDeck = null; errors = {};">Abbrechen</button>
      <button class="btn btn-success" @click="createDeck()">Speichern</button>
    </template>
  </modal>

  <!-- delete deck modal -->
  <modal v-if="deckToDelete">
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
  <modal v-if="categoryToEdit">
    <template #header> Kategorie bearbeiten </template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Name</label>
          <input class="form-control" :class="errors['name'] && 'form-control is-invalid'" type="text" v-model="categoryToEdit.name" maxlength="100" />
	  <div v-if="errors['name']" class="invalid-feedback">
	    {{ errors['name'].join(' ') }}
	  </div>
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn btn-success" @click="saveCategory()">
        Speichern
      </button>
    </template>
  </modal>

  <!-- delete category modal -->
  <modal v-if="categoryToDelete">
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
  <modal v-if="newCategory">
    <template #header>Neue Kategorie</template>
    <template #body>
      <form>
        <div class="form-group">
          <label>Name</label>
          <input class="form-control" :class="errors['name'] && 'form-control is-invalid'" type="text" v-model="newCategory.name" maxlength="100" />
	  <div v-if="errors['name']" class="invalid-feedback">
	    {{ errors['name'].join(' ') }}
	  </div>
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="newCategory = null; errors = {};">Abbrechen</button>
      <button class="btn btn-success" @click="createCategory()">
        Speichern
      </button>
    </template>
  </modal>

  <!-- deck -->
  <div v-if="flashcardsOpen" class="flashcards">
    <flashcard :selectedDeck="selectedDeck" @close="closeDeck"></flashcard>
  </div>
  <div v-else>
    <h3 v-if="editMode">Alle Flashcard-Decks</h3>
    <div v-if="gameMode">
      <h3 v-if="this.decks.length > 0">
	Flashcard-Decks zu dieser Wiki-Seite
      </h3>
      <div v-else>
	<h3>Keine Flashcard-Decks</h3>
	<p>
	  Helfe Strafrecht Online besser zu machen und erstelle ein Flashcard-Deck zu dieser Wiki-Seite in deinem Konto.
	</p>
      </div>
    </div>
    <div class="my-3">
      <button v-if="editMode" class="neu btn btn-success" @click="newDeck = {}">neues Deck</button>
    </div>
    <div class="row">
      <div class="col-9">
	<div class="card-columns">
	  <div class="shadow-sm card deck" v-for="(deck, index) in filteredDecks" :key="deck.id">
            <div class="card-body" @click="openDeck(deck.id)">
              <h5 class="card-title">{{ deck.name }}</h5>
	      <div v-if="editMode">
		<p class="deck-wiki-category small">
		  <span v-if="deck.wiki_category">
		    Wiki-Kategorie: <br/>
		    <i>{{ wiki_category_label(deck.wiki_category) }}</i>
		  </span>
		</p>
		<div class="deck-category">
		  <span v-if="categoriesById[deck.category]" class="badge badge-pill badge-primary">{{ categoriesById[deck.category].name }}</span>
		</div>
              </div>
            </div>
            <div class="card-footer">
	      <div v-if="gameMode">
		<small>von <em>{{ deck.user_name }}</em></small>
		<div v-if="!deck.approved" class="text-danger">
		  Eingereicht!
		  <a :href="cmsUrl(deck.id)" target="_blank">Bitte im CMS freigeben</a>
		</div>
	      </div>
	      <div v-if="editMode" class="text-right">
		<span v-if="deck.approved">
		  <i class="small">Freigegeben!</i>
		</span>
		<span v-else-if="deck.submission">
		  <i class="small">Eingereicht!</i>
		</span>
		<span v-else-if="!deck.submission">
		  <i v-if="deck.wiki_category" style="cursor: pointer" class="fa fa-upload tooltips mr-2" @click="openSubmitDeck(deck.id)">
		    <small class="tooltiptexts">Einreichen</small>
		  </i>
		  <i style="cursor: pointer" class="fa fa-edit tooltips mr-2" @click="openEditDeck(deck.id)">
		    <small class="tooltiptexts">Bearbeiten</small>
		  </i>
		</span>
		<i style="cursor: pointer" class="fa fa-trash tooltips text-danger" @click="deckToDelete = deck.id">
		  <small class="tooltiptexts">Löschen</small>
		</i>
              </div>
            </div>
	  </div>
	</div>
      </div>
      <div v-if="editMode" class="col-3">
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
	  <div v-if="categories.length > 0">
	    <span class="btn-link" @click="selectCategory(null)">Alle</span>
	    <div class="category" v-for="(category, index) in categories" :key="category.id">
              <span class="btn-link" @click="selectCategory(category.id)">{{ category.name }}</span>

              <i style="cursor: pointer" class="fa fa-trash tooltips text-danger float-right" @click="categoryToDelete = category.id">
		<small class="tooltiptexts">Löschen</small>
              </i>
              <i style="cursor: pointer" class="fa fa-edit tooltips float-right mr-2" @click="openEditCategory(index)">
		<small class="tooltiptexts">Bearbeiten</small>
              </i>
	    </div>
	    <br />
	  </div>
	  <div>
            <a href="#" class="btn btn-primary btn-sm" @click.prevent="newCategory = {}">neue Kategorie</a>
	  </div>
	</div>
    </div>
    </div>
  </div>
</div>
<div v-else class="deckspace">
  <h3>Lade Flashcard-Decks…</h3>
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
  props: {
    gameMode: {
      type: Boolean,
      default: false,
    },
    wikiCategory: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      dataReady: false,
      decks: [],
      categoryFilter: '',
      sortFilter: 'name-asc',
      categories: [],
      wiki_categories: [],
      flashcardsOpen: false,
      selectedDeck: null,
      categoriesById: {},
      errors: {},
      categoryToEdit: null,
      categoryToDelete: null,
      newCategory: null,
      deckToEdit: null,
      deckToDelete: null,
      deckToSubmit: null,
      newDeck: null,
    };
  },
  created() {
    // to generate the specific url per each deck and category
    const queryParams = new URLSearchParams(window.location.search);
    const deckId = queryParams.get("deck");
    const categoryId = queryParams.get("category");
    if (deckId) {
      this.selectedDeck = this.deckById(parseInt(deckId));
      this.flashcardsOpen = true;
    }
  },
  async mounted() {
    if (this.gameMode) {
      await this.getDecksForWikiCategory(this.wikiCategory);
    } else {
      await this.getWikiCategories();
      await this.getCategories();
      await this.getDecks();
    }
    this.dataReady = true;
  },
  computed: {
    editMode() {
      return !this.gameMode;
    },
    filteredDecks() {
      let decks = this.categoryFilter ? this.decksByCategory(this.categoryFilter) : this.decks

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
    deckById(id) {
      return this.decks.find((deck) => deck.id === id)
    },
    decksByCategory(category) {
      return this.decks.filter((deck) => deck.category === category)
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
        .then((response) => (this.decks = response.data));
    },
    async getDecksForWikiCategory(id) {
      await axios
        .get("/flashcards/api/decks/for_wiki?article_id=" + id)
        .then((response) => (this.decks = response.data));
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
    cmsUrl(id) {
      return "/cms/flashcards/deck/edit/" + id + "/";
    },
    createDeck() {
      axios
        .post("/flashcards/api/decks", {
          name: this.newDeck.name,
          category: this.newDeck.category,
          wiki_category: this.newDeck.wiki_category,
        }, axios_config)
        .then((response) => {
	  this.newDeck.id = response.data.id;
          this.decks.push(this.newDeck);
	  this.newDeck = null;
	  this.errors = {};
        })
        .catch((error) => {
	  if (error.response.status == 400)
	    this.errors = error.response.data;
        });
    },
    createCategory() {
      axios
        .post("/flashcards/api/categories", {
          name: this.newCategory.name,
        }, axios_config)
        .then((response) => {
          let newCategory = {
            id: response.data.id,
            name: this.newCategory.name,
          };
          this.categories.push(newCategory);
	  this.newCategory = null;
	  this.errors = {}
        })
        .catch((error) => {
	  if (error.response.status == 400)
	    this.errors = error.response.data;
        });
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
      this.categories = this.categories.filter((cat) => cat.id !== this.categoryToDelete);
      this.categoryToDelete = null;
    },
    submitDeck() {
      axios
	.put("/flashcards/api/decks/" + this.deckToSubmit.id + "/submit", {}, axios_config)
	.then(response => {
	  this.deckToSubmit.submission = response.data.submission;
	  this.deckToSubmit = null;
	})
	.catch(error => {
	  alert(error);
	});
    },
    saveDeck() {
      axios
        .put(
          "/flashcards/api/decks/" + this.deckToEdit.id,
          {
            name: this.deckToEdit.name,
            category: this.deckToEdit.category,
	    // treeselect returns undefined for deselected wiki category
	    // set it to null in this case, otherwise it won't be transmitted
            wiki_category: this.deckToEdit.wiki_category || null,
          }
          , axios_config)
        .then((response) => {
	  this.deckToEdit = null;
	  this.errors = {};
	})
	.catch(error => {
	  if (error.response.status == 400)
	    this.errors = error.response.data;
	})
    },
    saveCategory() {
      axios
        .put(
          "/flashcards/api/categories/" + this.categoryToEdit.id,
          {
            name: this.categoryToEdit.name,
          }
        , axios_config)
        .then((response) => {
	  this.getCategories;
	  this.categoryToEdit = null;
	  this.errors = {};
	})
        .catch((error) => {
	  if (error.response.status == 400)
	    this.errors = error.response.data;
        });
    },
    openEditDeck(id) {
      this.deckToEdit = this.decks.filter(x => x.id == id)[0];
    },
    openSubmitDeck(id) {
      this.deckToSubmit = this.decks.filter(x => x.id == id)[0];
    },
    openEditCategory(index) {
      this.categoryToEdit = this.categories[index];
    },
    async getWikiCategories() {
      await axios
        .get("/quiz/api/category_tree/")
        .then((response) => this.wiki_categories.push(response.data));
    },
    closeDeck() {
      this.flashcardsOpen = false;
      this.selectedDeck = null;
    },
    openDeck(deckId) {
      this.flashcardsOpen = true;
      this.selectedDeck = this.deckById(deckId);
    },
    selectCategory(id) {
      this.categoryFilter = id
    },
  },
};
</script>
<style lang="scss" scoped>
  @import './styles/deckspace.scss';
</style>
