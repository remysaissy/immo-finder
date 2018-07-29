# paris-immo-finder

Un bot Slack extensible pour chercher des appartements en vente sur Paris selon ses propres critères

# Deploiement
Le bot se deploit sur Heroku avec le Standard Scheduler.
clock.py est le point d'entrée à appeler.

Tout est configurable via des variables d'environement, le token Slack comme les paramètres de recherche.

heroku stack:set cedar-14
heroku buildpacks:add https://github.com/stomita/heroku-buildpack-phantomjs
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver.git
heroku addons:add heroku-postgresql
heroku addons:create scheduler:standard
heroku addons:open scheduler
 --> python clock.py -- hourly run
 
 
 On your local machine:
* brew install phantomjs
* brew cask install chromedriver

# Sources supportées

Actuellement les sources suivantes sont supportées:
* Bien Ici
* PAP
* Se Loger

De nouvelles sources peuvent être ajoutées facilement en étandant la classe BaseDataSource puis en ajoutant l'appel à cette dernière dans clock.py

# Paramètres

* DISTRICTS: code postaux des arrondissements à surveiller
* BLACKLISTED_WORDS: Mots clés dans le titre ou le texte de l'annonce donnant lieu à son exclusion
* MIN_PRICE: Prix minimal recherché
* MAX_PRICE: Prix maximal recherché
* MIN_PRICE_PER_SURFACE_UNIT: Prix minimal par m2
* MIN_SIZE: Taille minimale recherchée
* MAX_BUILDING_YEAR: Année maximale de construction de l'immeuble
* SLEEP_INTERVAL: Interval de passage du clock.py - A configurer sur la même valeur que l'intervalle de scheduler dans Heroku
* DATABASE_URL: URL de la base de données
* SLACK_CHANNEL: Nom du channel Slack à utiliser pour envoyer les notifications
* SLACK_BOT_TOKEN: Token Slack pour le bot
* SLACK_BOT_NAME: Nom du bot
* SLACK_BOT_ICON: Icône du bot
* PAP_DEVICE_GSF: Identifiant de device PAP. A récupérer en utilisant un proxy entre PAP sur mobile et internet. Sans cet entête HTTP, PAP ne pourra pas être scrapé

# Améliorons le bot !
Si vous souhaitez vous en servir, pas de problème. N'hésitez pas à apporter de modifications au bot et à les soumettre via une pull request, je me ferai un plaisir de les merger.


En revanche je n'ai pas de plans de développer moi même de nouvelles fonctionnalités sur ce bot pour le moment.
