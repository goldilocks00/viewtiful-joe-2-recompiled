# État de la recompilation — Viewtiful Joe 2

Mise à jour : 1 octobre 2026.

| Étape | Résultat |
| --- | --- |
| Identification | G2VP08 révision 0, Europe/PAL |
| Extraction | 226 fichiers et main.dol vérifiés contre les lectures logiques du CISO |
| Chaîne locale | GCC 15, CMake 4.2.3, Ninja ; tests C et C++23 réussis |
| DolRecomp | Construit ; 19 tests sur 19 réussis |
| Génération C | Réussie ; 173 fragments ; aucune instruction inconnue signalée |
| ModernGekko | Compilé : moderngekko-run et moderngekko-port |
| Module natif | Construit en O2 ; bibliothèque Linux de 80 270 928 octets |
| Essai natif sans affichage | 30 secondes, arrêt propre ; détails ci-dessous |
| Logo / écran titre | Affichés ; menus et sélection de difficulté accessibles |
| Jeu complet | Non validé |

DolRecomp a examiné 703 520 mots de 32 bits : 703 497 instructions reconnues et 23 mots classés comme données embarquées. Son rapport SMC contient 147 plages suspectes, à valider dynamiquement. Aucun avertissement n’a été supprimé et aucun correctif du jeu n’a été appliqué.

Les versions exactes sont épinglées dans `config/sources.lock.json`. Voir `build.md` et `known-issues.md` pour la procédure et les limites.

Lors de la reprise, la liaison a échoué sur `xcb_get_setup` : des entrées du cache CMake pointaient vers les archives X11 statiques découvertes avant la réparation des liens du SDK local. Les entrées ont été actualisées vers les bibliothèques partagées existantes ; la liaison a ensuite réussi. Aucune modification du jeu pour résoudre ce problème.

## Exécution du 1 octobre 2026

Le module actif a été chargé sans `--allow-interpreter`. L’essai sans affichage a duré 30 secondes et s’est terminé avec un code de sortie 0, sans arrêt forcé. Journal local : `build/logs/smoke-20261001-101104.log`.

- `native=26602656` : distributions vers du code natif.
- `fallback=0` : aucun pas de repli du dispatcher.
- `native_exc=6958` : exceptions émulées, pas un compteur de crashs du processus.
- `hook_fb=8696754` : passages par le hook d’instruction ; ce hook contient à la fois des chemins rapides de cache et un chemin interprété. Le compteur ne permet pas de les distinguer.
- `smc_failed=0`, 48 vérifications et 8 événements de revérification.

Ces compteurs ne constituent ni un taux d’instructions natives ni une validation visuelle ou fonctionnelle du jeu.

Deux problèmes du runtime ont été identifiés :

1. Le rendu Null accédait au contexte ImGui absent pendant l’attente des shaders. Le patch `recompcore-headless-shader-progress.patch` omet uniquement l’overlay de progression pour un backend sans affichage. L’attente et la compilation restent actives. L’essai natif ci-dessus passe après ce correctif.
2. ModernGekko forçait EGL à OFF alors que le contexte OpenGL X11 de son RecompCore nécessite EGL. `moderngekko-enable-egl-option.patch` rend l’option configurable ; le projet la passe à ON. Reconstruction réussie dans `build/egl-build.log`. Validation graphique : logo Capcom, extrait de cinématique, écran titre, menu principal et choix de difficulté visibles.

## Premier essai graphique natif

`build/logs/native-graphical-egl.log` confirme OpenGL 4.5 via llvmpipe et le chargement du module. Les commandes Start et A ont permis de passer la cinématique, ouvrir Game Start, New Game, puis la difficulté Normal/Hard. Captures locales dans `build/control/artifacts/` : `boot-egl.png`, `next-egl.png`, `after-start.png`, `game-start.png`, `new-game.png`.

À l’arrêt demandé : `native=368488025`, `fallback=0`, `native_exc=52401`, `hook_fb=89526598`, `smc_failed=0`. Les statistiques de fermeture sont présentes ; le wrapper `timeout` a cependant renvoyé 143, donc cet essai n’est pas une preuve d’un code de sortie normal. L’essai suivant lance directement le runner pour vérifier ce point.

Le profil créé automatiquement par ModernGekko utilisait `resolution=1920x1080` (EFB 3x). Le projet fournit désormais un profil initial `640x528` (EFB 1x), conforme au périmètre sans améliorations. Les réglages existants sont préservés par `tools/prepare_user.py` ; celui de la session de test a été corrigé explicitement. L’audio est désactivé pendant ces diagnostics graphiques.

## Validation complémentaire

À la résolution native, une nouvelle partie en Normal a atteint la scène d’introduction puis l’écran Tutorial 01. Captures examinées : `scene-1.png` et `gameplay-initial.png` dans `build/control/artifacts`. Cela ne valide pas encore les déplacements ni les combats. Le journal `native-graphical-1x.log` contient une fermeture du moteur avec `native=2859743545`, `fallback=0`, `hook_fb=769531392`, `smc_failed=0` ; le code de sortie de cette session interrompue n’a pas été récupéré.

Le test borné avec suivi des images a ensuite réussi : `build/logs/native-headless-frames.json`, 711 images comptabilisées par le backend Null, code de sortie 0, aucun arrêt forcé ; `native=68750994`, `fallback=0`, `hook_fb=19906977`, `smc_failed=0`. Un compteur d’images en mode Null ne constitue pas une validation visuelle.

## Tutoriel de combat — 2 octobre 2026

Le module natif a franchi les exercices du premier tutoriel : coup de poing (Y), coup de pied (X), accroupissement, uppercut, esquive basse puis haute, frappe sur l’ennemi étourdi et changement de Joe vers Silvia (Z). La capture `switch-test.png` montre Silvia et l’invitation à quitter le tutoriel avec Start. Les captures intermédiaires `punch-test.png`, `soft-down.png`, `uppercut-test.png` et `dodge-test.png` ont été examinées. Elles restent dans `build/control/artifacts/`, hors Git.

Les axes extrêmes ±1 du protocole n’ont pas permis de franchir l’exercice d’accroupissement ; ±0,7 ont fonctionné. La cause des valeurs extrêmes n’est pas identifiée. Aucun correctif du jeu ni du runtime n’a été appliqué pour ce constat. Les entrées testées sont celles du protocole local, pas une manette physique ni le profil clavier.

