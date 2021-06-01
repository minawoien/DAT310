let publishC = {
    template: /*html*/`
    <form action="#" method="POST"  v-on:submit="sendAnnonse" autocomplete="off">
        <select v-model="type" required>
            <option disabled value="">Velg stillingstype</option>
            <option value="Heltid">Heltid</option>
            <option value="Deltid">Deltid</option>
            <option value="Sommerjobb">Sommerjobb</option>
        </select><br /> 
        <input type="text" name="place" v-model="place" placeholder="Sted" required /><br />
        <input type="date" name="date" v-model="date" placeholder="Søknadsfrist" required /><br />
        <input type="text" name="link" v-model="link" placeholder="https://www.example.com"><br />
        <textarea id="desc" name="text" v-model="text" placeholder="Beskrivelse" required></textarea><br />
        <input type="submit" value="send">
        <p>{{validateTxt}}</p>
    </form>
`,
    data: function(){
        return {
            type: "",
            place: null,
            date: null,
            link: null,
            text: null,
            validateTxt: null
        }
    },
    methods: {
        // Lager en annonse
        sendAnnonse: async function(event){
            event.preventDefault();
            let request = await fetch("/innlegg",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({type: this.type, Sted: this.place, Dato: this.date, Lenke: this.link, Beskrivelse: this.text, Tittel:null})
            });
            // Hvis brukerinput var godkjent blir brukeren sendt til /studenter hvor annonsen blir publisert. Hvis det ikke er 
            // godkjent vises feilmeldingen.
            if (request.status == 200){
                result = await request.json();
                if (result == "Success"){
                    router.push("/studenter")
                }else{
                    this.validateTxt = result;
                }
                
            }
        },
    }
};