# Structure du disque — Viewtiful Joe 2

- Exécutable principal (main.dol) à l’offset logique `0x20000` ; hors de la FST.
- Point d’entrée : `0x80003100`.
- FST : offset `0x337200`, 5606 octets.
- 226 fichiers et 15 dossiers, hors racine.
- Aucun fichier portant les extensions .rel, .dol, .elf, .rso ou .map dans la FST. Cela n’exclut pas du code embarqué dans d’autres conteneurs.

## Sections du DOL

| Section | Offset dans DOL | Adresse mémoire | Taille |
| --- | --- | --- | --- |
| text0 | 0x100 | 0x80003100 | 928 |
| text1 | 0x4A0 | 0x800034A0 | 2813152 |
| data0 | 0x2AF180 | 0x802B2180 | 140832 |
| data1 | 0x2D17A0 | 0x802D47A0 | 278688 |
| data2 | 0x315840 | 0x80451EC0 | 2656 |
| data3 | 0x3162A0 | 0x80452F00 | 3840 |

BSS : `0x80318840`, 1287845 octets (non stockés dans le DOL).

## Fichiers les plus volumineux

| Chemin | Octets |
| --- | --- |
| movie/opu.h4m | 126410834 |
| movie/endingu.h4m | 96424302 |
| bgm/st06.afs | 40275968 |
| movie/pl_demo.h4m | 32846127 |
| bgm/st07.afs | 32751616 |
| bgm/st01.afs | 29618176 |
| bgm/st03.afs | 25454592 |
| bgm/st04.afs | 24578048 |
| bgm/st02.afs | 22829056 |
| bgm/st05.afs | 22593536 |

## Indices et limites

Des marqueurs Dolphin SDK sont présents dans le DOL : OS, EXI, SI, DVD, VI, PAD, AI, AR, ARQ, AX, DSP, CARD et GX. Ce sont des indices de bibliothèques, pas des fonctions déjà identifiées.

Un message de diagnostic OSLink relatif aux relocations est présent. Il ne prouve pas que le jeu charge effectivement des modules ; rechercher ses références avant de conclure à l’absence de chargement dynamique.

Les fichiers .afs et .h4m nécessitent une analyse distincte. Aucun désassemblage, test d’exécution, examen des archives internes ni inventaire complet des symboles n’a été effectué.

Lecture du CISO fondée sur le format décrit par [Dolphin CISOBlob](https://github.com/dolphin-emu/dolphin/blob/master/Source/Core/DiscIO/CISOBlob.h), et lecture FST sur [FileSystemGCWii](https://github.com/dolphin-emu/dolphin/blob/master/Source/Core/DiscIO/FileSystemGCWii.cpp).

Inventaire de métadonnées complet : `disc-metadata.json`.
