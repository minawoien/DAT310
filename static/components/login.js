let loginC = {
    props: ["bruker"],
    template: /*html*/`
    <div class="pages center">
        <div class="login" v-if="!display">
            <h1>Logg inn</h1>
            <form action="#" method="POST" v-on:submit="tryLogin" autocomplete="off">
                <input type="text" name="username" v-model="username" placeholder="Brukernavn" required/><br />
                <input type="password" name="password" v-model="password"  placeholder="Password" required/><br />
                <input type="submit" value="Logg Inn" />
                <p>{{loginText}}</p>
                <div id="or"></div>
                <button v-on:click="showReg">Opprett konto for bedrift</button>
            </form>
        </div>
        <div class="login" v-if="display">
            <span class="removeIcon" v-on:click="showReg" ></span>
            <h1>Register bedrift</h1>
            <form action="#" method="POST" v-on:submit="register" autocomplete="off">
                <input type="text" name="name" v-model="name" placeholder="Bedriftnavn" required/><br />
                <input type="email" name="mail" v-model="mail" placeholder="Mail" required/><br />
                <input type="text" name="address" v-model="address" placeholder="Adresse" required/><br />
                <input type="number" name="phone" v-model="phone" placeholder="Telefon" min="0" max="99999999" required/><br />
                <input type="text" name="regUsername" v-model="regUsername" placeholder="Brukernavn" required/><br />
                <input type="password" name="regPassword" v-model="regPassword" placeholder="Passord" required><br />
                <input type="password" name="valPassword" v-model="valPassword" placeholder="Passord" required><br />
                <input type="submit" value="Registrer">
                <p>{{text}}</p>
            </form>
        </div>
    </div>
    `,
    data: function(){
        return{
            username: null,
            password: null,
            name: null,
            mail: null,
            address: null,
            phone: null,
            regUsername: null,
            regPassword: null,
            valPassword: null,
            text: null,
            loginText: null,
            display: false
        }
    },
    // Hvis det er en innlogget bruker blir brukeren sendt til /404
    created: async function(){
        let response = await fetch('/userdata');
        if (response.status == 200){
            let result = await response.json();
            if (result["userid"]){
                router.push("/404")
            }
        }
    },
    methods: {
        // Funksjon for login
        tryLogin: async function(event){
            event.preventDefault();
            let request = await fetch("/login",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({username: this.username, password: this.password})
            });
            // Ved suksessfull innlogging sjekkes rollen til brukeren, og admin blir sendt til /stryet og vanlige brukere blir 
            // sendt til /minSide. Ved feilet innlogging vises feilmeldig.
            if (request.status == 200){
                let result = await request.json();
                if (result["userid"]){
                    if (result["role"] == "admin"){
                        this.$root.user=result;
                        router.push("/styret")
                    }else{
                        this.$root.user=result;
                        router.push("/minSide")
                    }
                }
                this.loginText = result
            }
        },
        // Funksjon for registrering
        register: async function(event){
            event.preventDefault();
            let request = await fetch("/register",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({Bedriftnavn: this.name, Mail: this.mail, Adresse: this.address, Telefon: this.phone, Brukernavn: this.regUsername, Passord: this.regPassword, SjekkPassord: this.valPassword})
            });
            // Ved suksessfull registrering blir registreringsfeltet skjult og brukeren kan logge inn. Ved feilet registrering eller
            // ugyldig brukerinput vises feilmledig
            if (request.status == 200){
                let result = await request.json();
                if (result == "Sucess"){
                    this.showReg();
                }else{
                    this.text = result;
                }
            }
        },
        showReg: function(){
            this.display=!this.display;
            this.name = this.mail =  this.address = this.phone = this.filename = this.regUsername = this.regPassword = this.valPassword = null;
        }
    }
};