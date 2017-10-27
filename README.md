NB. work in progress.

Project Goto er en "sublime project manager" som gir utviklere kjappe snarveger for å bare gå dit en trenger, akkurat nå. Man bruker goto fra terminalen(alle os), fra spotlight (osx) eller fra slick-run (windows).

For eksempel:

    goto visualstudio --> åpner solution for det aktive prosjektet i visual studio
    goto jira --> åpner jira boardet for det aktive prosjektet
    goto bitbucket --> bitbucket for prosjektet.

 

Hvordan vet Goto hvilket prosjekt som er aktivt?

Du forteller det med kommandoen:  project <project-name>

Eksempler: project sylvsmidja  | project bankid  |  project fjordtours

 

Hvordan vet Goto om hvilke prosjekter som finnes?

Du forteller det med kommandoen:

     project add <project-name> <path-to-project-dir>

 

Hvordan vet Goto om hvilke snarveger som finnes i  prosjektet?

Du definerer dem en gang, og bruker dem 1000 ganger deretter.  Dette med kommandoen:

     goto add <magic-word> <URI>

Når et prosjekt er aktivt, husker goto hvilket prosjekt du tenker på akkurat nå. Dermed gir det mening å kalle snarvegen for jira, for det da implsitt betyr at det er snakk om jira for dette prosjektet. F.eks sylvsmidja.

Eksempler:

    goto add jira http://jira.com/project/X

Full kommando dersom man vil være spesifikk:

     goto add [-p <project-name>] <magic-word> <URI>


## Setup (OS-X)

```
cd /usr/local/opt
git clone https://github.com/technocake/goto
# add goto | project commands to the terminal
ln -s /usr/local/opt/goto/bin/* /usr/local/bin/
```
