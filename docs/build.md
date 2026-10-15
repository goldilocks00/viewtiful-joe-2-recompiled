# Construire Viewtiful Joe 2 Recompiled

Cible actuelle : Linux x86-64, disque GameCube G2VP08 révision 0.
Les données propriétaires, les sources générées et les binaires restent dans les dossiers ignorés par Git.

## Sources et outils

Les révisions exactes du template et de ses dépendances sont dans `config/sources.lock.json`. Le fichier `patches/moderngekko-build-jobs.patch` ajoute la prise en compte de `CMAKE_BUILD_PARALLEL_LEVEL` pour éviter de saturer la mémoire lors de la compilation du module. Il ne modifie pas le jeu. Les deux autres patchs permettent d’activer EGL pour OpenGL sous Linux et évitent l’accès à ImGui absent en mode sans affichage. `tools/fetch_sources.py` applique ces patchs de manière idempotente.

```bash
python3 tools/fetch_sources.py
```

Chaîne standard : CMake, Ninja, pkg-config, GCC avec C11/C++23 et les bibliothèques de développement décrites par le [template officiel](https://github.com/ExpansionPak/ModernGekko-Template).

### Environnement local de cette VM

`build/deps/root` contient les paquets Ubuntu décompressés localement. Rien n’est installé dans `/usr` et aucun `sudo` n’est nécessaire.

```bash
python3 tools/bootstrap_deps.py
source tools/local-env.sh
```

Cette méthode vise Ubuntu 26.04 amd64 et dépend des bibliothèques d’exécution déjà installées sur la machine, ainsi que du paquet `cpp-15-x86-64-linux-gnu`. Ce n’est pas un SDK autonome ou portable. Les paquets téléchargés sont épinglés avec taille et SHA-256 dans `config/ubuntu-26.04-deps.json`. Une URL devenue indisponible nécessite une mise à jour explicite du manifeste.

## Reconstruction

Depuis la racine du projet :

```bash
tools/project.sh tools
# Uniquement si les fichiers du jeu ne sont pas déjà extraits :
tools/project.sh prepare '/chemin/vers/le/disque.ciso'
tools/project.sh build
tools/project.sh run
```

La préparation refuse d’écraser une extraction existante. La copie ISO de travail est créée avec des blocs nuls pour les blocs absents du CISO : elle ne prétend pas reconstituer un dump original bit pour bit. L’archive et le CISO source sont ouverts en lecture seule.

Par défaut, une seule compilation à la fois. Pour une machine disposant de plus de mémoire :

```bash
CMAKE_BUILD_PARALLEL_LEVEL=2 tools/project.sh build
```

`VJ2_OPT_LEVEL=0` permet un essai sans optimisation ; conserver la même valeur pour `build` et `run`. Le mode par défaut est `2`, sans fast-math, selon les options du module upstream.

Les réglages, sauvegardes et journaux du jeu sont placés dans `build/user`. Les modules sont dans `build/modules`. Les caches sont dans `build/cache`. Aucun fichier de jeu n’est téléchargé par les scripts.

## Vérifications

```bash
python3 -m unittest discover -s tests -v
source tools/local-env.sh
ctest --test-dir build/dolrecomp --output-on-failure
```

L’empreinte du DOL est vérifiée avant construction et lancement. Elle identifie l’exécutable inspecté, pas l’intégralité des ressources du disque.

## Validation du caractère natif

ModernGekko emploie un cœur dérivé de Dolphin pour les périphériques. Son moteur StaticRecomp comporte aussi des chemins de repli interprétés/JIT ; un module chargé ou une fenêtre ouverte ne prouvent donc pas à eux seuls une exécution entièrement native. Lire les compteurs `native`, `fallback`, `hook_fb` et les erreurs SMC dans les journaux de fin d’exécution. Le projet ne force pas `--allow-interpreter`.

## État des essais

Voir `recomp-status.md` pour les résultats effectivement obtenus. Les commandes de lancement décrivent la procédure ; elles ne certifient pas un jeu entièrement fonctionnel.

## Essais bornés et commande locale du jeu

```bash
source tools/local-env.sh
python3 tools/smoke_test.py --headless --seconds 30
# Essai graphique X11/OpenGL :
python3 tools/smoke_test.py --seconds 60
```

Le test enregistre la commande, la sortie, les compteurs natifs et le nombre d’images produit dans `build/logs`. Il utilise un répertoire de contrôle neuf pour chaque essai et refuse les opérations concurrentes. Un succès exige désormais au moins une image produite, une activité native et un arrêt propre. Même en cas de succès, il ne certifie ni le rendu visuel ni le gameplay.

Pour un essai interactif contrôlé par le protocole local de ModernGekko :

```bash
tools/project.sh run -X11 --graphics OGL --automation-dir "$PWD/build/control"
# Dans un second terminal :
python3 tools/game_control.py status
python3 tools/game_control.py screenshot boot.png
python3 tools/game_control.py pad start=1 --frames 3
python3 tools/game_control.py stop
```

Les captures restent dans `build/control/artifacts`, hors Git. Ce mode réserve les entrées manette à l’outil de test ; lancer sans `--automation-dir` pour jouer normalement avec sa configuration manette.

## Clavier et manette

Le lanceur utilise X11/OpenGL par défaut. `tools/prepare_user.py` prépare les dossiers du runtime et copie les profils initiaux uniquement s’ils n’existent pas : clavier et résolution interne native `640x528` (EFB 1x). Les réglages existants sont conservés. Le réglage upstream 1920x1080 active EFB 3x et peut ralentir fortement le rendu logiciel. Profil destiné au périphérique X11 standard `XInput2/0/Virtual core pointer` :

| Entrée GameCube | Touche |
| --- | --- |
| Stick principal | Flèches |
| A / B / X / Y | Espace / X / C / V |
| Z / Start | Z / Entrée |
| L / R | Q / E |
| Stick C | I / J / K / L |
| Croix directionnelle | W / A / S / D |

Ces bindings restent à confirmer dans le jeu. Ils ne remplacent pas le profil d’une manette physique. Les périphériques peuvent être configurés dans `build/user/Config/GCPadNew.ini` au format Dolphin. Le mode de test `--automation-dir` prend la main sur les entrées.

## Points de reprise des essais

Le protocole accepte aussi `python3 tools/game_control.py save_state essai.sav` et `load_state essai.sav`. Ces fichiers restent sous `build/control/artifacts/`. La création et la restauration au démarrage de `tutorial-start.sav` ont été vérifiées avec le module natif. Pour reprendre directement : ajouter `--load-state "$PWD/build/control/artifacts/tutorial-start.sav"` au lancement. Ils ne constituent pas une sauvegarde normale du jeu. Pour les essais de stick, utiliser d’abord `main_y=-0.7` (bas) ou `main_y=0.7` (haut) : les valeurs extrêmes n’ont pas répondu comme attendu dans le tutoriel.

### Avancer puis suspendre l'essai

Pour examiner les captures sans laisser les ennemis attaquer pendant l'analyse :

```bash
python3 tools/game_control.py step main_x=0.7 a=1 --frames 65 --capture saut-01.png
```

La commande reprend le moteur, applique l'entrée pendant 1 à 600 images, demande une capture, libère les boutons pendant trois images puis suspend le moteur. Elle attend la capture et la confirmation de pause (limite de 60 secondes). Utiliser un nom PNG neuf et attendre que la file des commandes précédentes soit vide. En cas de délai dépassé, inspecter le statut et la file avant de recommencer. Le temps du jeu avance de trois images supplémentaires après l'entrée ; cette pause est distincte du menu Start du jeu.

## Diagnostic des entrées

`VJ2_TRACE_PAD=1 tools/project.sh run ...` active le patch `recompcore-pad-trace.patch`. Il journalise le port 0 toutes les 60 lectures, au maximum 256 lignes par processus. Sans cette variable exacte, aucune trace. Les valeurs représentent la lecture manette côté moteur, pas la consommation par le code du jeu. Les journaux restent dans `build/logs`.

`VJ2_TRACE_TUTORIAL_ENTRY=1` active une trace bornée à 32 entrées de dispatch aux adresses 0x80138a60 et 0x80139eac (PC, r3, LR), via `recompcore-tutorial-entry-trace.patch`. Elle ne voit pas les branches internes aux blocs générés ; aucune ligne ne prouve donc pas l'absence d'appel. Désactivée par défaut, sans écriture de registre ou de mémoire invitée.
