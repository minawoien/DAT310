let studentC = {
    // property for innlogget bruker
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
                    <option v-for="p in bedrifter" :value="p">{{p.name}}</option>
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
            display: false
        }
    },
    created: async function(){
        // Henter innlegg hver gang siden blir åpnet, sjekker om innleggene er stillingsannonser eller innlegg fra styret i 
        // postType funksjonen
        let response = await fetch('/post');
        if (response.status == 200){
            let result = await response.json();
            this.posts = result;
        }
        this.postType();
        // Heter filtreingscookie
        this.getCookie();
    },
    watch: {
        // Setter cookie ettersom listen med stillingsannonser blir filtrert
        filteredList: function(){
            this.setCookie();
        }

    },
    methods: {
        // Oppdaterer hvilke innlegg som vises ved å nullstille listene med innlegg fra styret og stillingsannonser,
        // og legge til eksisterene innlegg i riktig liste ut i fra type
        // Funksjonen blir kalt når admin sletter et innlegg og hver gang siden åpnes (da det kan ha blitt lagt til flere innlegg)
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
                    // Legger til navn og id til bedriftene som har lagt ut stillingsannonser i en liste som blir brukt til 
                    // nedtrekksliste for filtrering.
                    // Hvis en bedirft har publisert mer enn en annonse vil bedriftnavnet bare vist en gang i nedtrekkslisten
                    if(!this.bedrifter.some(bedrift => bedrift.name == this.posts[p].userid["name"])){
                        this.bedrifter.push({
                            "name": this.posts[p].userid['name'],
                            "bid": this.posts[p].userid['bid']
                        })
                    }

                }
            }
        },
        // Sletter innlegg eller annonse med gitt id og oppdaterer hvilke innlegg som vises i postType-funksjonen
        deletePost: async function(id){
            let response = await fetch('/delete' ,{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({'id': id})
            });
            if (response.status == 200){
                let result = await response.json();
                this.posts = result;
                this.postType()
            }
        },
        // Setter en cookie på en dictionary med hvilke filtreringer som er valgt, og setter den som permanet
        // Lagrer kun id for bedriften som er valgt da en bedrift har mulighet for å endre bedriftnavn
        // (cookien blir kun slettet når en bruker logger ut)
        setCookie: function(){
            let data = {
                "selected": this.selected["bid"],
                "inpSearch": this.inpSearch,
                "checkedTimes": this.checkedTimes 
            }
            document.cookie = "list="+JSON.stringify(data)+";SameSite=strict;max-age=31536000;";
        },
        // Henter cookie og spliter så vi får dictionarien og kan fordele valgene på filtreringen
        // Kilde: https://www.w3schools.com/js/js_cookies.asp
        getCookie: function(){
            var name =  "list=";
            var decodedCookie = decodeURIComponent(document.cookie);
            var ca = decodedCookie.split(';');
            for(var i = 0; i <ca.length; i++) {
              var c = ca[i];
              while (c.charAt(0) == ' ') {
                c = c.substring(1);
              }
              if (c.indexOf(name) == 0) {
                let data = JSON.parse(c.substring(name.length, c.length))
                // Finner navnet på bedriften som er valgt ut i fra lagret bedriftid, og setter id og navn som selected for nedtrekkslisten
                for (j in this.bedrifter){
                    if (data.selected == this.bedrifter[j].bid){
                        this.selected = {
                            "name": this.bedrifter[j].name,
                            "bid": this.bedrifter[j].bid
                         }
                    }
                 }
                 // Setter lagret søk og hvilke/n checkbox 
                 this.inpSearch = data.inpSearch;
                 this.checkedTimes = data.checkedTimes;
              }
            }
        },
        filter: function(){
            this.display = !this.display
        },
        // Funksjon for sortering av type stilling og søk i tekst
        // Hvis alle eller ingen type er valgt blir kun sortering på søk returnert
        typeAndSearch: function(p){
            if (this.checkedTimes.length == 1){
                return p.type.includes(this.checkedTimes) && p.text.toLowerCase().includes(this.inpSearch.toLowerCase()) 
            }else if (this.checkedTimes.length == 2){
                return p.type.includes(this.checkedTimes[0]) && p.text.toLowerCase().includes(this.inpSearch.toLowerCase()) || p.type.includes(this.checkedTimes[1]) && p.text.toLowerCase().includes(this.inpSearch.toLowerCase()) 
            }else{
                return p.text.toLowerCase().includes(this.inpSearch.toLowerCase())   
            }
        }
    },
    computed: {
        // Sortering på søk, bedriftnavn og stillingstype
        // Sjekker først om det er valgt en bedrift, før typeAndSearch funksjonen sjekker om det er valgt en type stilling 
        // og/eller om det er gjort et søk i teksten
        filteredList() {
          return this.annonser.filter(p => {
            if (this.selected) {
                this.show = p.userid['name'].includes(this.selected["name"]) && this.typeAndSearch(p)
            }else{
                this.show = this.typeAndSearch(p)
            }
            return this.show
          })
        }
    }
};