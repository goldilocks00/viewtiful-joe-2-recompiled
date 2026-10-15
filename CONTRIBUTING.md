# Contribuer

Commencer par `docs/build.md`, `docs/recomp-status.md` et `docs/validation.md`.
La cible validée pour l’extraction est G2VP08 révision 0 ; annoncer explicitement
une autre révision dans toute proposition et ne pas remplacer silencieusement
les empreintes de référence.

Pour un correctif, fournir le problème observé, les étapes de reproduction,
les versions des outils et le résultat avant/après. Indiquer les compteurs
`native`, `fallback`, `hook_fb` et `smc_failed` lorsque le changement touche
l’exécution. Un correctif de rendu doit préciser le backend et la résolution.

Les tests des outils utilisent des données synthétiques :

```bash
python3 -m unittest discover -s tests -v
python3 tools/audit_share.py
```

Ne pas joindre le disque, les ressources extraites, les sources générées,
les sauvegardes ou les binaires du jeu aux commits et rapports. Relire les
journaux avant de les partager. Les captures des essais locaux restent dans
`build/`, hors Git. Conserver les notices des composants amont ; voir NOTICE.

Le projet n’a pas encore validé une partie complète. Un domaine non testé
reste indiqué comme tel, même si le démarrage fonctionne.
