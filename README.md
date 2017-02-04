# paris-immo-finder

Un bot Slack extensible pour chercher des appartements en vente sur Paris selon ses propres critères

# Deploiement
Le bot se deploi sur Heroku avec le Standard Scheduler.
clock.py est le point d'entrée à appeler.

Tout est configurable via des variables d'environement, le token Slack comme les paramètres de recherche.

# Sources supportées

Actuellement les sources suivantes sont supportées:
* Agences Saint Ferdinand
* Bien Ici
* PAP
* Se Loger

De nouvelles sources peuvent être ajoutées facilement en étandant la classe BaseDataSource puis en ajoutant l'appel à cette dernière dans clock.py

# Améliorons le bot !
Si vous souhaitez vous en servir, pas de problème. N'hésitez pas à apporter de modifications au bot et à les soumettre via une pull request, je me ferai un plaisir de les merger.


En revanche je n'ai pas de plans de développer moi même de nouvelles fonctionnalités sur ce bot pour le moment.
