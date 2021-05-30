let mypageC = {
    props: ["bruker"],
    template: /*html*/`
    <div class="pages content">
        <div class="publish">
            <h2>Legg ut en stillingsannonse</h2>
            <p>Informasjon om bedriften er lagret, og trenger ikke legges inn.</p>
            <publish-annonse></publish-annonse>
        </div>
        <div class="right">
            <div class="bedInfo" v-if="!display">
                <span class="editIcon" v-on:click="showEdit"></span>
                <img :src="comp.filename" />
                <h3>{{comp.name}}</h3>
                <p>{{comp.phone_numb}}</p>
                <p>{{comp.address}}</p>
                <p>{{comp.mail}}</p>
            </div>
            <form action="#" method="POST"  v-on:submit="edit" v-if="display" class="bedInfo" autocomplete="off">
                <input type="text" name="name" v-model="name" :placeholder="comp.name"/><br />
                <input type="number" name="phone" v-model="phone" :placeholder="comp.phone_numb"/><br />
                <input type="text" name="address" v-model="address" :placeholder="comp.address"/><br />
                <input type="email" name="mail" v-model="mail" :placeholder="comp.mail"/><br />
                <input type="file" @change="onFileSelected"/>
                <p class="error">{{text}}</p>
                <input type="submit" value="Ok"/>
                <p class="error">{{editText}}</p>
            </form>
            <div v-if="avtaler!=null" id="deal">
                <h1>Mine avtaler</h1>
                <div class="deals">
                    <div v-for="deal in avtaler">
                        <h3>{{deal.type}} {{deal.prosent}}</h3>
                        <p>{{deal.start_date}} - {{deal.end_date}}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    data: function(){
        return{
            comp: [],
            avtaler: null,
            file: null,
            name: null,
            mail: null,
            address: null,
            phone: null,
            display: false,
            editText: null,
            selectedFile: '',
            text: null
        }
    },
    // Henter bedrift og avtaler. Avtalene blir hentet etter bedriften er ferdig lastet, da avtalene blir hentet ut i fra
    // bedriftens id
    created: async function(){
        await this.getBed();
        this.getDeals();
        this.name = this.comp.name
        this.mail = this.comp.mail,
        this.address = this.comp.address,
        this.phone = this.comp.phone_numb
    },
    methods: {
        // Henter bedriftinformasjon. Hvis det ikke er en innlogget bedrift blir brukeren sendt til /404
        getBed: async function(){
            let response = await fetch('/bedrift');
            if (response.status == 200){
                let result = await response.json();
                this.comp = result;
                if (this.comp.bid == null){
                    router.push("/404")
                }
                // Bedriftene kan laste opp bilde når de redigerer bedriftsinformasjon. Etter de har laget en bruker vil
                // filnavnet være null, og et edit-bilde blir satt som default til brukeren laster opp et eget bilde.
                if (this.comp.filename == null){
                    this.comp.filename = "/static/img/edit.png"
                }
            }
        },
        // Henter avtalene til bedriften, hvis de ikke har noen avtaler med LED eller ISI vil ikke boksen være synlig
        getDeals: async function(){
            let request = await fetch('/avtaler?bid='+this.comp.bid);
            if (request.status == 200){
                let result = await request.json();
                this.avtaler = result
                if (this.avtaler.length == 0){
                    this.avtaler = null
                }else {
                    this.getProsent();
                }
            }
        },
        // Regner prosenten for hvor langt hver avtale har kommet ut i fra dagens dato, startdato og sluttdato
        getProsent: function(){
            for (i in this.avtaler){
                s = this.avtaler[i].start_date.split(".")
                e = this.avtaler[i].end_date.split(".")
                let start = new Date(s[2], s[1], s[0]), 
                end = new Date(e[2], e[1], e[0]), 
                today = new Date() 
                this.avtaler[i].prosent = ( Math.round(((today - start) / (end - start)) * 100) + '%');
            }
        },
        showEdit: function(){
            this.display = !this.display
            this.text = null
        },
        // Funkjson som sender inn den redigerte infoen, hvis ikke alle feltene er endret vil de gamle verdiene bli sendt inn 
        // med de nye.
        edit: async function(event){
            event.preventDefault();
            let request = await fetch("/editInfo",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({bid: this.comp.bid, Navn: this.name, Mail: this.mail, Adresse: this.address, Telefon: this.phone})
            });
            // Hvis brukerinputen er ugyldig vises det en feilmelding, men hvis det var velykket, kalles getBed funksjoen
            // for å oppdatere informasjonen som vises.
            if (request.status == 200){
                let result = await request.json();
                if (result == "Sucess"){
                    this.display = !this.display
                    this.getBed();
                }else{
                    this.editText = result;
                }
            }
        },
        // Bildet blir lastet opp med en gang det er valgt (onchange-funksjon)
        // Bruker formdata for å sende bildet
        onFileSelected(event){
            this.selectedFile = event.target.files[0]
            const formData = new FormData();
            formData.append('image', this.selectedFile, this.selectedFile.name);
            fetch("/uploadImg", {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            // Hvis filoplastningen feiles vises en feilmelding, men hvis den var velykket kalles getBed funksjoen
            // for å oppdatere informasjonen som vises. (Bildet vil bli opplastet hvis brukeren velger et bilde, men ikke 
            // trykker på ok knappen - den er for å endre bedriftsinformajsonen)
            .then(result => {
                if (result == ""){
                    this.text = "Opplastning feilet, prøv igjen!"
                }else{
                    this.getBed();
                }
            })
        }   
    }
};