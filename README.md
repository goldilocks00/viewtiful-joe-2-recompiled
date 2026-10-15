# Viewtiful Joe 2 Recompiled

Projet expérimental de port Linux x86-64 de Viewtiful Joe 2 GameCube, version Europe/PAL G2VP08 révision 0.

## État vérifié

- Disque identifié et extrait localement ; 226 fichiers et main.dol contrôlés contre le CISO.
- DolRecomp compilé, 19 tests réussis ; génération de 173 fragments C sans instruction inconnue signalée.
- Runtime et module natif construits ; logo Capcom, écran titre et menus affichés.
- Premiers combats et déplacements testés ; progression actuellement bloquée sur la démonstration du tutoriel Slow (Tutorial 02).
- Audio initialisé et signal détecté ; qualité audio, sauvegardes sur carte mémoire, premier niveau complet et reste du jeu non validés : voir [l’état détaillé](docs/recomp-status.md).

Aucun statut de jeu complet ou de port intégralement natif n’est revendiqué avant validation.

## Commandes

```bash
python3 tools/fetch_sources.py
# Option locale, uniquement pour cette base Ubuntu 26.04 amd64 :
python3 tools/bootstrap_deps.py
tools/project.sh tools
# À faire seulement lors de la première extraction :
tools/project.sh prepare '/chemin/vers/disque.ciso'
tools/project.sh build
tools/project.sh run
```

Consulter [la procédure de construction](docs/build.md), [la version du jeu](docs/game-version.md), [la structure du disque](docs/disc-layout.md) et [les problèmes connus](docs/known-issues.md).

## Données locales

Aucun jeu n’est téléchargé par le projet. `iso/`, `extracted/`, `build/` et `upstream/` sont exclus de Git. L’archive originale reste inchangée. Les modules recompilés et les ressources du jeu ne font pas partie du dépôt.

Le dossier conserve son nom initial `viewtiful-joe-recomp` ; le périmètre concerne uniquement le deuxième jeu.

## Partage et contributions

Voir [la préparation au partage](docs/sharing.md), [les contributions](CONTRIBUTING.md), [la licence](LICENSE) et [les attributions](NOTICE).
