
const routes = [
    { path: '/', component: mainC},
    { path: '/studenter', component: studentC},
    { path: '/bedrift', component: companyC},
    { path: '/minSide', component: mypageC},
    { path: '/logginn', component: loginC},
    { path: '/styret', component: adminC},
];


const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes: routes
});


let app = Vue.createApp({
    data: function(){
        return {
            user: {
                "userid": null,
                "username": null,
                "role": null
            }
        }
    },
    created: async function(){
        let response = await fetch('/userdata');
        if (response.status == 200){
            let result = await response.json();
            if (result.userid){
                this.user = result;
            }
        }
    },
    methods: {
        logout: async function(){
            let response = await fetch('/logout');
            if (response.status == 200){
                this.user = {
                            "userid": null,
                            "username": null,
                            "role": null
                            };
                router.push("/")
            }
        }
    }
});
app.use(router);
app.component("main-page", mainC);
app.component("student-page", studentC);
app.component("company-page", companyC);
app.component("my-page", mypageC);
app.component("login-page", loginC);
app.component("admin-page", adminC);
app.component("annonse", annonseC);
app.component("innlegg", innleggC);
app.component("top-menu", menuC);
app.component("footerbox", footerC);
app.mount('#app');
