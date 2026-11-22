# PulseTrack — Suivi d'Habitudes & Bilan Visuel

**PulseTrack** est une application web conçue pour suivre ses routines quotidiennes (sport, lecture, hydratation, sommeil, projets personnels), visualiser sa régularité sur 84 jours, suivre ses séries de jours consécutifs (*streaks*) et identifier automatiquement sa meilleure semaine.

## Fonctionnalités

* **Checklist quotidienne interactive** : cochez vos routines du jour avec calcul en temps réel du taux de complétion et barre de progression.
* **Séries consécutives (*Streaks*)** : suivi automatique des jours d'affilée par habitude et mise en avant de la meilleure série globale.
* **Bilan automatique de la meilleure semaine** : analyse des 12 dernières semaines pour détecter la semaine la plus régulière, son taux de réussite, le nombre d'actions validées et l'habitude pilier.
* **Calendrier de régularité (84 jours)** : grille visuelle sur 12 semaines graduée selon l'intensité quotidienne.
* **Gestion des routines** : ajout de nouvelles habitudes avec sélection d'icônes **Flaticon UIcons** et suppression d'habitudes existantes.
* **Mode Jour / Mode Nuit** : basculeur de thème persistant (`localStorage`) dans une palette **Noir, Blanc & Midnight Blue** avec surfaces semi-transparentes lisibles et animations fluides.
* **Persistance locale JSON** : sauvegarde automatique des habitudes et de l'historique dans `data.json` via volume Docker.

## Stack technique

* **Backend** : Python, Flask, Gunicorn
* **Frontend** : HTML5, Tailwind CSS, JavaScript (Vanilla), Flaticon UIcons
* **Conteneurisation** : Docker & script `run.sh`

## Structure du projet

```text
pulsetrack/
├── Dockerfile
├── run.sh
├── app.py
├── data.json
└── templates/
    └── index.html
```

## Démarrage rapide avec Docker

1. Cloner le dépôt et se placer dans le dossier du projet :
   ```bash
   git clone <url-du-repo>
   cd pulsetrack
   ```

2. Rendre le script exécutable et lancer le build + conteneur :
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

3. Ouvrir l'application dans le navigateur :
   ```text
   http://localhost:5000
   ```
   *(Modifiez la variable `PORT` dans `run.sh` si le port `5000` est déjà utilisé sur votre machine.)*
