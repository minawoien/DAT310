Databasen er inkludert i zip-fil, men ikke på github

# For å kjøre nettsiden:
- Kjør app.py

# Lagde brukere 
- Admin login:
    Brukernavn: 256461
    Passord: 123

    Brukernavn: 253467
    Passord: 123

- Bedrift login:
    Brukernavn: kongsberg
    Passord: 1234

    Brukernavn: sopra
    Passord: 123


# Sider
Login - side:
* Login:
- Logge inn som bedrift / admin
- Alle feltene må være fylt inn. 
- Ved innlogging vises feilmelding dersom brukernavnet ikke eksisterer eller passordet er feil.
- Ved oppdatering av siden sjekkes det om det er en innlogget bruker.
    - Innloggede brukere har ikke tilgang til login-siden
    - Sender brukeren til /404 hvis det er en innlogget bruker
    - Forblir pålogget til brukeren er logget ut.
- Blir sendt til "Min side" eller "For styret", avhengig om det er en admin eller vanlig bruker.
    - En admin har ikke tilgang til "Min side" og bedriftbrukere har ikke tilgang til "For styret".
    - Blir da sendt til /404

* Registering:
- Kan registrere bruker som bedrift
- Alle feltene må være fylt inn med minst 3 tegn (uten spesialtegn). 
- Passord må være minst 8 tegn ved registrering, det må fylles inn to ganger og de må være like. Vises feilmelding.
- Brukernavnet kan ikke være tatt. Vises feilmelding.
- Innloggede brukere har ikke tilgang til registrering
    - Sender brukeren til /404

Bedrift - side:
- Bildene til bedrift brukerene som har enten samarbeidsavtale eller bedriftspersentasjon blir lagt til på denne siden, og sortert ut i fra type avtale.
- Avtalene kan kun bli lagd i setup_db.py

For studenter - side:
- Innlegg som admin kan publisere på "admin-side" blir publisert under Innlegg
- Stillingsannonser som bedrifter kan publisere på "myPage" blir publisert under Stillingsannonser.
- Ved å trykke på søk-ikonet kan man filtrere stillingsannonser
    - Kan filtrere stillingsannonsene på søk i tekst, bedriftnavn og stillingstype.
    - Filtreringen blir lagret i en cookie, som slettes når en bruker logger ut, ellers er den satt permanent.
- Admin kan slette innlegg og stillingsannonser
- Innlegg sorteres etter nyeste publiseringsdato øverst
- Stillingsannonser sorteres etter seneste søknadsfrist øverst

MyPage - side:
- Side for bedrifter, kommer opp i menyen dersom det er en innlogget bedrift
- Kan legge ut stillingsannonser som publiseres på "For studenter"-siden
    - Bedriftsnavn blir lagt til i annonsen uten å måtte fylles inn
    - Alle feltene, uten om lenke, må fylles ut. Brukerinput blir sjekket - viser feilmelding.
- Bedrifts informasjon vises på siden. 
- Ved å trykke på redigerings-ikonet kan brukeren redigere bedriftsinformasjon og laste opp et bilde.
    - Bildet blir lagret som en fil med filnavn som orginalt filnavn og bedriftens id, og pathen lagres i databasen. Kun 'jpg', 'jpeg' og 'png' filer blir akseptert.
    - Hvis brukeren ikke har lastet opp et bilde vises et "last opp"-bilde som default
    - Alle feltene blir sjekket ved redigering, men må ikke endres. Brukerinput blir sjekket - viser feilmelding.
- Viser avtalene med LED og ISI, startdato og sluttdato. Prosent for hvor lenge avtalen er vart vises ut i fra dagens dato, startdato og sluttdato.

Amdin - side
- Side for admin, kommer opp i menyen dersom det er en innlogget amdin. Kun admin kan se innholdet på denne siden
- Kan legge ut innlegg som publiseres på "For studenter"-siden
    - Navn, dagens dato og styretittel blir lagt til uten å måtte fylles inn
    - Alle feltene, uten om lenke, må fylles ut. Brukerinput blir sjekket - viser feilmelding.
- Viser avtaler med bedrifer, med navn, pris og datoer.

Logout:
- Når brukeren logges ut sjules "Min side" eller "For styret" fra menyen. Session med brukernavn og rolle blir slettet.
- Blir sendt til "Hjem"
- Filtrerings cookies blir slettet


# Brukerinput:
- All brukerinput blir sjekket i en funksjon
- Spesialtegn er ikke tillatt og alle felt må ha mer enn tre tegn
- Viser feilmelding


# Brukere
Adminbruker:
- Tilgang til "For styret"
- Se alle avtaler
- Legge ut innlegg som kommer på student-siden
- Slette innlegg og stillingsutlysninger
- Se stillingsanonnser og filtrere de
- Se innlegg

Med bedriftsbruker:
- Tilgang til "Min side"
- Lage bruker
- Se avtaler med LED
- Legge ut stillingsannonser som kommer på student-siden
- Endre bedriftsinformasjon
- Laste opp bilde
- Se stillingsanonnser og filtrere de
- Se innlegg

Uten bruker:
- Se stillingsanonnser og filtrere de
- Se innlegg
- Lage bedriftbruker


# I databasen som blir lagd når setup_db.py kjøres og databasen blir lagd (Trenger ikke kjøres)
- Fire brukere
- To adminbrukere med et innlegg hver
- To bedrifter med en stillingsannonse hver
- Sopra Steria bedriften har et opplastet bilde. Kongsberg Digital har ikke et lastet opp bilde
- En bedriftspresentasjon-avtale med Kongsberg Digital
- En samarbeidsavtale med Kongsberg Digital og en med Sopra Steria

Feilmeldinger og status fra setub_db.py blir lagt til i filen log.txt.

# Fargepallett:
#049893
#075564
#dfe2e4
#74d2cc
#60a2a7