Un état moteur `tutorial-start.sav` a été créé (environ 18 Mo), avant les exercices. Son rechargement reste à vérifier ; il ne remplace pas la validation de la sauvegarde sur carte mémoire. La session graphique s’est arrêtée depuis. Le journal `build/logs/gameplay-20261002.log` contient les statistiques finales : native=8297204844, fallback=0, native_exc=4251989, hook_fb=2080235708, smc_failed=0. Le code de sortie de la session n’a pas été récupéré.

La résolution interne est 1x ; les relevés du tutoriel tournaient autour de 22–23 images/s avec llvmpipe, soit environ 45 % de la vitesse PAL. Cela reste insuffisant pour revendiquer une expérience fluide sur cette VM.

Pour vérifier la séquence attendue du tutoriel, consultation du [guide GameFAQs de kabul04](https://gamefaqs.gamespot.com/gamecube/920421-viewtiful-joe-2/faqs/55302). Les résultats ci-dessus proviennent des essais locaux, pas du guide.

## Restauration et scène jouable — 2 octobre 2026

Un nouveau processus a restauré `tutorial-start.sav` avec `--load-state`. La capture `restored-tutorial.png` confirme la reprise au premier exercice ; les actions ont de nouveau permis de terminer le tutoriel. Après Start, Joe apparaît dans la scène jouable (`field-before.png`). Le déplacement à droite avec `main_x=0.7` et le saut avec A ont été vérifiés visuellement (`field-moved.png`, `field-jump.png`).

Deux nouveaux états locaux sont disponibles : `field-start.sav` et `field-progress.sav`, chacun environ 21 Mo. L’arrêt demandé via le protocole s’est terminé avec un code de sortie 0. Journal `build/logs/state-restore-test.log` : native=1499717971, fallback=0, hook_fb=428908813, smc_failed=0. La restauration d’un état moteur est validée ; la sauvegarde sur carte mémoire ne l’est pas.

## Audio — 2 octobre 2026

Un essai borné de 30 secondes a chargé `field-progress.sav`, initialisé PulseAudio en stéréo et quitté proprement (code 0). Journal `build/logs/audio-test.log` : `Pulse successfully initialized`, native=45231803, fallback=0, hook_fb=15977116, smc_failed=0. Le flux DSP enregistré localement contient 207 712 trames à 32 028 Hz, deux canaux 16 bits, pic absolu 11 493 et 415 005 échantillons non nuls. Le flux DTK de cette scène est silencieux.

Cela valide l’initialisation audio et la production d’un signal DSP ; la qualité à l’écoute et la synchronisation audio/vidéo ne sont pas encore validées. L’enregistrement a été désactivé après le test. Les fichiers WAV restent dans `build/user/Dump/Audio`, hors Git.

L’essai utilise `PULSE_SERVER=unix:/run/user/1000/pulse/native` et un `PULSE_RUNTIME_PATH` privé dans `build/pulse-runtime`. Le lanceur configure désormais ces variables lorsqu’un socket Pulse local existe et qu’aucun serveur n’est déjà choisi ; il préserve les variables fournies par l’utilisateur.

## Plateformes et contrôle par étapes — 2 octobre 2026

Depuis `field-progress.sav`, les déplacements et sauts ont atteint la grande feuille puis le sol à droite du premier trou. Les captures `leaf-checkpoint.png` et `step-leaf-jump.png` ont été examinées ; le compteur affiche deux bobines. Le déclenchement de la première mission avec trois ennemis est visible. Les essais d'uppercut montrent des animations de combat, mais la victoire sur ce groupe n'est pas validée (`uppercut-combat-5.png`, `combat-uppercut-next.png`).

Le contrôle en temps réel laissait le jeu avancer pendant l'examen des images. `game_control.py step` enchaîne désormais reprise, entrée bornée, capture, trois images neutres puis pause du moteur. Plusieurs séquences ont confirmé le retour à `state=paused` et une capture produite. Ce mécanisme utilise le protocole existant sans modifier le code du jeu.

États locaux : `after-pit.sav` conserve toute la vie après le premier trou ; `combat-progress.sav` reprend le combat avec deux unités de vie perdues. Préférer le premier pour un nouvel essai. `first-fight.sav` provient d'un essai mal positionné dans le trou et n'est pas recommandé. Les états restent hors Git.

La session `build/logs/first-level-resume.log` est arrêtée et le verrou libéré. Statistiques : native=961715673, fallback=0, hook_fb=328120552, smc_failed=0. Le lanceur a renvoyé 143 malgré les messages de fermeture du moteur : ne pas présenter cette session comme une sortie 0. Aucune validation de niveau complet ni de carte mémoire n'en découle.

## Première mission de combat remportée — 2 octobre 2026

Reprise depuis `combat-progress.sav` avec le lanceur habituel, module en cache et audio Pulse. Les entrées par étapes alternant Y/X avec `main_y=-0.7`, puis une orientation à gauche pour le dernier ennemi, ont permis de vaincre les trois adversaires. Les captures `combat-r2-chain-7.png`, `combat-r2-end-11.png` et `combat-r2-results.png` montrent la diminution du compteur puis l'écran de résultats : rang B, bonus V ×80. La dernière capture a été examinée directement. Aucun code du jeu n'a été modifié.

Point de reprise local créé : `build/control/artifacts/first-mission-cleared.sav` (21 158 402 octets), sur l'écran de résultats. Son rechargement reste à vérifier. La session a quitté avec le code 0 et libéré le verrou. Journal `build/logs/combat-resume.log` : native=242131603, fallback=0, hook_fb=74142152, smc_failed=0. Le compteur hook_fb reste non nul : ne pas qualifier cet essai d'exécution intégralement native sans replis internes.

Cette victoire valide le premier groupe d'ennemis, pas le premier niveau complet, les pouvoirs VFX, les boss ni la sauvegarde sur carte mémoire. Poursuivre depuis cet état, fermer l'écran de résultats puis progresser vers l'objectif suivant.

## Progression après la première mission — 3 octobre 2026

Le chargement de `first-mission-cleared.sav` a réussi. Après confirmation A, marche à droite pendant 100 images puis sauts A+droite de 40, 55 et 60 images, Joe a franchi les marches vers le plateau suivant. Les captures `after-mission-confirm.png`, `after-mission-wall.png`, `after-mission-top.png` et `after-mission-plateau.png` ont été examinées. Le compteur de bobines passe de 2 à 6 ; un ennemi volant est visible à droite. Aucun combat contre cet ennemi n'est encore validé.

État local `second-platform.sav` créé (22 446 160 octets), avant le prochain obstacle. Session arrêtée avec code 0, verrou libéré. Journal `build/logs/after-mission.log` : native=89191228, fallback=0, hook_fb=28810352, smc_failed=0. Ces résultats étendent la progression vérifiée mais ne valident pas le niveau complet.

## Traversée des feuilles et de l'eau — 3 octobre 2026

`second-platform.sav` a été rechargé avec succès. Un premier saut avec attaque X a conduit à une chute ; l'état a été restauré avant de réessayer sans attaque. Les sauts à droite ont ensuite atteint la feuille, traversé la zone d'eau puis rejoint la berge à droite. Captures examinées : `plateau-jump-02.png`, `plateau-leaf-03.png`, `plateau-land-05.png`, `plateau-water-06.png`, `plateau-bank-08.png`. Le compteur de bobines atteint 11. Les ennemis volants ont été dépassés, pas vaincus : leur combat reste non validé.

Point de reprise `after-water.sav` créé (21 265 596 octets), après 35 images neutres sur la berge. Journal `second-platform.log` : native=62140420, fallback=0, hook_fb=19313207, smc_failed=0 ; sortie 0 et verrou libéré. Aucun changement du code du jeu. Poursuivre vers la droite depuis ce nouvel état, dont le rechargement reste à vérifier.

## Arrivée à la cascade — 3 octobre 2026

Restauration de `after-water.sav` réussie. Une marche à droite de 70 images déclenche une vue cinématique de la cascade (`water-next-01.png`). Après Start et 60 images neutres, déplacement de 40 images, saut A+droite de 45 images puis droite de 40 images : Joe atteint les feuilles devant la cascade. Après 70 images neutres, une nouvelle mission affiche un compteur de deux ennemis (`waterfall-mission.png`, examinée). Le compteur de bobines est à 13. Cette mission n'est pas encore remportée.

État `waterfall-mission.sav` créé (22 577 348 octets). Journal `after-water.log` : native=57498561, fallback=0, hook_fb=17883640, smc_failed=0. Sortie 0, verrou libéré. Prochaine étape : reprendre cet état et examiner les deux adversaires.

## Combat de la cascade, premier adversaire — 3 octobre 2026

Restauration de `waterfall-mission.sav` réussie. Saut à droite de 40 images puis déplacement de 45 images vers la feuille devant la cascade. Une orientation à gauche et des attaques alternées X/Y accroupies ont détruit un adversaire : `cascade-combat-9.png` montre sa destruction et le compteur passant à 1. `cascade-wait.png`, examinée après 120 images neutres, confirme qu'un adversaire reste ; une partie d'un personnage apparaît en bas à gauche. Aucun écran de victoire sur cette mission.

État `waterfall-one-left.sav` créé (21 338 636 octets), Joe sur la feuille, 13 bobines, 249 points. Rechargement de ce nouvel état à vérifier. Journal `waterfall-combat.log` : native=123670303, fallback=0, hook_fb=37159666, smc_failed=0 ; sortie 0, verrou libéré. Prochaine étape : localiser et vaincre le dernier adversaire en contrebas.

## Dernier adversaire de la cascade et arrivée du char — 3 octobre 2026

Rechargement de `waterfall-one-left.sav` réussi. Descente à gauche (55 puis 30 images) jusqu'au dernier adversaire au sol, visible dans `cascade-lower.png`. Deux séries de 12 attaques X/Y alternées avec accroupissement, 25 images chacune, ont permis de terminer le combat : `cascade-finish-7.png` montre la disparition du compteur d'ennemis et 853 points. Après la transition noire et 120 images neutres, `cascade-outcome.png` montre la cinématique d'arrivée d'un char devant la cascade. Ces captures ont été examinées ; le combat contre le char n'est pas validé.

État `tank-intro.sav` créé (20 712 132 octets), pendant cette cinématique ; rechargement à vérifier. Journal `waterfall-last.log` : native=142498796, fallback=0, hook_fb=44271497, smc_failed=0. Sortie 0 et verrou libéré. Prochaine étape : poursuivre la cinématique et examiner les commandes du combat contre le char.

## Écran Tutorial 02 — 3 octobre 2026

Restauration de `tank-intro.sav` réussie. Start puis 90 images neutres atteignent l'écran animé « Awaken the Power Within! », Tutorial 02, qui explique Slow avec L, l'esquive V-Dodge et le renvoi des projectiles. Captures examinées : `tank-instructions.png`, `slow-after-demo.png`, `slow-back.png`. Il s'agit d'une démonstration à l'écran : cela ne valide pas encore l'utilisation réelle de Slow dans le gameplay.

Les essais A, Start, B, L numérique avec L analogique, et trois périodes neutres de 600 images n'ont pas quitté cet écran. L'animation et le texte évoluent ; la cause de cette absence de transition reste à examiner (commande attendue, durée ou comportement du runtime), sans diagnostic de panne établi. État local `slow-tutorial-screen.sav` conservé pour cette investigation ; conserver aussi `tank-intro.sav` pour comparer une reprise antérieure.

Journal `tank-intro.log` : native=289081633, fallback=0, hook_fb=73056652, smc_failed=0 ; sortie 0, verrou libéré. Prochaine étape : déterminer la transition attendue du Tutorial 02 avant de valider le combat contre le char.

## Comparaison sans saut de cinématique — 3 octobre 2026

La reprise de `slow-tutorial-screen.sav` fonctionne ; Y, X et Z pendant 60 images chacun ne quittent pas l'écran animé (captures `slow-y-test.png`, `slow-x-test.png`, `slow-z-test.png`). Puis restauration de `tank-intro.sav` et cinq étapes neutres de 600 images, sans Start : la cinématique progresse jusqu'au même Tutorial 02 (`tank-unskipped-5.png`). Cela exclut seulement la nécessité de sauter la cinématique pour atteindre cet écran, pas un défaut de transition ultérieure. État de comparaison conservé : `slow-unskipped.sav`.

Le [guide de kabul04](https://gamefaqs.gamespot.com/gamecube/920421-viewtiful-joe-2/faqs/55302) décrit les exercices Slow après le char, sans préciser comment quitter cet écran de démonstration. Le code local `dolphin_runtime.cpp` confirme que `pad_frames` applique les entrées puis les libère après le compteur demandé. Il reste à examiner la durée complète de la démonstration et, si nécessaire, comparer le comportement avec un cœur de référence avant de modifier le runtime.

Journal `slow-transition.log` : native=397782122, fallback=0, hook_fb=127631373, smc_failed=0 ; sortie 0 et verrou libéré. Aucun correctif ni validation de Slow réel à ce stade.

## Attente prolongée et comparaison JIT — 3 octobre 2026

Depuis `slow-unskipped.sav`, six étapes neutres de 600 images en recompilation statique laissent la démonstration affichée (`slow-duration-5.png`, examinée). Session `slow-duration.log` : native=443284989, fallback=0, hook_fb=107174492, smc_failed=0 ; sortie 0.

Une comparaison distincte a ensuite utilisé `MODERNGEKKO_STATICRECOMP=0 tools/project.sh run --load-state "$PWD/build/control/artifacts/slow-unskipped.sav" --audio Pulse --automation-dir "$PWD/build/control"`. Le code `SelectCPUCore()` de `src/runtime/dolphin_runtime.cpp` sélectionne JIT64 sur cette machine avec cette variable. Le module reste chargé par le lanceur, ce qui ne rend pas cette exécution native statique ; aucun compteur de fermeture StaticRecomp n'apparaît.

Dans cet essai JIT, A pendant 120 images puis L numérique et analogique pendant 120 et 600 images laissent également l'écran Tutorial 02 visible (`slow-jit-a.png`, `slow-jit-l.png`, `slow-jit-long-l.png`, examinées). L'animation passe à l'explication du renvoi par coup de poing. Sortie 0 ; journal `slow-jit-comparison.log`, verrou libéré. Aucun état JIT n'a remplacé les points de reprise natifs.

Ce test ne révèle pas de différence de transition entre les deux cœurs sur les entrées essayées. Il n'exclut pas un problème partagé du runtime ou un état sauvegardé déjà incorrect. Prochain diagnostic : comprendre les conditions de sortie de cette démonstration et les entrées effectivement lues, ou comparer depuis un état antérieur. Ne pas répéter indéfiniment les mêmes boutons ni présenter ce test JIT comme un progrès du port natif.

## Entrées combinées et inspection du protocole — 3 octobre 2026

Inspection de `ApplyAutomationPad` : le protocole transmet les contrôles au périphérique Touch ; cela ne prouve pas que le jeu les consomme dans cet écran. Depuis `slow-tutorial-screen.sav`, une entrée combinée `l=1 l_analog=1 y=1` de 300 images en recompilation statique ne quitte pas la démonstration (`slow-combined-input.png`, examinée). Journal `slow-combined-input.log` : native=43193460, fallback=0, hook_fb=14945570, smc_failed=0 ; sortie 0, verrou libéré.

Pour la prochaine investigation, privilégier une comparaison JIT depuis `waterfall-one-left.sav` avant l'entrée dans le tutoriel, ou une observation des lectures manette en mémoire via le protocole de lecture existant. Les comparaisons précédentes reprennent des états créés par le cœur statique après l'entrée dans la démonstration : elles ne peuvent exclure un problème introduit plus tôt. Ne pas réessayer les mêmes séquences d'attente et de boutons sur ces états sans hypothèse nouvelle.

## Comparaison JIT depuis le combat précédent — 3 octobre 2026

Avec `MODERNGEKKO_STATICRECOMP=0`, reprise de `waterfall-one-left.sav`, descente à gauche de 55 puis 30 images et 24 attaques X/Y accroupies de 25 images. Le dernier adversaire est franchi et la cinématique du char commence. Après 120 images neutres puis Start pendant 120 images, le Tutorial 02 apparaît (`jit-before-tutorial.png`). L numérique+analogique pendant 600 images puis A pendant 120 images laissent encore cette démonstration affichée (`jit-before-slow.png`, `jit-before-confirm.png`, examinées).

Cette comparaison utilise JIT64 dès avant le dernier combat, pas seulement après l'entrée dans le tutoriel. Elle ne met pas en évidence un défaut propre à la recompilation statique pendant cette transition ; elle ne constitue pas une validation native. Aucun nouvel état JIT n'a été sauvegardé. Session `jit-before-tutorial.log` arrêtée avec code 0, verrou libéré.

La prochaine investigation doit observer les lectures manette ou les conditions internes de sortie de cet écran, plutôt que répéter l'attente et les boutons. Les données du jeu et les captures restent locales.

## Lecture manette instrumentée — 3 octobre 2026

Ajout d'une trace optionnelle et bornée à `Pad::GetStatus`, sans modification des valeurs retournées. Reconstruction incrémentale à quatre tâches réussie (`pad-trace-build.log`), après correction d'un nom de champ de diagnostic lors de la première compilation.

Essai natif depuis `slow-tutorial-screen.sav` avec `VJ2_TRACE_PAD=1`, A+L numérique+L analogique pendant 180 images. `slow-pad-trace.log` confirme une manette connectée, boutons `0140` (A et L), gâchette gauche 255 et stick centré 128,128 aux lectures 60 à 360. Les entrées atteignent donc bien la lecture manette côté moteur. Cela ne prouve pas leur consommation par la logique du tutoriel : prochaine étape, examiner le buffer PAD côté jeu et les conditions de sortie de la démonstration. Session arrêtée avec code 0. Le patch est appliqué de manière idempotente par `fetch_sources.py` et reste désactivé par défaut.

## Corrélation des boutons dans la RAM invitée — 3 octobre 2026

Depuis `slow-tutorial-screen.sav` en recompilation statique, quatre mesures successives : reprise, `command=pad` port 0 avec respectivement A/B/X/Y seuls, attente de deux secondes réelles, pause, `command=read_memory` à `address=0x80000000`, `size=16777216`, puis libération des entrées. Les dumps `pad-probe-{a,b,x,y}.bin` et le script exact `build/diagnostics/probe_pad.py` restent hors Git. Aucun octet de mémoire n'a été écrit par le protocole.

Recherche corrélée des valeurs big-endian 0x0100/0x0200/0x0400/0x0800 dans les quatre dumps : trois positions 16 bits concordent, 0x80353c12, 0x80353c16, 0x803b6a0c ; les deux premières correspondent aussi à des mots 32 bits aux adresses 0x80353c10 et 0x80353c14. Il s'agit de candidats de buffers manette, pas encore de symboles PADRead identifiés. Cette corrélation démontre que l'effet des entrées atteint la RAM du jeu pendant cet écran ; elle ne prouve pas que la logique de sortie du tutoriel les exploite.

Prochaine étape : identifier les lecteurs de ces adresses et distinguer état maintenu, front de pression et données SDK ; suivre ensuite leur usage dans la transition Tutorial 02. Journal `slow-memory-probe.log` : native=46053335, fallback=0, hook_fb=11393826, smc_failed=0 ; sortie 0 et verrou libéré.

## Reprise du diagnostic — 3 octobre 2026

Recherche statique ciblée dans le DOL : une lecture directe du candidat 0x80353c14 est repérée à 0x801fda60. Le traitement suivant teste le masque 0x1600 ; cette référence seule ne suffit pas à l'attribuer à la sortie du tutoriel. Le candidat 0x803b6a0c est transmis comme argument à deux routines depuis 0x80207460 et 0x80207468 (cibles 0x802781ec et 0x802774ec), puis traité dans une boucle de quatre éléments. Cela fournit des points d'entrée concrets pour identifier le traitement des manettes ; aucune modification du DOL ou des sources générées n'a été faite.

## Identification des deux niveaux d'entrée — 3 octobre 2026

L'analyse statique de la routine vers 0x802074e8 identifie le buffer brut à 0x803b6a0c, puis la structure à 0x80353c00 (pas de 60 octets par port). Dans cette structure, +0x10 conserve l'état précédent, +0x14 l'état actuel, +0x18 les pressions nouvelles, +0x1c les relâchements et +0x20 la répétition. La copie vers les structures de jeu commence à 0x80353920, avec un pas de 184 octets.

Dans le dump A déjà capturé, les mots brut/précédent/actuel contiennent le bouton, mais la copie de jeu est nulle. Le pointeur global trouvé via r13=0x80459ec0 pointe vers 0x80353d00 ; ses flags à +6000 valent 0x00808004 dans ce dump. Le bit 0x1000 testé dans la routine de copie n'est donc pas positionné dans cette mesure. Une autre étape peut filtrer ou remplacer les entrées après copie. La routine vers 0x801d51f0 contient notamment un filtrage, mais son exécution pendant Tutorial 02 n'est pas encore démontrée.

Prochaine mesure : observer cette copie de jeu et son filtrage aux différentes étapes de la boucle ; ne pas supprimer de masque ni forcer une transition sans comprendre son rôle. Aucun patch de gameplay appliqué.

## Filtre conditionnel et essai R — 3 octobre 2026

La routine 0x801d503c choisit son filtrage selon l'octet +6 de son objet : certains états annulent les boutons de la copie de jeu, d'autres autorisent des masques spécifiques. Elle est appelée depuis 0x801d477c, après 0x801d49ec et avant le traitement de transition 0x801d522c. Il reste à identifier l'objet actif à l'exécution : cette analyse statique ne prouve pas que cette routine gère l'écran affiché du Tutorial 02. Ne pas modifier ces masques sur cette seule base.

Essai distinct depuis `slow-tutorial-screen.sav` : R numérique et analogique pendant 180 images. La capture `slow-r-investigation.png` montre toujours la démonstration et son indication L. Aucune transition validée. Session `slow-filter-investigation.log` arrêtée avec code 0. Prochaine investigation ciblée : identifier l'objet et son état lors de l'appel du filtre, puis suivre la condition de transition correspondante, sans forcer l'état du jeu.

## Recherche de l'objet du filtre — 3 octobre 2026, suivi 15:00 UTC

L'initialisation liée au filtre est à 0x801d4328 ; le répartiteur 0x801d42d8 choisit sa routine via l'octet +4 de l'objet. L'initialisation écrit un pointeur à +80 et la valeur 100 à +304. Recherche alignée dans les 16 Mio du dump A : aucun candidat combinant +304=100, +4 dans {1,2}, +6<7 et un pointeur +80 dans la RAM. Cela ne démontre pas l'absence d'objet : il pourrait être hors de la plage capturée, avoir changé de champs, ou appartenir à un autre tutoriel. La piste reste non confirmée ; aucune correction de gameplay justifiée.

Ne pas relancer des combinaisons de boutons identiques. Prochaine étape utile : obtenir l'adresse de l'objet à l'exécution du répartiteur ou étendre la capture de RAM aux 8 Mio restants avant de poursuivre cette piste. Dernier journal inchangé, verrou disponible, aucune nouvelle compilation ou session graphique lancée pendant ce suivi.

## Capture complète de RAM — 3 octobre 2026, suivi 15:15 UTC

Reprise native de `slow-tutorial-screen.sav`, pause du moteur, puis lectures de 16 Mio à 0x80000000 et 8 Mio à 0x81000000. Les fichiers locaux `slow-ram-low.bin` et `slow-ram-high.bin` couvrent ensemble les 24 Mio ; script reproductible `build/diagnostics/probe_fullram.py`. Aucune écriture en RAM invitée.

Aucun candidat dans cette capture complète avec les critères précédents (+304=100, +4 dans {1,2}, +6<7, pointeur +80 dans la RAM). Une recherche alternative remplaçant +304=100 par le flottant 1000 à +28 ne trouve rien non plus. La plage manquante n'explique donc pas le résultat avec ces critères ; ils peuvent être trop restrictifs ou viser une autre routine. Ne pas poursuivre des recherches de signatures supposées sans mesure dynamique de l'appel. Prochaine piste : trace bornée du répartiteur 0x801d42d8 et de l'adresse de son objet, pour confirmer ou abandonner l'attribution à Tutorial 02.

Session `slow-fullram.log` arrêtée avec code 0. Aucun jalon de gameplay supplémentaire validé ; captures et dumps hors Git.

## Trace de dispatch ciblée — 3 octobre 2026, suivi 15:30 UTC

Ajout d'une trace optionnelle bornée à 32 lignes aux entrées de dispatch 0x801d42d8/0x801d503c, enregistrant PC, r3 et LR. Patch reproductible intégré à `fetch_sources.py`, désactivé par défaut. Reconstruction incrémentale à quatre tâches réussie (`tutorial-entry-build.log`) ; huit tests Python réussis.

Essai natif avec `VJ2_TRACE_TUTORIAL_ENTRY=1` depuis `slow-tutorial-screen.sav`, 180 images neutres puis pause. Aucune ligne `[vj2-entry]` dans `slow-entry-trace.log`. Ce résultat ne confirme ni n'exclut l'appel, car les branches internes aux blocs générés ne repassent pas nécessairement par ce dispatch. La trace n'apporte donc pas encore l'adresse de l'objet ; il faudra observer l'entrée dans le bloc généré lui-même ou identifier une entrée réellement dispatchée. Session arrêtée avec code 0 ; aucun correctif ni nouvelle validation de gameplay.

## Observation directe des blocs — 3 octobre 2026

Instrumentation temporaire locale des labels 0x801d42d8 et 0x801d503c dans le chunk généré 117 : compteur borné à huit messages par label, PC/r3/LR uniquement. Reconstruction incrémentale du module dans `module-build` réussie (`tutorial-block-build.log`). Le module actif à la racine du cache n'a pas été remplacé ; lancement direct de `moderngekko-run` avec le module de diagnostic de `module-build`, état `slow-tutorial-screen.sav` et 180 images neutres.

`slow-block-trace.log` confirme le chargement de ce module instrumenté ; aucune ligne `[vj2-block]` pendant l'essai. Contrairement à la trace de dispatch, les labels instrumentés couvrent aussi leurs branches internes. Aucun passage natif dans ces deux labels n'a donc été observé dans cette fenêtre ; cela affaiblit leur attribution à l'écran courant, sans exclure un passage à un autre moment. Session arrêtée avec code 0. Pas de transition de gameplay validée.

Source générée restaurée depuis la copie locale originale, puis reconstruction de restauration réussie (`tutorial-block-restore-build.log`, sortie 0). Les sources générées, la copie de diagnostic et les captures restent ignorées par Git. Prochaine investigation : identifier le gestionnaire de l'écran de démonstration réellement actif plutôt que poursuivre les signatures de cet objet non observé.

## Profil de l'écran actif — 3 octobre 2026, suivi 17:01 UTC

Essai natif du module normal, `STATICRECOMP_DISPATCH_SAMPLES=1 tools/project.sh run --load-state "$PWD/build/control/artifacts/slow-tutorial-screen.sav" --audio Pulse --automation-dir "$PWD/build/control"`, puis 240 images neutres et arrêt propre (code 0). Journal `slow-dispatch-profile.log` ; native=29173587, fallback=0, hook_fb=7217762, smc_failed=0. L'échantillonnage porte sur un dispatch sur 4096 et affiche les 16 sites les plus fréquents ; ce n'est pas un relevé exhaustif des fonctions.

Premier site : 0x801fd780 (1616 échantillons), boucle attendant un global non nul à r13-29952. Elle domine le profil sans démontrer un blocage permanent : les images continuent d'avancer. Parmi les autres sites : 0x80138964 (194), petite comparaison de l'identifiant 16 bits à +566 de son argument, et 0x800bd29c (188). Ces entrées réellement observées peuvent servir à relever les appelants (LR) et remonter vers le gestionnaire actif. Aucune chaîne ASCII `TUTORIAL`, `tutorial`, `Awaken`, `SLOW` ou `Slow` trouvée dans le DOL ; ne pas supposer que les textes de cet écran y sont présents. Aucun nouveau jalon de gameplay.

## Appelant réellement observé — suivi 17:16 UTC

Trace bornée réorientée vers 0x80138964 et 0x800bd29c, sites observés dans le profil. Reconstruction incrémentale réussie (`active-entry-build.log`), vérification inverse du patch réussie et huit tests Python réussis. Essai natif de 180 images depuis `slow-tutorial-screen.sav`, journal `slow-active-entry.log`, sortie 0.

La trace obtient effectivement `pc=80138964 r3=80852128 lr=800bd29c` ; au retour, `pc=800bd29c r3=0 lr=800bd29c`. L'analyse du code confirme l'appel à 0x800bd298, dans une boucle comparant des identifiants chargés dans une table globale. Le LR au retour est encore celui de cet appel interne : il ne fournit pas l'appelant supérieur. Pour remonter plus loin, viser l'entrée de la routine englobante ou son LR sauvegardé sur la pile. L'objet observé ne doit pas encore être qualifié de gestionnaire du tutoriel. Aucune nouvelle transition de jeu validée.

## Remontée statique des appelants — suivi 17:31 UTC

La routine englobant le site observé commence à 0x800bd218 ; son prologue sauvegarde LR à +28 de la pile après allocation de 24 octets. Deux appels directs trouvés dans les commentaires du code généré : 0x80138a5c (argument r4=4, retour 0x80138a60) et 0x80139ea8 (r4=2, retour 0x80139eac). Une observation future de ces retours ou du LR sauvegardé permettra de les distinguer sans supposer qu'il s'agit de la logique du tutoriel.

Dans la capture antérieure `slow-ram-low.bin`, l'objet 0x80852128 contient 0x80139378 aux offsets +4 et +292 et l'identifiant 0x0203 à +566. La présence de traitements de matrices dans le premier appelant invite à vérifier si cette piste concerne l'affichage plutôt que les commandes. Ces données proviennent d'une capture antérieure, pas d'un instantané synchronisé avec la trace. Aucun lancement supplémentaire ni modification de gameplay lors de ce suivi ; verrou disponible et dernier essai arrêté.

## Discrimination des deux appelants — 3 octobre 2026

Trace bornée déplacée vers les retours 0x80138a60 et 0x80139eac ; reconstruction incrémentale réussie (`caller-entry-build.log`), patch inverse vérifié, huit tests Python réussis. Essai natif depuis `slow-tutorial-screen.sav`, 180 images neutres ; `slow-caller-entry.log` enregistre 0x80138a60 avec r3=0 ou 1. La limite globale de 32 lignes ne permet pas d'affirmer que l'autre site ne s'exécute jamais. Le premier appelant est effectivement observé, mais son traitement contient des opérations de matrices : ne pas le confondre avec la logique de sortie du tutoriel. Arrêt propre avec code 0.

Recherche de documentation de jeu effectuée ; le guide https://gamefaqs.gamespot.com/gamecube/920421-viewtiful-joe-2/faqs/34469 ne fournit pas, dans les résultats examinés, de nouvelle commande confirmée pour quitter cette démonstration. Aucune nouvelle combinaison testée sans hypothèse. La transition Slow reste non résolue ; prochaine piste à privilégier : les lecteurs du buffer de pressions brutes pendant l'écran, plutôt que les sites fréquents de rendu.

## Lecteurs des boutons — suivi 17:46 UTC

Recherche des lectures directes des offsets 14644 (+0x14, boutons maintenus) et 14648 (+0x18, pressions) de la copie à 0x80353920 dans les commentaires PPC générés. Inventaire local détaillé : `build/diagnostics/pad-copy-read-sites.json` (non publié, contient des extraits générés). Les résultats doivent être filtrés selon le registre de base : un offset seul n'établit pas l'adresse effective. Plusieurs lecteurs utilisent les masques globaux r13-29972 et r13-29968 ; d'autres des masques immédiats.

La recherche de lectures directes à 0x80353c14/0x80353c18 et des constructions de base 0x80353c00 retrouve surtout le traitement/copieur et le test 0x1600 déjà repéré. Cela oriente la prochaine observation vers les lecteurs de la copie de jeu, plutôt que les routines fréquentes de rendu. Aucun correctif appliqué, aucun nouvel essai lancé ; dernier journal et verrou cohérents avec un runtime arrêté.

## Instrumentation des lecteurs en préparation — suivi 18:01 UTC

Ajout temporaire de traces dans 15 chunks générés, juste après les 47 lectures candidates recensées : au maximum trois lignes par site, avec adresse de l'instruction, valeur lue et LR. Les sources d'origine et leurs SHA-256 sont conservés dans `build/diagnostics/pad-reader-trace/manifest.json` et les fichiers voisins. Aucun fichier généré ajouté à Git.

Compilation incrémentale à quatre tâches lancée sous le verrou du projet, journal `pad-reader-trace-build.log`, sortie de diagnostic dans `module-build/gG2VP08_recomp.so`. Le module normal à la racine du cache reste intact. À la reprise, vérifier le verrou et la fin du journal avant tout lancement : ne pas lancer une autre compilation. Ensuite lancer directement le runner avec le module de `module-build`, reprendre `slow-tutorial-screen.sav`, mesurer les sites réellement lus. Après l'essai, restaurer chaque source depuis le manifeste et reconstruire `module-build`. Ne pas utiliser ce module instrumenté comme preuve de validation du jeu normal.

## Résultat des 47 sondes — suivi 18:16 UTC

Compilation instrumentée terminée avec code 0. Lancement direct du module de diagnostic de `module-build` depuis `slow-tutorial-screen.sav`, A pendant 180 images puis arrêt propre (code 0), journal `slow-pad-reader-trace.log`. Aucune ligne `[pad-reader]` enregistrée aux 47 sites instrumentés. Ces sondes couvrent uniquement les lectures directes recensées, pas les lectures par pointeur ni les éventuels chemins interprétés ; leur silence ne démontre pas l'absence de lecture des boutons dans le jeu. Aucun progrès de gameplay validé.

Les 15 sources générées ont été restaurées et leurs sauvegardes vérifiées par SHA-256. Reconstruction incrémentale de restauration lancée à quatre tâches sous verrou, journal `pad-reader-restore-build.log` : vérifier sa fin avant une nouvelle opération. Le module normal du cache reste intact. Prochaine analyse : vérifier si la boucle affichée suit un chemin de démonstration/cinématique avec traitement des entrées indirect, et considérer les replis internes plutôt que multiplier les sondes DOL silencieuses. Aucun fichier `.rel` ou `.rso` nommé repéré dans l'extraction, ce qui n'exclut pas d'autres chargements dynamiques.

## Restauration et portée des replis — 4 octobre 2026

Reconstruction de restauration terminée avec code 0 (`pad-reader-restore-build.log`), verrou libre. Les 15 sources générées correspondent toutes aux SHA-256 d'origine du manifeste. Aucun runtime lancé lors de ce contrôle.

Lecture de `HookInstructionFallback` : le compteur `hook_fb` est incrémenté avant une voie rapide pour certaines instructions de cache, qui ne passe pas par l'interpréteur. Les autres cas exécutent une seule instruction via `SingleStepInner`, puis rendent la main au dispatcher. Le compteur ne représente donc ni un nombre de fonctions interprétées ni un pourcentage de gameplay interprété. Il ne suffit pas à expliquer le silence des sondes sur les lectures de boutons.

Comparaison pixel par pixel de `slow-r-investigation.png` avec six captures des essais suivants : différences présentes dans la zone animée (environ x=66..636, y=59..348), confirmant des images distinctes. Cela ne mesure pas la cadence et ne valide pas une transition de jeu. Prochaine observation utile : vérifier le traitement/copieur des entrées à l'exécution comme contrôle positif avant d'instrumenter de nouveaux lecteurs.

## Contrôle positif du traitement PAD — 4 octobre 2026

Deux sondes temporaires dans le chunk 130, après la lecture brute à 0x80207518 et après copie à 0x80207970, bornées à 16 messages par site. Compilation réussie (`pad-copy-build.log`) et présence des formats de trace vérifiée dans le binaire. Essai du module instrumenté : A pendant 180 images depuis `slow-tutorial-screen.sav`, puis arrêt propre, code 0 (`slow-pad-copy.log`).

Cette fois les sondes s'exécutent : à 0x8020751c, r9=0x0100 pour le port 0 ; à 0x80207970, r8 prend successivement 0x80353920, 0x803539d8, 0x80353a90, 0x80353b48. Le traitement natif reçoit donc A et atteint la copie vers les quatre structures. Cela valide le mécanisme d'instrumentation local, mais ne prouve pas la valeur finale de la copie après filtrage. Les lecteurs directs précédemment sondés n'ont pas été observés dans leur fenêtre ; privilégier maintenant les accès indirects ou les écritures qui effacent cette copie.

Source du chunk 130 restaurée depuis `build/diagnostics/chunk130-original.c`. Reconstruction de restauration lancée sous verrou : `pad-copy-restore-build.log`, à vérifier avant tout nouvel essai. Aucun changement du module normal, aucune transition de gameplay validée.

## Accès par base de structure — 4 octobre 2026, suivi 22:31 UTC

Reconstruction de restauration précédente terminée avec code 0 et verrou libéré. Nouvelle observation préparée : 57 constructions d'adresse utilisant `addi ...,14624`, réparties dans 20 chunks générés. Trace juste après la construction, limitée à deux lignes par site (adresse calculée, r3, LR). La valeur calculée permettra d'écarter les constantes sans rapport avec la base PAD ; ce sont des candidats, pas 57 accès PAD prouvés.

Copies originales et empreintes dans `build/diagnostics/pad-base-trace/manifest.json`. Compilation incrémentale à quatre tâches en cours sous verrou, journal `pad-base-build.log`. À la reprise : vérifier sa fin, exécuter directement le module de `module-build` depuis l'état Slow, relever les bases effectivement égales à 0x80353920, puis restaurer les 20 sources et reconstruire. Module normal du cache intact ; données et instrumentation générée hors Git.

## Filtre actif identifié — 4 octobre 2026, suivi 22:46 UTC

Compilation des sondes de base terminée avec code 0. Essai instrumenté depuis l'état Slow, A pendant 180 images, sortie 0 (`slow-pad-base.log`). Six sites observent effectivement la base 0x80353920 : 0x801d3544 (r3=0x808b54b0), 0x801d413c, 0x801ecc40, 0x801ecf1c, 0x802078f0 et 0x8020b888.

La routine 0x801d4120 est donc une piste exécutée, contrairement au filtre initial 0x801d503c. Elle appelle 0x801fe9a8 avec l'identifiant lu à +272 de son objet (5 dans la trace) ; si le résultat est nul, elle efface précédent/actuel/pression de PAD. Ensuite elle filtre selon l'octet +5. La capture antérieure de l'objet 0x808b54b0 porte +5=2 ; ce chemin ne conserve que le bit L (0x40). Il reste à mesurer le résultat du premier test dans la session active, sans forcer ces conditions.

0x801fe9a8 teste le bit 0x2 du demi-mot +24 d'une table à global+0x40000+29392, pas de 36 octets, index 0..5. Prochaine étape ciblée : suivre ce bit pour l'entrée 5 et les routines qui le définissent. Les 20 sources ont été restaurées après vérification des sauvegardes ; reconstruction de restauration en cours (`pad-base-restore-build.log`), vérifier le verrou avant de relancer. Aucun changement de gameplay ni transition validée.

## L atteint bien la logique Slow — suivi 23:01 UTC

Restauration des 20 chunks terminée (code 0). Deux essais du module normal depuis `slow-tutorial-screen.sav`, avec `command=pad`, `port=0`, `l=1`, `l_analog=1`, puis pause et lecture de 24 Mio de RAM après 3 et 30 secondes réelles. Arrêts propres, codes 0 ; journaux `slow-l-state.log` et `slow-l-sustained.log`. Dumps locaux `slow-l-ram-{low,high}.bin` et `slow-l-long-ram-{low,high}.bin`, hors Git.

Après 3 secondes, L=0x40 est présent dans le PAD brut, traité et copié. Le filtre conserve donc bien L. Le bit 0x40000000 de global+6036 est défini ; objet 0x808b54b0 : état +5=2, sous-état +7=1. Après 30 secondes de maintien continu, l'état passe à +5=3, +7=0. Ceci prouve une transition interne du tutoriel sous entrée normale, sans modification de mémoire invitée ; pas encore une validation visuelle de la suite ni du gameplay Slow complet.

La routine 0x801d3520 attend en sous-état 1 que l'écart de position (+396) entre joueur et objet 28 atteigne le seuil. Objet 28 trouvé à 0x806c831c : position 12389 après 3 secondes, 12347 après 30 ; joueur 12200. Cette observation correspond au seuil de 150 du chemin courant. Les anciens essais courts et les captures après relâchement ne suffisaient donc pas à caractériser cette attente.

Prochaine étape : reprendre le même état, maintenir L en continu assez longtemps pour atteindre l'état 3, capturer et sauvegarder avant de relâcher ; suivre ensuite l'entrée Y attendue par 0x801d3758. Aucun correctif du runtime justifié par ces observations. Runtime arrêté, aucune compilation active.

## Transition visuelle du tutoriel Slow — suivi 23:16 UTC

Module normal repris depuis `slow-tutorial-screen.sav`, journal `slow-l-y-transition.log`. Maintien continu L numérique + analogique pendant 30 secondes réelles, sauvegarde `slow-await-y.sav`. Une capture demandée immédiatement avant la pause n'était pas encore produite ; `step l=1 l_analog=1 --frames 5 --capture slow-await-y-visible.png` a permis de vérifier visuellement le nouvel écran « PUNCH », avec l'explication du renvoi des projectiles sous Slow. Le précédent écran HOLD DOWN L est donc effectivement franchi.

Puis `step l=1 l_analog=1 y=1 --frames 300 --capture slow-after-y-visible.png` : passage visible à l'explication du puissant coup de poing Slow (« heavy damage »), Joe devant un ennemi étourdi. Sauvegarde locale `slow-after-punch.sav`, puis arrêt propre. Aucun patch ni modification de mémoire invitée. Cela valide deux transitions du tutoriel avec le module natif normal, pas la fin du tutoriel ni le jeu complet ; les replis d'instructions du runtime restent possibles.

Prochaine reprise : `slow-after-punch.sav`, lire les prochaines consignes et terminer Tutorial02. Les données, captures et états restent hors Git.

## Reprise et limite d'affichage — 15 octobre 2026

Reprise depuis `slow-after-punch.sav`. Dans cette session, `DISPLAY=:2.0` est déclaré et le socket X2 existe, mais `xdpyinfo -display :2.0` échoue (« unable to open display ») ; le lancement `-X11 --graphics OGL` se termine par « No X11 display found ». Aucun réglage système ou installation effectués. Essai headless du module normal avec `--headless --graphics Null` : le module et le DOL se chargent, le contrôle local fonctionne, mais une capture fournit une image noire et ne permet aucune validation visuelle.

Depuis ce checkpoint, un essai de 300 images avec L+A et un essai de 360 images avec L+Y en headless n'ont pas changé les octets de contrôle de l'objet tutoriel 0x808b54b0 (+5=1, +7=1) ni les indicateurs Slow observés ; ces essais ne permettent pas d'affirmer l'action suivante attendue. Les runs se sont arrêtés proprement. Ceci ne retire pas la preuve visuelle antérieure des transitions HOLD DOWN L → PUNCH et PUNCH → explication du Slow punch ; les fichiers de checkpoint `slow-after-punch.sav` ont été produits avant ce problème d'affichage.

État : aucune compilation ni runtime actif ; verrou libre. Pour reprendre la validation visuelle, il faut un serveur X accessible à la session ou une session locale graphique fonctionnelle. Entre-temps, l'analyse des états et des contrôles peut continuer sans prétendre avoir vu l'écran.
