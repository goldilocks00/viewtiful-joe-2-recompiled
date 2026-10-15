# Reprise autonome

Le suivi de cette tâche est configuré dans l’application sous le nom « Continuer Viewtiful Joe 2 », toutes les 15 minutes. La VM, l’application et les fichiers locaux doivent rester disponibles. Il doit s’arrêter si le travail est réellement terminé ou si une intervention utilisateur devient nécessaire.

Lire `recomp-status.md`, puis les journaux de `build/`, avant d’agir. Ne pas relancer une opération encore active. `tools/project.sh` utilise désormais `flock` sur `build/.operation.lock` pour empêcher les exécutions concurrentes.

À la dernière mise à jour (2 octobre 2026) :

- Runtime EGL et module natif O2 construits ; aucune reconstruction complète nécessaire.
- Logo, écran titre, menus, nouvelle partie Normal, scène initiale et écran Tutorial 01 examinés à l’écran.
- L’essai graphique est arrêté. Le fichier `build/control/status.txt` peut rester sur `running` après l’arrêt : vérifier sa fraîcheur et le verrou, jamais son contenu seul.
- Test sans affichage borné réussi : `build/logs/native-headless-frames.json`, 711 images comptabilisées, sortie 0. Combats du premier tutoriel validés séparément ; initialisation audio et signal DSP validés, écoute non validée.
- Dernier essai : tutoriel franchi jusqu’au changement Joe → Silvia, capture `switch-test.png`. Session arrêtée ; journal `build/logs/gameplay-20261002.log`.
- Restauration de `tutorial-start.sav`, sortie du tutoriel, déplacement à droite et saut validés ; arrêt propre (code 0).
- Point de reprise conseillé : `build/control/artifacts/tank-intro.sav`, cinématique du char après les deux adversaires de la cascade ; rechargement validé. `waterfall-one-left.sav` reste disponible et sa restauration est validée.
- Audio : Pulse initialisé avec succès, signal DSP non nul, sortie 0 ; qualité à l’écoute et synchronisation non validées. Journaux `audio-test.log` et `audio-test-summary.json`. DumpAudio désactivé après mesure.
- Dernière session `slow-memory-probe.log` (recompilation statique, lecture seule de RAM) arrêtée, verrou libéré ; code de sortie 0. Première mission remportée, rang B et bonus V ×80. Utiliser `game_control.py step ... --frames N --capture nom-neuf.png` pour avancer puis suspendre avant examen.
- Prochaines validations : déterminer comment quitter la démonstration Tutorial 02 ; état `slow-tutorial-screen.sav` disponible. A/Start/B/L/Y/X/Z testés sans transition ; comparaison sans saut de cinématique conservée dans `slow-unskipped.sav`. Attente native supplémentaire de 3600 images et comparaison JIT64 A/L réalisées sans sortie de cet écran. L+Y combinés ont aussi échoué à quitter cet écran. Comparaison JIT depuis `waterfall-one-left.sav` effectuée jusqu’au même écran, sans transition avec L/A. Trace côté moteur confirmée : A+L=0140 et gâchette=255. Corrélation A/B/X/Y en RAM confirmée à 0x80353c12, 0x80353c16 et 0x803b6a0c. Prochain diagnostic : suivre la copie de jeu à 0x80353920 et son filtrage (nulle dans le dump A malgré les entrées brutes). Structure brute traitée à 0x80353c00 : précédent +0x10, actuel +0x14, pression +0x18, relâchement +0x1c ; conditions internes de sortie ; aucune cause établie dans la première scène, écoute/synchronisation, puis sauvegarde sur carte mémoire. Les états moteur ne valident pas la carte mémoire.
- Utiliser ±0,7 pour les axes du protocole ; ±1 n’a pas fait avancer l’exercice, cause encore inconnue.
- `save_state`/`load_state` sont disponibles dans `tools/game_control.py` ; état moteur créé et rechargement au démarrage validé. Aucun test de carte mémoire.
- Profils initiaux créés par `tools/prepare_user.py` : EFB 1x, OpenGL, clavier. Aucun écrasement des réglages existants.
- La préparation au partage GitHub est autorisée ; `docs/sharing.md` et `tools/audit_share.py` décrivent le contrôle de l’index et de l’historique. Publication effective non réalisée ; aucun remote configuré.
- Vérifier les permissions de session pour X11. Un refus ptrace antérieur ne doit pas être contourné.

Les données du jeu, captures, sauvegardes et fichiers générés restent hors Git.
