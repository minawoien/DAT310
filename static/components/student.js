//const { throwStatement } = require("jscodeshift");

let studentC = {
    // property for the logged in user
    props: ["bruker"],
    template: /*html*/`
    <div class="pages content">
        <div class="innlegg">
            <h1>Innlegg fra styret</h1>
            <innlegg v-for="p in innlegg" v-bind:p="p" v-bind:bruker="bruker"></innlegg>
        </div>
        <div class="annonser">
            <span id="searchIcon" v-on:click="filter" v-if="!display"></span>
            <form action=""  v-if="display">
                <span class="removeIcon" v-on:click="filter" v-if="display"></span>
                <h3>Filtrer søk</h3>
                <input type="text" placeholder="Søk i tekst" v-model="inpSearch"/>
                <fieldset>
                    <label><input type="checkbox" name="type" value="Heltid" v-model="checkedTimes" />Heltid</label>
                    <label><input type="checkbox" name="type" value="Deltid" v-model="checkedTimes" />Deltid</label>
                    <label><input type="checkbox" name="type" value="Sommerjobb" v-model="checkedTimes" />Sommerjobb</label>
                </fieldset>
                <select v-model="selected">
                    <option selected value="">Velg bedrift</option>
                    <option v-for="p in bedrifter" :value="p">{{p}}</option>
                </select>
            </form>
            <h1>Stillingsannonser</h1>
            <annonse v-for="p in filteredList" v-bind:p="p" v-bind:bruker="bruker"></annonse>
        </div>
    </div>

    `,
    data: function(){
        return {
            posts: [],
            annonser: [],
            innlegg: [],
            inpSearch: '',
            show: [],
            selected: '',
            bedrifter: [],
            checkedTimes: [],
            display: false,
            liste: []
        }
    },
    created: async function(){
        let response = await fetch('/post');
        if (response.status == 200){
            let result = await response.json();
            this.posts = result;
        }
        this.postType();
        this.getCookie();
    },
    watch: {
        filteredList: function(){
            this.setCookie();
        }
    },
    methods: {
        deletePost: async function(id){
            console.log("deleting: ")
            console.log(id)
            let response = await fetch('/delete?post_id='+id);
            if (response.status == 200){
                let result = await response.json();
                this.posts = result;
                this.postType()
            }
        },
        postType: function(){
            this.bedrifter = [];
            this.innlegg = [];
            this.annonser = [];
            for (p in this.posts){
                if (this.posts[p]["type"] == "innlegg"){
                    this.innlegg.push(this.posts[p])
                }
                else{
                    this.annonser.push(this.posts[p])
                    if (!this.bedrifter.includes(this.posts[p].userid['name'])){
                        this.bedrifter.push(this.posts[p].userid['name'])
                    }
                }
            }
        },
        // Funksjon for sortering av type stilling 
        // Hvis alle eller ingen er valgt blir kun sortering på søk returnert
        typeAndSearch: function(p){
            if (this.checkedTimes.length == 1){
                return p.type.includes(this.checkedTimes) && p.text.toLowerCase().includes(this.inpSearch.toLowerCase()) 
            }else if (this.checkedTimes.length == 2){
                return p.type.includes(this.checkedTimes[0]) && p.text.toLowerCase().includes(this.inpSearch.toLowerCase()) || p.type.includes(this.checkedTimes[1]) && p.text.toLowerCase().includes(this.inpSearch.toLowerCase()) 
            }else{
                return p.text.toLowerCase().includes(this.inpSearch.toLowerCase())   
            }
        },
        filter: function(){
            this.display = !this.display
        },
        setCookie: function(){
            // Set cookie with expiration date after a year
            document.cookie = "list="+this.filteredList+";SameSite=strict;max-age=31536000;";
        },
        getCookie: function(){
            console.log("heiiiiiii");
        }
    },
    computed: {
        // Sortering på søk, bedriftnavn og stillingstype
        // TypeAndSearch funskjonen returnerer annonsene sortert etter søk og type
        filteredList() {
          return this.annonser.filter(p => {
            if (this.selected) {
                this.show = p.userid['name'].includes(this.selected) && this.typeAndSearch(p)
            }else{
                this.show = this.typeAndSearch(p)
            }
            return this.show
          })
        }
    }

};