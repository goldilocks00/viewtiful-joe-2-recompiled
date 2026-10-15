# Viewtiful Joe 2 Recompiled

## Objectif

Créer un port PC natif de **Viewtiful Joe 2 (Nintendo GameCube)** à partir d’un disque original possédé par le développeur, en utilisant principalement :

- **DolRecomp**
- **ModernGekko**
- CMake / Ninja
- GCC ou Clang
- outils d’analyse GameCube / PowerPC si nécessaire

Le projet doit devenir à terme un projet communautaire propre, documenté et reproductible.

---

## Environnement

OS principal :

- Ubuntu Desktop 26.04 LTS

Machine de développement :

- VM Linux sous Proxmox
- environnement dédié au projet
- snapshots Proxmox recommandés avant modifications importantes

Agent de développement :

- Codex CLI

---

## Principes importants

L’ISO du jeu provient d’un disque original possédé légalement par le développeur.

L’ISO doit rester STRICTEMENT locale.

Ne jamais :

- committer l’ISO
- uploader l’ISO
- copier l’ISO dans GitHub
- publier des fichiers propriétaires extraits du jeu
- publier musiques, textures, vidéos ou autres assets originaux
- modifier l’ISO originale

L’ISO doit idéalement être en lecture seule.

Exemple :

```bash
chmod 444 iso/ViewtifulJoe2.iso
```

Ajouter au `.gitignore` :

```gitignore
iso/
extracted/
build/
*.iso
*.gcm
```

---

# Structure souhaitée

```text
viewtiful-joe-2-recomp/
├── PROJECT.md
├── README.md
├── CMakeLists.txt
├── iso/
│   └── ViewtifulJoe2.iso
├── upstream/
│   ├── DolRecomp/
│   └── ModernGekko/
├── src/
├── patches/
├── config/
├── tools/
├── docs/
├── extracted/
└── build/
```

`iso/`, `extracted/` et `build/` ne doivent jamais être versionnés.

---

# Première mission

NE PAS essayer immédiatement d’ajouter :

- 4K
- widescreen
- 60 FPS
- mods
- nouvelles textures
- améliorations graphiques

Le premier travail doit être une **reconnaissance technique complète du jeu**.

---

## Étape 1 — Identifier précisément l’ISO

Déterminer :

- nom du jeu
- Game ID
- région
- version / révision
- taille du fichier
- MD5
- SHA-1
- SHA-256

Documenter les résultats dans :

```text
docs/game-version.md
```

Ne jamais inclure de données propriétaires inutiles dans ce document.

---

## Étape 2 — Examiner la structure GameCube

Inspecter l’ISO sans la modifier.

Identifier au minimum :

- `main.dol`
- fichiers `.rel`
- DOL secondaires éventuels
- fichiers exécutables particuliers
- structure générale du filesystem
- taille des principales sections
- présence éventuelle de symboles ou fichiers MAP
- bibliothèques Nintendo / Dolphin SDK reconnaissables

Documenter les résultats.

---

## Étape 3 — Évaluer la compatibilité avec DolRecomp

Installer ou compiler la version actuelle de DolRecomp.

Tester le `main.dol`.

Rechercher notamment :

- instructions PPC non prises en charge
- indirect branches problématiques
- appels système particuliers
- self-modifying code
- code chargé dynamiquement
- REL / overlays
- dépendances inhabituelles
- hypothèses sur la mémoire GameCube

Ne jamais masquer silencieusement une erreur.

Chaque workaround doit être documenté.

---

# Premier milestone

Le premier objectif fonctionnel est :

```text
exécutable Linux x86-64
        ↓
initialisation ModernGekko
        ↓
code recompilé
        ↓
logo Capcom
```

Puis :

```text
logo Capcom
    ↓
écran titre
    ↓
menu principal
    ↓
nouvelle partie
    ↓
premier niveau jouable
```

La priorité est la fidélité au comportement original.

---

# Milestones

## v0.1 — Boot

Objectifs :

- compilation reproductible
- lancement natif Linux
- initialisation correcte
- affichage du logo / écran titre

---

## v0.2 — Gameplay

Objectifs :

- menu fonctionnel
- nouvelle partie
- premier niveau jouable
- entrée manette fonctionnelle
- audio basique
- sauvegarde si possible

---

## v0.5 — Vanilla Complete

Objectif principal :

**terminer le jeu intégralement via la recompilation native.**

Doivent être testés :

- tous les niveaux
- cinématiques
- sauvegardes
- chargements
- boss
- transitions
- audio
- effets VFX
- Slow
- Mach Speed (Joe)
- Replay (Silvia)
- Zoom

---

## v0.7 — Port PC

Ajouter progressivement :

- Windows x64
- Linux x64
- Steam Deck
- manettes Xbox
- DualSense
- configuration propre
- gestion moderne des sauvegardes
- résolution configurable

---

## v1.0 — Projet communautaire

Évaluer ensuite :

- 16:9 natif
- ultrawide
- hautes résolutions
- framerate supérieur à l’original si techniquement sûr
- modding
- texture packs
- patches communautaires
- améliorations QoL

Ne jamais modifier le timing ou le framerate sans comprendre les conséquences sur le moteur.

