NB. work in progress.

Project Goto er en "sublime project manager" som gir utviklere kjappe snarveger for å bare gå dit en trenger, akkurat nå. Man bruker goto fra terminalen(alle os), fra spotlight (osx) eller fra slick-run (windows).

For eksempel:

```
    goto visualstudio  -->  åpner solution for det aktive prosjektet i visual studio
    goto jira          -->  åpner jira boardet for det aktive prosjektet
    goto bitbucket     -->  bitbucket for prosjektet.
```
 

#### Hvordan vet Goto hvilket prosjekt som er aktivt?

Du forteller det med kommandoen:  project <project-name>

Eksempler: project sylvsmidja  | project bankid  |  project fjordtours


#### Hvordan vet Goto om hvilke prosjekter som finnes?

Du forteller det med kommandoen:

     project add <project-name>

 
#### Hvordan vet Goto om hvilke snarveger som finnes i  prosjektet?

Du definerer dem en gang, og bruker dem 1000 ganger deretter.  Dette med kommandoen:

     goto add <magic-word> <URI>

Når et prosjekt er aktivt, husker goto hvilket prosjekt du tenker på akkurat nå. Dermed gir det mening å kalle snarvegen for visualstudio, for det da implsitt betyr at det er snakk om solutionen for dette prosjektet. F.eks sylvsmidja.

Eksempler:

    goto add jira http://jira.com/project/X

Full kommando dersom man vil være spesifikk:

     goto add [-p <project-name>] <magic-word> <URI>


## Setup (OS-X)

```
git clone https://github.com/technocake/goto /usr/local/opt/goto
bash /usr/local/opt/goto/install_goto.sh
```



Now you can test it. No need to close the terminal.

```
goto goto
```
