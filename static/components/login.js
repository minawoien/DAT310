let loginC = {
    props: ["bruker"],
    template: /*html*/`
    <div class="pages center">
        <div class="login" v-if="!display">
            <h1>Logg inn</h1>
            <form action="#" method="POST" v-on:submit="tryLogin" autocomplete="off">
                <input type="text" name="username" v-model="username" placeholder="Brukernavn" /><br />
                <input type="password" name="password" v-model="password"  placeholder="Password" /><br />
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
                <input type="mail" name="mail" v-model="mail" placeholder="Mail" required/><br />
                <input type="text" name="address" v-model="address" placeholder="Adresse" required/><br />
                <input type="number" name="phone" v-model="phone" placeholder="Telfon" required/><br />
                <input type="text" name="filename" v-model="filename" placeholder="Filnavn" required/><br />
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
            filename: null,
            regUsername: null,
            regPassword: null,
            valPassword: null,
            text: null,
            loginText: null,
            display: false
        }
    },
    methods: {
        tryLogin: async function(event){
            event.preventDefault();
            let request = await fetch("/login",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({username: this.username, password: this.password})
            });
            if (request.status == 200){
                let result = await request.json();
                if (result["userid"]){
                    if (result["role"] == "admin"){
                        this.$root.user=result;
                        console.log(result)
                        router.push("/styret")
                    }else{
                        this.$root.user=result;
                        router.push("/minSide")
                    }
                }
                this.loginText = result
            }
            
        },
        register: async function(event){
            event.preventDefault();
            let request = await fetch("/register",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({Bedriftnavn: this.name, Mail: this.mail, Adresse: this.address, Telefon: this.phone, Filnavn: "/static/img"+this.filename, Brukernavn: this.regUsername, Passord: this.regPassword, SjekkPassord: this.valPassword})
            });
            if (request.status == 200){
                let result = await request.json();
                if (result == "Sucess"){
                    this.display = !this.display
                    this.name = this.mail =  this.address = this.phone = this.filename = this.regUsername = this.regPassword = this.valPassword = null;
                }else{
                    this.text = result;
                }

            }
        },
        showReg: function(){
            this.display=!this.display;
        }
    }
};