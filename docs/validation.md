# Validation fonctionnelle

Un test non effectué reste « non testé ». L’absence de crash n’est pas une preuve d’équivalence au jeu original.

| Domaine | Critère | État |
| --- | --- | --- |
| Génération | DOL traité sans instruction inconnue | Réussi |
| Extraction | 226 fichiers et DOL identiques aux lectures CISO | Réussi |
| Chargement natif | Module accepté, compteurs natifs actifs | Réussi : essai sans affichage de 30 s, 1 octobre 2026 |
| Démarrage | Logo Capcom et écran titre visibles | Réussi : captures examinées, 1 octobre 2026 |
| Entrées | Menus, déplacements, saut et attaques | Partiel : menus, poing, pied, accroupissement, uppercut et esquives validés via protocole ; déplacement à droite et saut validés dans la scène ; périphériques physiques non validés |
| Gameplay | Nouvelle partie et premier niveau jouable | Partiel : tutoriel franchi, scène jouable avec déplacement, saut, premier trou franchi et première mission remportée (trois ennemis, résultat B), traversée des plateformes et combat de la cascade terminés ; Tutorial 02 atteint, transition non résolue ; niveau complet non validé |
| Joe/Silvia | Changement de personnage et attaques spécifiques | Joe → Silvia validé dans le tutoriel ; attaques spécifiques non testées |
| VFX | Slow, Mach Speed, Zoom et Replay | Non testé |
| Vidéos | Absence d’écran noir, synchronisation audio/vidéo | Extrait d’introduction visible ; audio désactivé, synchronisation non testée |
| Audio | Initialisation, signal DSP, écoute et synchronisation | Partiel : Pulse initialisé, signal DSP non nul ; écoute/synchronisation non validées |
| Sauvegarde | Sauvegarder, quitter, relancer et charger | Non testé |
| Progression | Tous les niveaux, boss et transitions | Non testé |
| Fin du jeu | Partie complète avec journaux et révision identifiée | Non testé |

Les compteurs de repli du moteur doivent être examinés et leurs causes identifiées. Un succès en mode hybride ne sera pas présenté comme une recompilation intégrale.