Viewtiful Joe 2 utilise fortement des mécaniques dépendantes du temps :

- Slow
- Mach Speed (Joe)
- Replay (Silvia)
- Zoom

Ces fonctions doivent faire l’objet de tests spécifiques avant toute modification du framerate.

---

# Philosophie de développement

Favoriser :

- modifications petites et compréhensibles
- commits fréquents
- documentation
- reproductibilité
- assertions
- logs explicites
- tests simples
- compréhension avant contournement

Éviter :

- hacks opaques
- énormes modifications non documentées
- désactivation d’erreurs
- modifications simultanées de plusieurs sous-systèmes
- « ça marche donc on garde »

---

# Git

Créer des commits cohérents et petits.

Exemples :

```text
chore: initialize project structure
docs: document supported game revision
build: add DolRecomp dependency
recomp: add initial main.dol configuration
runtime: reach game initialization
runtime: fix memory mapping
video: reach Capcom logo
input: map GameCube controller inputs
```

Ne jamais committer automatiquement une grosse quantité de fichiers générés sans vérifier leur utilité.

---

# Branches

Initialement :

```text
main
```

Pour les développements importants :

```text
feature/*
fix/*
research/*
```

Exemples :

```text
research/main-dol
feature/first-boot
fix/audio-init
```

---

# Documentation

Conserver progressivement :

```text
docs/
├── game-version.md
├── disc-layout.md
├── memory-map.md
├── recomp-status.md
├── known-issues.md
└── reverse-engineering-notes.md
```

---

# Reverse engineering

Ne lancer Ghidra ou d’autres outils lourds que lorsque cela devient réellement utile.

Commencer autant que possible avec :

- outils CLI
- analyse des sections
- symboles
- logs
- traces
- comparaison de comportement
- Dolphin si nécessaire comme référence

Lorsque Ghidra devient nécessaire :

- nommer les fonctions progressivement
- conserver les notes
- documenter les structures découvertes
- éviter de supposer le rôle d’une fonction sans preuve suffisante

---

# Dolphin

Dolphin peut être utilisé comme référence comportementale.

Cas d’usage possibles :

- observer le boot original
- analyser les appels
- comparer le comportement
- vérifier mémoire / registres
- reproduire un crash
- tester les inputs
- comparer audio / vidéo

Le but final reste un port natif, pas un frontend Dolphin.

---

# Distribution future

Ne pas supposer qu’un module recompilé peut être redistribué librement.

La stratégie de distribution préférée est :

```text
utilisateur
    ↓
installe notre launcher
    ↓
sélectionne son ISO original
    ↓
validation de la version
    ↓
génération locale des fichiers nécessaires
    ↓
recompilation locale
    ↓
lancement du jeu
```

Le dépôt public doit contenir uniquement ce qui peut légalement et techniquement être partagé.

---

# Sécurité de l’environnement

Codex peut :

- créer/modifier des fichiers du projet
- utiliser Git
- compiler
- lancer CMake/Ninja
- lancer les outils de recompilation
- analyser les logs
- exécuter le programme recompilé
- documenter les résultats

Codex ne doit pas :

- utiliser `sudo` sans nécessité
- modifier des fichiers système inutilement
- supprimer l’ISO
- modifier l’ISO
- envoyer l’ISO sur Internet
- publier automatiquement sur GitHub
- rendre un repository public sans instruction explicite

---

# Règle pour Codex

Avant une modification importante :

1. comprendre le problème ;
2. expliquer brièvement l’hypothèse ;
3. effectuer une modification minimale ;
4. compiler ;
5. tester ;
6. analyser le résultat ;
7. documenter ;
8. committer uniquement si l’étape est stable.

---

# Première tâche à effectuer maintenant

1. Inspecter l’environnement Linux.
2. Vérifier les outils déjà disponibles.
3. Localiser l’ISO dans `iso/`.
4. Ne PAS modifier l’ISO.
5. Calculer MD5, SHA-1 et SHA-256.
6. Identifier Game ID, région et révision.
7. Examiner le filesystem GameCube.
8. Identifier `main.dol` et tous les `.rel`.
9. Produire `docs/game-version.md`.
10. Produire `docs/disc-layout.md`.
11. Présenter les résultats avant de commencer la recompilation.

Une fois cette phase terminée, évaluer si Viewtiful Joe 2 est un bon candidat pour DolRecomp/ModernGekko et identifier les premiers obstacles techniques concrets.

---

# Instruction initiale pour Codex

Lis intégralement `PROJECT.md`.

Considère ce document comme les règles du projet.

Commence uniquement par la phase de reconnaissance de l’ISO et de l’environnement.

Ne modifie jamais l’ISO.

Ne cherche pas encore à ajouter d’améliorations au jeu.

Documente ce que tu découvres et travaille progressivement jusqu’à obtenir suffisamment d’informations pour préparer la première tentative DolRecomp.
## Adaptation au deuxième jeu

Tester également le changement Joe/Silvia, les armes de Silvia et Replay. Ces points complètent le cadrage initial. Référence descriptive : [test GameSpot de Viewtiful Joe 2](https://www.gamespot.com/reviews/viewtiful-joe-2-review/1900-6113677/).
