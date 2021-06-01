let menuC = {
    // property for the logged in user
    props: ["bruker"],
    template: /*html*/`
    <header>
        <nav>
            <ul>
                <a href="#" v-on:click="home"><img src="static/img/logo.png"/></a>
                <router-link class="link" v-if="!bruker.username" to="/loggInn">Logg inn</router-link>
                <a class="link" v-on:click="logout" v-if="bruker.username" href="#">Logg ut</a>
                <router-link class="link" v-if="bruker.role=='user'" to="/minSide">Min side</router-link>
                <router-link class="link" v-if="bruker.role=='admin'" to="/styret">For styret</router-link>
                <router-link class="link" to="/bedrift">Bedrifter</router-link>
                <router-link class="link" to="/studenter">For studenter</router-link>
                <router-link class="link" to="/">Om LED</router-link>
            </ul>
        </nav>
    </header>
    `,
    methods: {
        logout: function(){
            this.$parent.logout();
        },
        home: function(){
            router.push("/")
        }
    }
};