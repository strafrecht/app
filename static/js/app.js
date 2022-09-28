!function(){"use strict";var e,t={7198:function(e,t,n){var r=n(144),s=n(4070),a=n.n(s),i=(n(5577),n(5674),n(4916),n(5306),n(4304)),o=(n(6992),n(1539),n(8783),n(3948),n(285),n(4765),n(8309),n(7327),n(9714),n(2526),n(1817),n(2165),n(1038),n(7042),n(9669)),c=n.n(o),l=n(1900),d=(0,l.Z)({name:"Modal"},(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("transition",{attrs:{name:"modal"}},[n("div",{staticClass:"modal-mask"},[n("div",{staticClass:"modal-wrapper"},[n("div",{staticClass:"modal-container"},[n("div",{staticClass:"modal-header"},[e._t("header")],2),e._v(" "),n("div",{staticClass:"modal-body"},[e._t("body")],2),e._v(" "),n("div",{staticClass:"modal-footer"},[e._t("footer",[n("button",{staticClass:"modal-default-button",on:{click:function(t){return e.$emit("close")}}},[e._v("\n                OK\n              ")])])],2)])])])])}),[],!1,null,null,null).exports,u=(n(5666),n(9653),n(9826),n(4553),n(561),n(8674),n(7941),n(5003),n(4747),n(9337),n(1329));function f(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function v(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?f(Object(n),!0).forEach((function(t){h(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):f(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function h(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function _(e){return function(e){if(Array.isArray(e))return p(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?p(e,t):void 0}}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function m(e,t,n,r,s,a,i){try{var o=e[a](i),c=o.value}catch(e){return void n(e)}o.done?t(c):Promise.resolve(c).then(r,s)}var g={name:"Flashcards",components:{Modal:d},props:{selectedDeckId:{type:Number,default:null}},data:function(){return{flashcards:[],front_side:"",back_side:"",selectedDeck:0,newSelectedDeck:-1,decks:[],cardToEdit:void 0,new_back_side:"",new_front_side:"",showModal:!1,cardToDelete:null,showGameMod:!1,showCards:!0,sortFilter:"",selectedCardIndex:0,rotatedCards:[],gameFinished:!1,gameProgress:{}}},mounted:function(){this.getFlashcards(),this.getDecks(),window.addEventListener("keydown",this.onKeyDown)},beforeDestroy:function(){window.removeEventListener("keydown",this.onKeyDown)},watch:{showGameMod:function(e){var t,n=this;return(t=regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(!e){t.next=6;break}return t.next=3,n.$nextTick();case 3:n.initSwiper(),t.next=7;break;case 6:n.flashcardsSwiper&&n.flashcardsSwiper.delete();case 7:case"end":return t.stop()}}),t)})),function(){var e=this,n=arguments;return new Promise((function(r,s){var a=t.apply(e,n);function i(e){m(a,r,s,i,o,"next",e)}function o(e){m(a,r,s,i,o,"throw",e)}i(void 0)}))})()}},computed:{selectedFlashcards:function(){var e,t=this;return this.selectedDeckId?null===(e=this.flashcards)||void 0===e?void 0:e.filter((function(e){return e.deck===t.selectedDeckId})):[]},selectedDeckName:function(){var e,t=this;return(null===(e=this.decks.find((function(e){return e.id===t.selectedDeckId})))||void 0===e?void 0:e.name)||""},gameModeCards:function(){var e=this;return _(this.selectedFlashcards).filter((function(t){var n;return!(null!==(n=e.gameProgress[t.id])&&void 0!==n&&n.learned)})).sort((function(e,t){return t.probability-e.probability}))},sortedCards:function(){var e=this,t=_(this.selectedFlashcards);return this.sortFilter&&t.sort((function(t,n){var r=new Date(t.created).getTime(),s=new Date(n.created).getTime(),a=new Date(t.updated).getTime(),i=new Date(n.updated).getTime();if("created-newest"===e.sortFilter){if(r<s)return-1;if(r>s)return 1}if("created-oldest"===e.sortFilter){if(r>s)return-1;if(r<s)return 1}if("updated-newest"===e.sortFilter){if(a<i)return-1;if(a>i)return 1}if("updated-oldest"===e.sortFilter){if(a>i)return-1;if(a<i)return 1}if("name-asc"===e.sortFilter){if(t.front_side<n.front_side)return-1;if(t.front_side>n.front_side)return 1}if("name-desc"===e.sortFilter){if(t.front_side>n.front_side)return-1;if(t.front_side<n.front_side)return 1}return 0})),t}},methods:{updateCardProbability:function(){var e,t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,n=null===(e=this.gameModeCards[this.selectedCardIndex])||void 0===e?void 0:e.id,r=this.flashcards.findIndex((function(e){return e.id===n})),s=this.flashcards[r],a=function(e,t){return Math.floor(Math.random()*(t-e+1)+e)},i=a(0,100)+t,o=v(v({},s),{},{probability:i<0?0:i});this.$set(this.flashcards,r,o)},onCardLearned:function(){var e=this.gameModeCards[this.selectedCardIndex];e.id in this.gameProgress||this.$set(this.gameProgress,e.id,{card:e,learned:0,notLearned:0}),this.$set(this.gameProgress[e.id],"learned",1),0==this.gameModeCards.length&&(this.showGameMod=!1,this.gameFinished=!0)},onCardNotLearned:function(){var e=this.gameModeCards[this.selectedCardIndex];e.id in this.gameProgress||this.$set(this.gameProgress,e.id,{card:e,learned:0,notLearned:0}),this.$set(this.gameProgress[e.id],"notLearned",this.gameProgress[e.id].notLearned+1),this.updateCardProbability(-33)},swipeNext:function(){this.selectedCardIndex+=1,this.flashcardsSwiper&&this.flashcardsSwiper.slideNext()},swipePrev:function(){this.selectedCardIndex-=1,this.flashcardsSwiper&&this.flashcardsSwiper.slidePrev()},onSlideClick:function(e){var t,n=null===(t=this.$refs["flashcard-".concat(e)])||void 0===t?void 0:t[0];if(n){var r=this.rotatedCards.findIndex((function(t){return t===e}));r<0?(n.classList.add("swiper-slide-rotate"),this.rotatedCards.push(e)):(n.classList.remove("swiper-slide-rotate"),this.rotatedCards.splice(r,1))}},initSwiper:function(){this.flashcardsSwiper=new u.Z(".swiper-container",{keyboard:{enabled:!0,onlyInViewport:!1},navigation:{nextEl:".swiper-button-next",prevEl:".swiper-button-prev"}})},getFlashcards:function(){var e=this;c().get("/profile/flashcards/cards").then((function(t){return e.flashcards=t.data}))},addFlashcard:function(){var e=this;c().post("/profile/flashcards/cards",{front_side:this.front_side,back_side:this.back_side,deck:this.selectedDeck}).then((function(t){var n={id:t.data.id,front_side:e.front_side,back_side:e.back_side,deck:e.selectedDeck};e.flashcards.push(n),e.front_side="",e.back_side="",e.selectedDeck=null,e.getFlashcards(),e.showModal=!1})).catch((function(e){console.log(e)}))},editFlashcard:function(){c().put("/profile/flashcards/cards/"+this.cardToEdit.id,{front_side:this.new_front_side,back_side:this.new_back_side,deck:this.newSelectedDeck}).then(this.getFlashcards),this.new_front_side="",this.new_back_side="",this.newSelectedDeck=null,this.cardToEdit=null},deleteFlashcard:function(){var e=this;c().delete("/profile/flashcards/cards/"+this.cardToDelete).then(this.getFlashcards),this.flashcards=this.flashcards.filter((function(t){return t.id!==e.cardToDelete})),this.cardToDelete=null},getDecks:function(){var e=this;c().get("/profile/flashcards/decks").then((function(t){return e.decks=t.data}))},openEditModal:function(e){this.cardToEdit=this.flashcards.find((function(t){return t.id===e})),this.cardToEdit&&(this.new_front_side=this.cardToEdit.front_side,this.new_back_side=this.cardToEdit.back_side,this.newSelectedDeck=this.cardToEdit.deck)},toggleMode:function(){this.gameModeCards.length>0?(this.showGameMod=!this.showGameMod,this.showCards=!this.showCards):alert("Zuerst eine Karte erstellen")}}};function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var y={name:"Decks",components:{Modal:d,Flashcard:(0,l.Z)(g,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"cards"},[n("h5",{domProps:{textContent:e._s(this.selectedDeckName)}}),e._v(" "),n("div",[n("button",{staticClass:"btn btn-success",class:e.gameFinished&&"hide",on:{click:function(t){e.showModal=!0}}},[e._v("\n      neue Karte\n    ")]),e._v(" "),n("button",{staticClass:"btn btn-primary",class:e.gameFinished&&"hide",on:{click:e.toggleMode}},[e._v("Spielmodus")]),e._v(" "),n("button",{staticClass:"btn btn-secondary",on:{click:function(t){return t.preventDefault(),e.$emit("close")}}},[e._v("\n      Zurück\n    ")]),e._v(" "),e.showModal?n("modal",{on:{close:function(t){e.showModal=!1}},scopedSlots:e._u([{key:"header",fn:function(){return[e._v("Neue Karte")]},proxy:!0},{key:"body",fn:function(){return[n("form",[n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Vorderseite")]),e._v(" "),n("div",{staticClass:"control"},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.front_side,expression:"front_side"}],staticClass:"input",attrs:{type:"text"},domProps:{value:e.front_side},on:{input:function(t){t.target.composing||(e.front_side=t.target.value)}}})])]),e._v(" "),n("br"),e._v(" "),n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Rückseite")]),e._v(" "),n("div",{staticClass:"control"},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.back_side,expression:"back_side"}],staticClass:"input",attrs:{type:"text"},domProps:{value:e.back_side},on:{input:function(t){t.target.composing||(e.back_side=t.target.value)}}})])]),e._v(" "),n("br"),e._v(" "),n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Deck")]),e._v(" "),n("div",{staticClass:"control"},[n("select",{directives:[{name:"model",rawName:"v-model",value:e.selectedDeck,expression:"selectedDeck"}],staticClass:"select",on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.selectedDeck=t.target.multiple?n:n[0]}}},e._l(e.decks,(function(t){return n("option",{key:t.id,domProps:{value:t.id}},[e._v("\n                  "+e._s(t.name)+"\n                ")])})),0)])]),e._v(" "),n("br")])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{staticClass:"btn btn-secondary",on:{click:function(t){e.showModal=!1}}},[e._v("\n          Abbrechen\n        ")]),e._v(" "),n("button",{staticClass:"btn btn-success",on:{click:function(t){return e.addFlashcard()}}},[e._v("\n          Speichern\n        ")])]},proxy:!0}],null,!1,3176736359)}):e._e()],1),e._v(" "),n("br"),e._v(" "),n("div",{staticClass:"cards-container"},[1==e.showCards?n("div",{staticClass:"flashcards col-10"},[e._l(e.sortedCards,(function(t){var r=t.front_side,s=t.back_side,a=t.deck_name,i=t.id;return n("div",{key:i,staticClass:"card"},[n("div",{staticClass:"flip-card"},[n("div",{staticClass:"flip-card-inner"},[n("div",{staticClass:"flip-card-front"},[n("br"),e._v(" "),n("small",[e._v(e._s(r))]),e._v(" "),n("br"),e._v(" "),n("small",[n("i",[e._v(e._s(a))])])]),e._v(" "),n("div",{staticClass:"flip-card-back"},[n("br"),e._v(" "),n("small",[e._v(e._s(s))]),e._v(" "),n("br"),e._v(" "),n("small",[n("i",[e._v(e._s(a))])])])])]),e._v(" "),n("div",[n("p"),e._v(" "),n("i",{staticClass:"bi bi-pencil-square tooltips",on:{click:function(t){return e.openEditModal(i)}}},[n("small",{staticClass:"tooltiptexts"},[e._v("Bearbeiten")])]),e._v(" "),e.cardToEdit?n("modal",{on:{close:function(t){e.cardToEdit=void 0}},scopedSlots:e._u([{key:"header",fn:function(){return[e._v(" Karte bearbeiten ")]},proxy:!0},{key:"body",fn:function(){return[n("form",[n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Vorderseite bearbeiten")]),e._v(" "),n("div",{staticClass:"control"},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.new_front_side,expression:"new_front_side"}],staticClass:"input",attrs:{type:"text"},domProps:{value:e.new_front_side},on:{input:function(t){t.target.composing||(e.new_front_side=t.target.value)}}})])]),e._v(" "),n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Rückseite bearbeiten")]),e._v(" "),n("div",{staticClass:"control"},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.new_back_side,expression:"new_back_side"}],staticClass:"input",attrs:{type:"text"},domProps:{value:e.new_back_side},on:{input:function(t){t.target.composing||(e.new_back_side=t.target.value)}}})])]),e._v(" "),n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Deck bearbeiten")]),e._v(" "),n("div",{staticClass:"control"},[n("select",{directives:[{name:"model",rawName:"v-model",value:e.newSelectedDeck,expression:"newSelectedDeck"}],staticClass:"select",on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.newSelectedDeck=t.target.multiple?n:n[0]}}},e._l(e.decks,(function(t){return n("option",{key:t.id,domProps:{value:t.id}},[e._v("\n                        "+e._s(t.name)+"\n                      ")])})),0)])])])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{staticClass:"btn btn-secondary",on:{click:function(t){e.cardToEdit=void 0}}},[e._v("\n                Abbrechen\n              ")]),e._v(" "),n("button",{staticClass:"btn btn-success",on:{click:function(t){return e.editFlashcard()}}},[e._v("\n                Speichern\n              ")])]},proxy:!0}],null,!0)}):e._e(),e._v("\n           \n          "),n("i",{staticClass:"bi bi-trash tooltips",on:{click:function(t){e.cardToDelete=i}}},[n("small",{staticClass:"tooltiptexts"},[e._v("Löschen")])])],1)])})),e._v(" "),null!==e.cardToDelete?n("modal",{on:{close:function(t){e.cardToDelete=null}},scopedSlots:e._u([{key:"header",fn:function(){return[e._v("Karte löschen")]},proxy:!0},{key:"body",fn:function(){return[n("p",[e._v("Sicher?")])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{staticClass:"btn btn-secondary",on:{click:function(t){e.cardToDelete=null}}},[e._v("\n            Abbrechen\n          ")]),e._v(" "),n("button",{staticClass:"btn btn-success",on:{click:e.deleteFlashcard}},[e._v("\n            Löschen\n          ")])]},proxy:!0}],null,!1,4274973295)}):e._e()],2):e._e(),e._v(" "),1==e.showCards?n("div",{staticClass:"sidemenu col-3"},[n("label",[e._v("Sortieren nach")]),e._v(" "),n("br"),e._v(" "),n("select",{directives:[{name:"model",rawName:"v-model",value:e.sortFilter,expression:"sortFilter"}],on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.sortFilter=t.target.multiple?n:n[0]}}},[n("option",{attrs:{value:""}},[e._v("Sortieren")]),e._v(" "),n("option",{attrs:{value:"updated-newest"}},[e._v("Aktualisiert (älteste)")]),e._v(" "),n("option",{attrs:{value:"updated-oldest"}},[e._v("Aktualisiert (neueste)")]),e._v(" "),n("option",{attrs:{value:"created-newest"}},[e._v("Erstellt (älteste)")]),e._v(" "),n("option",{attrs:{value:"created-oldest"}},[e._v("Erstellt (neueste)")]),e._v(" "),n("option",{attrs:{value:"name-asc"}},[e._v("Name (absteigend)")]),e._v(" "),n("option",{attrs:{value:"name-desc"}},[e._v("Name (aufsteigend)")])])]):e._e()]),e._v(" "),!0===e.showGameMod?n("div",{staticClass:"gamemode"},[n("div",{staticClass:"swiper-container"},[n("div",{staticClass:"swiper-wrapper"},e._l(e.gameModeCards,(function(t){var r=t.front_side,s=t.back_side,a=t.id;return n("div",{key:a,staticClass:"swiper-slide"},[n("div",{ref:"flashcard-"+a,refInFor:!0,class:["swiper-flashcard"],attrs:{"data-id":a},on:{click:function(t){return e.onSlideClick(a)}}},[n("div",{staticClass:"flashcard-front"},[n("span",{staticClass:"card-content"},[e._v(e._s(r))]),e._v(" "),n("br")]),e._v(" "),n("div",{staticClass:"flashcard-back"},[n("span",{staticClass:"card-content"},[e._v(" "+e._s(s))]),e._v(" "),n("br")])])])})),0)]),e._v(" "),n("div",{staticClass:"swiper-controls"},[n("button",{staticClass:"btn btn-outline-success btn-sm",on:{click:function(t){return t.preventDefault(),e.onCardLearned(t)}}},[n("small",[e._v("Gelernt")])]),e._v(" "),n("button",{staticClass:"btn btn-outline-danger btn-sm",on:{click:function(t){return t.preventDefault(),e.onCardNotLearned(t)}}},[n("small",[e._v("Nicht Gelernt")])])])]):e._e(),e._v(" "),!0===e.gameFinished?n("div",{staticClass:"results"},[n("h5",[e._v("Erfolg!")]),e._v(" "),n("h5",[e._v("Dies sind die Ergebnisse Ihrer Spielsitzungen:")]),e._v(" "),n("br"),e._v(" "),e._l(Object.values(e.gameProgress),(function(t){return n("div",{key:t.card.id},[n("div",[e._v("Karte: "+e._s(t.card.front_side))]),e._v(" "),n("div",[e._v("Gelernt: "+e._s(t.learned))]),e._v(" "),n("div",[e._v("Nicht gelernt: "+e._s(t.notLearned))]),e._v(" "),n("br")])}))],2):e._e()])}),[],!1,null,null,null).exports},data:function(){return{decks:[],categoryFilter:"",sortFilter:"",categories:[],wiki_categories:[],name:"",category_name:"",deckToEdit:null,categoryToEdit:null,new_name:"",selectedCategory:null,newSelectedCategory:null,selectedWikiCategory:null,showModal:!1,showCatModal:!1,deckToDelete:null,categoryToDelete:null,flashcardsOpen:!1,selectedDeck:null,categoriesById:{}}},created:function(){var e=new URLSearchParams(window.location.search),t=e.get("deck"),n=e.get("category");t&&(this.selectedDeck=parseInt(t),this.flashcardsOpen=!0),n&&(this.selectedCategory=parseInt(n))},mounted:function(){this.getDecks(),this.getCategories()},computed:{filteredDecks:function(){var e,t=this,n=this.categoryFilter?this.filterByCategory(this.decks,this.categoryFilter):function(e){if(Array.isArray(e))return b(e)}(e=this.decks)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?b(e,t):void 0}}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}();return this.sortFilter&&n.sort((function(e,n){var r=new Date(e.created).getTime(),s=new Date(n.created).getTime(),a=new Date(e.updated).getTime(),i=new Date(n.updated).getTime();if("created-newest"===t.sortFilter){if(r<s)return-1;if(r>s)return 1}if("created-oldest"===t.sortFilter){if(r>s)return-1;if(r<s)return 1}if("updated-newest"===t.sortFilter){if(a<i)return-1;if(a>i)return 1}if("updated-oldest"===t.sortFilter){if(a>i)return-1;if(a<i)return 1}if("name-asc"===t.sortFilter){if(e.name<n.name)return-1;if(e.name>n.name)return 1}if("name-desc"===t.sortFilter){if(e.name>n.name)return-1;if(e.name<n.name)return 1}return 0})),n}},methods:{filterByCategory:function(e,t){return e.filter((function(e){return e.category===t}))},getDecks:function(){var e=this;c().get("/profile/flashcards/decks").then((function(t){e.decks=t.data}))},getCategories:function(){var e=this;c().get("/profile/flashcards/categories").then((function(t){e.categories=t.data,e.categoriesById=t.data.reduce((function(e,t){return e[t.id]=t,e}),{})}))},addDeck:function(){var e=this;c().post("/profile/flashcards/decks",{name:this.name,category:this.selectedCategory,wiki_category:this.selectedWikiCategory}).then((function(t){var n={id:t.data.id,name:e.name,category:e.selectedCategory,wiki_category:e.selectedWikiCategory};e.decks.push(n),e.name="",e.selectedCategory=null,e.selectedWikiCategory=null})).catch((function(e){console.log(e)})),this.showModal=!1},addKategorie:function(){var e=this;c().post("/profile/flashcards/categories",{name:this.category_name}).then((function(t){var n={id:t.data.id,name:e.category_name};e.categories.push(n),e.categoriesById[n.id]=n,e.name=""})).catch((function(e){console.log(e)})),this.showCatModal=!1},deleteDecks:function(){var e=this;c().delete("/profile/flashcards/decks/"+this.deckToDelete).then(this.getDecks),this.decks=this.decks.filter((function(t){return t.id!==e.deckToDelete})),this.deckToDelete=null},deleteCategory:function(){var e=this;c().delete("/profile/flashcards/categories/"+this.categoryToDelete).then(this.getCategories),this.categories=this.categories.filter((function(t){return t.id!==e.categoryToDelete})),this.categoryToDelete=null},editDeck:function(){c().put("/profile/flashcards/decks/"+this.decks[this.deckToEdit].id,{name:this.new_name,category:this.newSelectedCategory}).then(this.getDecks),this.new_name="",this.newSelectedCategory=null,this.deckToEdit=null},editCategory:function(){c().put("/profile/flashcards/categories/"+this.categories[this.categoryToEdit].id,{name:this.new_category}).then(this.getCategories),this.new_category="",this.categoryToEdit=null},openEditModal:function(e){this.deckToEdit=e,this.new_name=this.decks[e].name,this.newSelectedCategory=this.decks[e].category},openEditCategory:function(e){this.categoryToEdit=e,this.new_category=this.categories[e].name},getWikiCategories:function(){var e=this;c().get("/quiz/api/category_tree/").then((function(t){return e.wiki_categories.push(t.data)}))},onCloseFlashcards:function(){this.flashcardsOpen=!1;var e=new URLSearchParams(window.location.search);e.delete("deck"),history.pushState(null,null,"?"+e.toString())},openDeck:function(e){this.flashcardsOpen=!0,this.selectedDeck=e;var t=new URLSearchParams(window.location.search);t.set("deck",e),history.pushState(null,null,"?"+t.toString())},selectCategory:function(e){this.categoryFilter=e},openCategory:function(e){this.selectedCategory=e,this.selectCategory(e);var t=new URLSearchParams(window.location.search);t.set("category",e),history.pushState(null,null,"?"+t.toString())}}},k=(0,l.Z)(y,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"deckspace"},[n("div",[n("button",{directives:[{name:"show",rawName:"v-show",value:!e.flashcardsOpen,expression:"!flashcardsOpen"}],staticClass:"neu btn btn-success",on:{click:function(t){e.showModal=!0}}},[e._v("neues Deck")]),e._v(" "),e.showModal?n("modal",{on:{close:function(t){e.showModal=!1}},scopedSlots:e._u([{key:"header",fn:function(){return[e._v("Neues Deck")]},proxy:!0},{key:"body",fn:function(){return[n("form",[n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Name")]),e._v(" "),n("div",{staticClass:"control"},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.name,expression:"name"}],staticClass:"input",attrs:{type:"text"},domProps:{value:e.name},on:{input:function(t){t.target.composing||(e.name=t.target.value)}}})])]),e._v(" "),n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Kategorie")]),e._v(" "),n("div",{staticClass:"control"},[n("select",{directives:[{name:"model",rawName:"v-model",value:e.selectedCategory,expression:"selectedCategory"}],staticClass:"select",on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.selectedCategory=t.target.multiple?n:n[0]}}},e._l(e.categories,(function(t){return n("option",{key:t.id,domProps:{value:t.id}},[e._v("\n                  "+e._s(t.name)+"\n                ")])})),0)])])])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{staticClass:"btn btn-secondary",on:{click:function(t){e.showModal=!1}}},[e._v("Abbrechen")]),e._v(" "),n("button",{staticClass:"btn btn-success",on:{click:function(t){return e.addDeck()}}},[e._v("Speichern")])]},proxy:!0}],null,!1,202653413)}):e._e()],1),e._v(" "),n("br"),e._v(" "),n("div",{staticClass:"deckwrap"},[n("div",{directives:[{name:"show",rawName:"v-show",value:!e.flashcardsOpen,expression:"!flashcardsOpen"}],staticClass:"decks col-10",staticStyle:{padding:"0"}},e._l(e.filteredDecks,(function(t,r){return n("div",{key:t.id,staticClass:"deck"},[n("div",{staticClass:"deckarea",on:{click:function(n){return e.openDeck(t.id)}}},[n("h5",[e._v(e._s(t.name))]),e._v(" "),n("br"),e._v(" "),n("br"),e._v(" "),e.categoriesById[t.category]?n("p",[e._v(e._s(e.categoriesById[t.category].name))]):e._e()]),e._v(" "),n("div",{staticClass:"buttons"},[n("i",{staticClass:"bi bi-pencil-square tooltips",on:{click:function(t){return e.openEditModal(r)}}},[n("small",{staticClass:"tooltiptexts"},[e._v("Bearbeiten")])]),e._v(" "),null!==e.deckToEdit?n("modal",{on:{close:function(t){e.deckToEdit=null}},scopedSlots:e._u([{key:"header",fn:function(){return[e._v(" Deck bearbeiten ")]},proxy:!0},{key:"body",fn:function(){return[n("form",[n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Name bearbeiten")]),e._v(" "),n("div",{staticClass:"control"},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.new_name,expression:"new_name"}],staticClass:"input",attrs:{type:"text"},domProps:{value:e.new_name},on:{input:function(t){t.target.composing||(e.new_name=t.target.value)}}})])]),e._v(" "),n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Kategorie bearbeiten")]),e._v(" "),n("div",{staticClass:"control"},[n("select",{directives:[{name:"model",rawName:"v-model",value:e.newSelectedCategory,expression:"newSelectedCategory"}],staticClass:"select",on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.newSelectedCategory=t.target.multiple?n:n[0]}}},e._l(e.categories,(function(t){return n("option",{key:t.id,domProps:{value:t.id}},[e._v("\n                        "+e._s(t.name)+"\n                      ")])})),0)])])])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{staticClass:"btn btn-secondary",on:{click:function(t){e.deckToEdit=null}}},[e._v("Abbrechen")]),e._v(" "),n("button",{staticClass:"btn btn-success",on:{click:function(t){return e.editDeck()}}},[e._v("Speichern")])]},proxy:!0}],null,!0)}):e._e(),e._v("\n             \n          "),n("i",{staticClass:"bi bi-trash tooltips",on:{click:function(n){e.deckToDelete=t.id}}},[n("small",{staticClass:"tooltiptexts"},[e._v("Löschen")])]),e._v(" "),null!==e.deckToDelete?n("modal",{on:{close:function(t){e.deckToDelete=null}},scopedSlots:e._u([{key:"header",fn:function(){return[e._v(" Deck löschen ")]},proxy:!0},{key:"body",fn:function(){return[n("p",[e._v("Sicher?")])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{staticClass:"btn btn-secondary",on:{click:function(t){e.deckToDelete=null}}},[e._v("Abbrechen")]),e._v(" "),n("button",{staticClass:"btn btn-success",on:{click:e.deleteDecks}},[e._v("\n                Löschen\n              ")])]},proxy:!0}],null,!0)}):e._e()],1)])})),0),e._v(" "),n("div",{directives:[{name:"show",rawName:"v-show",value:!e.flashcardsOpen,expression:"!flashcardsOpen"}],staticClass:"sidemenu col-3"},[n("div",[n("label",[e._v("Sortieren nach")]),e._v(" "),n("br"),e._v(" "),n("select",{directives:[{name:"model",rawName:"v-model",value:e.sortFilter,expression:"sortFilter"}],on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.sortFilter=t.target.multiple?n:n[0]}}},[n("option",{attrs:{value:""}},[e._v("Sortieren")]),e._v(" "),n("option",{attrs:{value:"updated-newest"}},[e._v("Aktualisiert (älteste)")]),e._v(" "),n("option",{attrs:{value:"updated-oldest"}},[e._v("Aktualisiert (neueste)")]),e._v(" "),n("option",{attrs:{value:"created-newest"}},[e._v("Erstellt (älteste)")]),e._v(" "),n("option",{attrs:{value:"created-oldest"}},[e._v("Erstellt (neueste)")]),e._v(" "),n("option",{attrs:{value:"name-asc"}},[e._v("Name (absteigend)")]),e._v(" "),n("option",{attrs:{value:"name-desc"}},[e._v("Name (aufsteigend)")])])]),e._v(" "),n("br"),e._v(" "),n("h5",[e._v("Kategorien")]),e._v(" "),n("a",{attrs:{href:"/profile/flashcards"}},[e._v("Alle")]),e._v(" "),e._l(e.categories,(function(t,r){return n("div",{key:t.id,staticClass:"category"},[n("a",{attrs:{href:"#"},on:{click:function(n){return e.openCategory(t.id)}}},[e._v(e._s(t.name))]),e._v("\n         \n        "),n("i",{staticClass:"bi bi-pencil-square tooltips",on:{click:function(t){return e.openEditCategory(r)}}},[n("small",{staticClass:"tooltiptexts"},[e._v("Bearbeiten")])]),e._v("\n         \n        "),null!==e.categoryToEdit?n("modal",{on:{close:function(t){e.categoryToEdit=null}},scopedSlots:e._u([{key:"header",fn:function(){return[e._v(" Kategorie bearbeiten ")]},proxy:!0},{key:"body",fn:function(){return[n("form",[n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Name bearbeiten")]),e._v(" "),n("div",{staticClass:"control"},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.new_category,expression:"new_category"}],staticClass:"input",attrs:{type:"text"},domProps:{value:e.new_category},on:{input:function(t){t.target.composing||(e.new_category=t.target.value)}}})])])])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{staticClass:"btn btn-secondary",on:{click:function(t){e.categoryToEdit=null}}},[e._v("Abbrechen")]),e._v(" "),n("button",{staticClass:"btn btn-success",on:{click:function(t){return e.editCategory()}}},[e._v("\n              Speichern\n            ")])]},proxy:!0}],null,!0)}):e._e(),e._v(" "),n("i",{staticClass:"bi bi-trash tooltips",on:{click:function(n){e.categoryToDelete=t.id}}},[n("small",{staticClass:"tooltiptexts"},[e._v("Löschen")])]),e._v(" "),null!==e.categoryToDelete?n("modal",{on:{close:function(t){e.categoryToDelete=null}},scopedSlots:e._u([{key:"header",fn:function(){return[e._v(" Kategorie löschen ")]},proxy:!0},{key:"body",fn:function(){return[n("p",[e._v("Sicher?")])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{staticClass:"btn btn-secondary",on:{click:function(t){e.categoryToDelete=null}}},[e._v("Abbrechen")]),e._v(" "),n("button",{staticClass:"btn btn-success",on:{click:e.deleteCategory}},[e._v("\n              Löschen\n            ")])]},proxy:!0}],null,!0)}):e._e()],1)})),e._v(" "),n("br"),e._v(" "),n("div",[n("a",{attrs:{href:"#"},on:{click:function(t){e.showCatModal=!0}}},[e._v("+ neue Kategorie")]),e._v(" "),e.showCatModal?n("modal",{on:{close:function(t){e.showCatModal=!1}},scopedSlots:e._u([{key:"header",fn:function(){return[e._v("Neue Kategorie")]},proxy:!0},{key:"body",fn:function(){return[n("form",[n("div",{staticClass:"field"},[n("label",{staticClass:"label"},[e._v("Name")]),e._v(" "),n("div",{staticClass:"control"},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.category_name,expression:"category_name"}],staticClass:"input",attrs:{type:"text"},domProps:{value:e.category_name},on:{input:function(t){t.target.composing||(e.category_name=t.target.value)}}})])])])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{on:{click:function(t){e.showCatModal=!1}}},[e._v("Abbrechen")]),e._v(" "),n("button",{staticClass:"button is-link",on:{click:function(t){return e.addKategorie()}}},[e._v("\n              Speichern\n            ")])]},proxy:!0}],null,!1,220500229)}):e._e()],1)],2)]),e._v(" "),n("div",[e.flashcardsOpen?n("div",{staticClass:"flashcards"},[n("flashcard",{attrs:{selectedDeckId:e.selectedDeck},on:{close:e.onCloseFlashcards}})],1):e._e()])])}),[],!1,null,null,null).exports;!function(){if(document.querySelector(".modern")){var e=document.querySelector(".modern"),t=e.textContent.trimLeft(),n=new i.ZP({el:document.querySelector(".editor"),initialEditType:"wysiwyg",previewStyle:"vertical",height:"600px",initialValue:t,usageStatistics:!1});n.on("change",(function(){e.innerHTML=n.getValue().replace(/\\/g,"")}))}}(),new r.Z({render:function(e){return e(k)}}).$mount("deck"),a()(document).ready((function(){window.console.log("dom ready")}))}},n={};function r(e){var s=n[e];if(void 0!==s)return s.exports;var a=n[e]={exports:{}};return t[e].call(a.exports,a,a.exports,r),a.exports}r.m=t,e=[],r.O=function(t,n,s,a){if(!n){var i=1/0;for(l=0;l<e.length;l++){n=e[l][0],s=e[l][1],a=e[l][2];for(var o=!0,c=0;c<n.length;c++)(!1&a||i>=a)&&Object.keys(r.O).every((function(e){return r.O[e](n[c])}))?n.splice(c--,1):(o=!1,a<i&&(i=a));o&&(e.splice(l--,1),t=s())}return t}a=a||0;for(var l=e.length;l>0&&e[l-1][2]>a;l--)e[l]=e[l-1];e[l]=[n,s,a]},r.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return r.d(t,{a:t}),t},r.d=function(e,t){for(var n in t)r.o(t,n)&&!r.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})},r.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},function(){var e={143:0};r.O.j=function(t){return 0===e[t]};var t=function(t,n){var s,a,i=n[0],o=n[1],c=n[2],l=0;for(s in o)r.o(o,s)&&(r.m[s]=o[s]);if(c)var d=c(r);for(t&&t(n);l<i.length;l++)a=i[l],r.o(e,a)&&e[a]&&e[a][0](),e[i[l]]=0;return r.O(d)},n=self.webpackChunkfrontend=self.webpackChunkfrontend||[];n.forEach(t.bind(null,0)),n.push=t.bind(null,n.push.bind(n))}();var s=r.O(void 0,[216],(function(){return r(7198)}));s=r.O(s)}();
//# sourceMappingURL=app.js.map