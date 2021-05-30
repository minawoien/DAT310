let companyC = {
    props: ["bruker"],
    template: /*html*/`
    <div id="comp">
        <h1>SAMARBEIDSPARTNERE</h1>
        <div class="companyP center">
            <div class="image" v-for="deal in samarbeid">
                <img :src="deal.bid['filename']"/>
            </div>
        </div>
        <h1>BEDRIFTSPRESENTASJONER</h1>
        <div class="companyP center">
            <div class="image" v-for="deal in presentasjon">
                <img :src="deal.bid['filename']"/>
            </div>
        </div>
    </div>

    `,
    data: function(){
        return{
            samarbeid: [],
            presentasjon: []
        }
    },
    created: async function(){
        // Henter bedrifter som har avtaler med LED. Sorterer de etter om de har enten samarbeidsavtale eller
        // bedriftspresentasjon ved å sjekke avtale-typen og putte de i forskjellige lister.
        // Bedrifter som ikke har lastet opp bilde får et default-bilde.
        let request = await fetch('/alleAvtaler');
        if (request.status == 200){
            let result = await request.json();
            for (deal in result){
                if (result[deal].type=="Samarbeidsavtale"){
                    this.samarbeid.push(result[deal])
                }else{
                    this.presentasjon.push(result[deal])
                }
                if (result[deal].bid["filename"] == null){
                    result[deal].bid["filename"] = "/static/img/noImg.png"
                }
            }
        }
    }
};