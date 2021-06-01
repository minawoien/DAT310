let adminC = {
    props: ["bruker"],
    template: /*html*/`
    <div class="tittel">
        <h1>Velkommen {{styret.firstname}}!</h1>
        <p>Kun styret kan se denne siden!</p>
    </div>
    <div class="pages content">
        <div class="publish">
            <h2>Legg ut et innlegg</h2>
            <p>Innlegget vil bli publisert under "For studenter"!</p>
            <form action="#" method="POST" v-on:submit="sendAnnonse" autocomplete="off">
                <input type="text" name="title" v-model="title" placeholder="Tittel" required /><br />
                <input type="text" name="link" v-model="link" placeholder="Lenke"><br />
                <textarea id="desc" name="text" v-model="text" placeholder="Beskrivelse" required ></textarea><br />
                <input type="submit" value="send">
                <p>{{validateTxt}}</p>
            </form>
        </div>
        <div class="adminDeal post">
            <h1>LED avtaler</h1>
            <div v-for="deal in avtaler">
                <h4>{{deal.type}} - {{deal.bid["name"]}}</h4>
                <p>Med {{deal.owner}}.</p>
                <p>Avtalt pris: {{deal.price}}</p>
                <p>{{deal.start_date}} - {{deal.end_date}}</p>
                <br>
            </div>
        </div>
    </div>
    `,
    data: function(){
        return{
            title: null,
            link: null,
            text: null,
            styret: [],
            avtaler: null,
            validateTxt: null
        }
    },
    created: async function(){
        let response = await fetch('/admin');
        if (response.status == 200){
            let result = await response.json();
            if (result){
                this.styret = result;
            }else{
                router.push("/")
            }
        }
        let request = await fetch('/alleAvtaler');
        if (request.status == 200){
            let result = await request.json();
            this.avtaler = result
        }

    },
    methods: {
        sendAnnonse: async function(event){
            event.preventDefault();
            var currentDateWithFormat = new Date().toJSON().slice(0,10).replace(/-/g,'/');
            let request = await fetch("/innlegg",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({Lenke: this.link, Beskrivelse: this.text, type: "innlegg", Dato: currentDateWithFormat, Sted: null, Tittel:this.title})
            });
            if (request.status == 200){
                result = await request.json();
                if (result == "Success"){
                    router.push("/studenter")
                }else{
                    this.validateTxt = result;
                }
                
            }
            // Videreføre til student for å se stillingsannonsen?
        }
    },
};