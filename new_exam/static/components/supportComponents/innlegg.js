const annonseC = {
    props: ["bruker", "p"],
    template: /*html*/`
    <div class="post">
        <span class="deleteIcon" v-if="bruker.role == 'admin'" v-on:click="deletePost(p.id);"></span>
        <h3>{{p.userid["name"]}}</h3>
        <p>{{p.type}} i {{p.place}}</p>
        <p>Søknadsfrist: {{p.date}}</p>
        <p>{{ p.text }}</p>
        <a href="#">{{p.link}}</a>
    </div>
`,
    methods: {
        // Kaller på parent funksjonen i student for å slette en annonse
        deletePost: function(id){
            this.$parent.deletePost(id);
        }
    }
};

const innleggC = {
    props: ["bruker", "p"],
    template: /*html*/`
    <div class="post">
        <span class="deleteIcon" v-if="bruker.role == 'admin'" v-on:click="deletePost(p.id);"></span>
        <h3>{{p.title}}</h3>
        <p>Publisert av {{p.userid["firstname"]}} | {{p.userid["stilling"]}}</p>
        <p style="color: #60a2a7">{{p.date}}</p>
        <p>{{ p.text }}</p>
        <a href="#">{{p.link}}</a>
    </div>
`,
    methods: {
        // Kaller på parent funksjonen i student for å slette et innlegg
        deletePost: function(id){
            this.$parent.deletePost(id);
        }
    }
};

