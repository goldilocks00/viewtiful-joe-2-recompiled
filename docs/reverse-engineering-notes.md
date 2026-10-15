# Notes d’analyse — G2VP08 révision 0

## Avertissements SMC

La sortie de DolRecomp contient 147 plages couvrant 173 instructions candidates : une invalidation du cache d’instructions (`icbi`) et 172 autres candidats d’écriture. Ce comptage porte sur les instructions signalées, pas sur des modifications observées à l’exécution.

Exemple concret à surveiller : l’instruction située à `0x80258EEC` écrit vers `0x80258FD0`, adresse située dans la seconde section texte. Il faut déterminer si la destination est une donnée intégrée à la section texte ou du code réellement exécuté avant de proposer un correctif.

Le cœur StaticRecomp vérifie les fragments et peut se replier sur l’interpréteur/JIT lorsqu’ils diffèrent. Les compteurs SMC et les adresses des fragments concernés guideront la suite. Aucun patch visant à ignorer une différence n’est appliqué.

## Chargement dynamique

Le DOL contient un diagnostic OSLink, mais la FST ne contient pas de REL explicite. La présence de cette chaîne ne suffit pas à prouver une utilisation du chargeur. L’analyse des appels et des archives internes reste à effectuer si les traces indiquent du code absent du module.
