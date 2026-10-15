# Points à vérifier

- Le CISO possède 576 octets après ses blocs déclarés. Ils sont conservés et inclus dans son empreinte ; leur rôle n’est pas identifié.
- DolRecomp signale 147 plages suspectes de modification du code. Son analyse marque notamment les instructions d’invalidation du cache (`icbi`) ; toutes ces plages ne sont donc pas nécessairement des modifications actives du code. Aucun correctif du jeu n’a été appliqué.
- Aucun REL nommé dans la FST, mais présence du diagnostic OSLink dans le DOL : l’absence de chargement dynamique n’est pas prouvée.
- La première compilation a démarré sur une VM de 3,3 Gio. Après augmentation, 6 processeurs et environ 11 Gio sont disponibles ; reprise à 4 tâches simultanées. Le script conserve un défaut prudent de 1, modifiable par `CMAKE_BUILD_PARALLEL_LEVEL`.
- Aucun périphérique `/dev/dri` visible lors de la préparation. Les performances graphiques de cette VM devront être mesurées.
- Terminer le jeu, valider les sauvegardes, l’audio et toutes les mécaniques reste nécessaire avant un statut « Vanilla Complete ».
