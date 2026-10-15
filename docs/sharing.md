# Partager le projet

Le dépôt contient les outils écrits pour ce projet, les correctifs du runtime et la documentation. Chaque utilisateur prépare ses propres données du jeu localement. Les binaires du jeu recompilé, les captures, les sauvegardes, le disque, les ressources extraites et les sources C générées restent hors Git.

Avant un push, depuis la racine du projet :

```bash
python3 -m unittest discover -s tests -v
python3 tools/audit_share.py
git diff --cached --check
git status --short
```

L’audit examine l’index et les arbres de tous les commits accessibles : dossiers locaux interdits, formats attendus, taille et texte UTF-8. Il ne certifie pas l’absence de tout contenu sensible ou propriétaire dans un fichier texte ; relire les fichiers destinés au partage reste nécessaire. Ne pas utiliser `git add -f` pour inclure un dossier ignoré.

Le dépôt est expérimental. Le README et `docs/validation.md` doivent décrire les essais effectivement réalisés. Ne pas présenter un écran titre fonctionnel comme un jeu entièrement validé.

Aucun dépôt distant n’est configuré à ce stade. Une fois le dépôt GitHub créé par son propriétaire, ajouter son URL comme remote `origin`, vérifier `git remote -v`, puis pousser la branche `main`. Ne pas joindre les dossiers locaux aux releases GitHub.

Les dépendances sont récupérées à leurs révisions épinglées, sans être recopiées dans le dépôt. `LICENSE` contient la GPL version 3 pour les scripts et documents originaux ; `NOTICE` identifie les dépendances et les licences propres aux correctifs. Les notices amont restent applicables aux composants récupérés.
