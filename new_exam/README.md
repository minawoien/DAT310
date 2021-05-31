For å kjøre nettsiden: 
- Kjør setup_db.py
- Kjør app.py

Admin login:
Brukernavn: 256461
Passord: 123

Bedrift login:
Brukernavn: kongsberg
Passord: 1234

Brukerinput:
- All brukerinput blir sjekket i en funksjon
- Spesialtegn er ikke tillatt og alle felt må ha mer enn tre tegn
- Viser feilmelding

Login:
- Kan registrere bruker som bedrift
- Logge inn som bedrift / admin
- Passord må være minst 8 tegn ved registrering, det må fylles inn to ganger og de må være like. Vises feilmelding.
- Brukernavnet kan ikke være tatt. Vises feilmelding.
- Ved innlogging vises feilmelding dersom brukernavnet ikke eksisterer eller passordet er feil.
- Ved oppdatering av siden sjekkes det om det er en innlogget bruker. Forblir pålogget til brukeren er logget ut.
- Blir sendt til "Min side" eller "For styret", avhengig om det er en admin eller vanlig bruker.
- En admin har ikke tilgang til "Min side" og bedriftbrukere har ikke tilgang til "For styret".
- Innloggede brukere har ikke tilgang til login-siden

Logout:
- Når brukeren logges ut sjules "Min side" eller "For styret" fra menyen.
- Session med brukernavn og rolle blir slettet.
- Blir sendt til "Hjem"
- Filtrerings cookies blir slettet

Bedrift - side:
- Bildene til bedrift brukerene som har enten samarbeidsavtale eller bedriftspersentasjon blir lagt til på denne siden, og sortert ut i fra type avtale.

For studenter - side:
- Innlegg som admin kan publisere på "admin-side" blir publisert under Innlegg
- Stillingsannonser som bedrifter kan publisere på "myPage" blir publisert under Stillingsannonser.
- Ved å trykke på søk-ikonet kan man filtrere stillingsannonser
- Kan filtrere stillingsannonsene på søk i tekst, bedriftnavn og stillingstype.
- Filtreringen blir lagret i en cookie, som slettes når en bruker logger ut, ellers er den satt permanent.
- Admin kan slette innlegg og stillingsannonser
- Innlegg sorteres etter nyeste publiseringsdato øverst

MyPage - side:
- Side for bedrifter, kommer opp i menyen dersom det er en innlogget bedrift
- Kan legge ut stillingsannonser som publiseres på "For studenter"
- Bedriftsnavn blir lagt til i annonsen uten å måtte fylles inn
- Alle feltene, uten om lenke, må fylles ut. Brukerinput blir sjekket - viser feilmelding.
- Bedrifts informasjon vises på siden. 
- Ved å trykke på redigerings-ikonet kan brukeren redigere bedriftsinformasjon og laste opp et bilde.
- Bildet blir lagret som en fil med bedriftens id, og pathen lagres i databasen.
- Alle feltene blir sjekket, men må ikke endres. Brukerinput blir sjekket - viser feilmelding.
- Viser avtalene med LED og ISI, startdato og sluttdato. Prosent for hvor lenge avtalen er vart vises ut i fra dagens dato, startdato og sluttdato.

Amdin - side
- Side for admin, kommer opp i menyen dersom det er en innlogget amdin. Kun admin kan se innholdet på denne siden
- Kan legge ut innlegg som publiseres på "For studenter"
- Navn, dagens dato og styretittel blir lagt til uten å måtte fylles inn
- Alle feltene, uten om lenke, må fylles ut. Brukerinput blir sjekket - viser feilmelding.
- Viser avtaler med bedrifer, med navn, pris og datoer.

Feilmeldinger og status fra setub_db.py blir lagt til i filen log.txt.

Fargepallett:
#049893
#075564
#dfe2e4
#74d2cc
#60a2a7
