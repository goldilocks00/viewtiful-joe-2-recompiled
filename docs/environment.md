# Environnement — 16 septembre 2026

- Ubuntu 26.04.1 LTS, architecture x86-64.
- Noyau : 7.0.0-31-generic.
- Git : 2.53.0.
- Python : 3.14.4.
- CMake, Ninja, GCC et Clang : non trouvés dans le PATH.
- Aucun paquet système installé ou modifié durant cette reconnaissance.

## Suite

Python suffit pour commencer à lire l’en-tête et la structure du disque.
Vérifier les prérequis actuels des dépôts officiels de DolRecomp et ModernGekko avant d’installer la chaîne de compilation. Leur compatibilité avec le jeu n’est pas encore établie.

## Vérification du 30 septembre 2026

7-Zip 26.00 disponible. Git et Python présents. CMake, Ninja, GCC et Clang toujours absents du PATH. Aucun paquet installé.

## Chaîne locale ajoutée le 30 septembre 2026

Paquets de développement décompressés dans `build/deps/root` : GCC/G++ 15, CMake 4.2.3, Ninja, pkg-config et dépendances du runtime. Les bibliothèques déjà présentes sur Ubuntu sont réutilisées via des liens locaux. Les compilations de petits programmes C et C++23 ont réussi. Aucun paquet système n’a été installé.

## Ressources après augmentation de la VM

La reprise constate 6 processeurs logiques et environ 11 Gio de RAM utilisable (allocation annoncée : 12 Go), avec environ 8,3 Gio disponibles et aucun swap utilisé. La compilation du runtime est relancée avec 4 tâches simultanées. Les objets existants ont été conservés ; Ninja annonce 359 étapes restantes à la reprise.

## Diagnostic graphique — 1 octobre 2026

Une sonde EGL locale a créé un contexte OpenGL sur le serveur X11 de la session : EGL 1.5 Mesa, OpenGL 4.5, Mesa 26.0.8, renderer `llvmpipe (LLVM 21.1.8, 256 bits)`. Le rendu est logiciel ; l’ajout de CPU/RAM ne fournit pas à lui seul une accélération GPU. Le contexte est disponible malgré l’avertissement DRI3. Journal : `build/egl-environment.log`. Ce diagnostic ne valide pas le rendu du jeu.
