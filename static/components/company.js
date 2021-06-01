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
        let request = await fetch('/alleAvtaler');
        if (request.status == 200){
            let result = await request.json();
            for (deal in result){
                if (result[deal].type=="Samarbeidsavtale"){
                    this.samarbeid.push(result[deal])
                }else{
                    this.presentasjon.push(result[deal])
                }
            }
        }
    }
};