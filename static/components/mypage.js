let mypageC = {
    props: ["bruker"],
    template: /*html*/`
    <div class="pages content">
        <div class="publish">
            <h2>Legg ut en stillingsannonse</h2>
            <p>Informasjon om bedriften er lagret, og trenger ikke legges inn.</p>
            <form action="#" method="POST"  v-on:submit="sendAnnonse" autocomplete="off">
                <select v-model="type" required>
                    <option disabled value="">Velg stillingstype</option>
                    <option value="Heltid">Heltid</option>
                    <option value="Deltid">Deltid</option>
                    <option value="Sommerjobb">Sommerjobb</option>
                </select><br /> 
                <input type="text" name="place" v-model="place" placeholder="Sted" required /><br />
                <input type="text" name="date" v-model="date" placeholder="Søknadsfrist" required /><br />
                <input type="text" name="link" v-model="link" placeholder="Lenke"><br />
                <textarea id="desc" name="text" v-model="text" placeholder="Beskrivelse" required></textarea><br />
                <input type="submit" value="send">
                <p>{{validateTxt}}</p>
            </form>
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
                <input type="mail" name="mail" v-model="mail" :placeholder="comp.mail"/><br />
                <input type="text" name="filename" v-model="filename" :placeholder="comp.filename"/><br />
                <input type="submit" value="Ok"/>
                <p>{{editText}}</p>
            </form>

            <div id="deal">
                <h1>Mine avtaler</h1>
                <br>
                <div v-for="deal in avtaler">
                    <h3>{{deal.type}} {{deal.prosent}}</h3>
                    <p>{{deal.start_date}} - {{deal.end_date}}</p>
                    <br>
                </div>
            </div>
        </div>
    </div>
    `,
    data: function(){
        return{
            type: "",
            place: null,
            date: null,
            link: null,
            text: null,
            comp: [],
            avtaler: null,
            file: null,
            name: null,
            mail: null,
            address: null,
            phone: null,
            filename: null,
            display: false,
            validateTxt: null,
            editText: null
        }
    },
    created: async function(){
        await this.getBed();
        this.getDeals();
        this.name = this.comp.name
        this.mail = this.comp.mail,
        this.address = this.comp.address,
        this.phone = this.comp.phone_numb
    
    },
    watch: {
        comp: function(val){
            let list = this.comp.filename.split("/")
            this.filename = list[list.length-1]
            console.log(this.filename)
        }
    },
    methods: {
        getBed: async function(){
            let response = await fetch('/bedrift');
            if (response.status == 200){
                let result = await response.json();
                console.log(result)
                this.comp = result;
            }
        },
        getDeals: async function(){
            console.log(this.comp.bid)
            let request = await fetch('/avtaler?bid='+this.comp.bid);
            if (request.status == 200){
                let result = await request.json();
                this.avtaler = result
                this.getProsent();
            }
        },
        sendAnnonse: async function(event){
            event.preventDefault();
            console.log(this.type)
            let request = await fetch("/innlegg",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({type: this.type, Sted: this.place, Dato: this.date, Lenke: this.link, Beskrivelse: this.text, Tittel:null})
            });
            if (request.status == 200){
                result = await request.json();
                if (result == "Success"){
                    router.push("/studenter")
                }else{
                    this.validateTxt = result;
                }
                
            }
        },
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
        },
        edit: async function(event){
            event.preventDefault();
            let request = await fetch("/editInfo",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({bid: this.comp.bid, Navn: this.name, Mail: this.mail, Adresse: this.address, Telefon: this.phone, Filnavn: "static/img/"+this.filename})
            });
            if (request.status == 200){
                let result = await request.json();
                if (result == "Sucess"){
                    this.display = !this.display
                    this.getBed();
                }else{
                    this.editText = result;
                }
            }
        }
    }
};