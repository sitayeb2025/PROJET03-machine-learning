# Prédiction du Churn Client — Telco

Projet de Machine Learning visant à analyser et prédire la résiliation d'abonnement (*churn*) des clients d'un opérateur télécom, à partir du dataset [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn).

## Objectif

- Identifier les facteurs qui poussent un client à résilier son abonnement
- Entraîner un modèle de classification capable de prédire le risque de churn
- Fournir un outil exploitable (dashboard) pour cibler les clients à risque


## Structure du projet

```
Projet3_machine_learning/
├── Data/
│   ├── raw/                        # Données brutes (téléchargées depuis Kaggle)
│   │   └── telco_churn_raw.csv
│   └── processed/                  # Données nettoyées, encodées, séparées
│       ├── telco_churn_train.csv
│       └── telco_churn_test.csv
├── models/
│   └── best_model.joblib           # Modèle final entraîné et optimisé
├── notebooks/
│   ├── 01_exploration.ipynb        # Nettoyage, EDA, préparation des données
│   ├── 02_modelisation.ipynb       # Comparaison de modèles, optimisation
│   ├── 03_validation.ipynb         # Validation croisée et test final
│   └── dashboard.py                # Visualisation / restitution des résultats
├── src/
│   └── download_data.py            # Script de téléchargement des données brutes
├── reports.Documentation 
    └── documentation_projet CHURN.docx      # Exports, graphiques, résultats
├── venv/                           # Environnement virtuel Python (non versionné)
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

### Prérequis

- Python 3.10 ou supérieur


### 1. Cloner le projet

```bash
git clone https://github.com/sitayeb2025/PROJET03-machine-learning.git
cd PROJET03-machine-learning-main
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv venv
```

Sur Windows :
```bash
venv\Scripts\activate
```

Sur macOS / Linux :
```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancer le projet étape par étape

Les étapes doivent être exécutées **dans cet ordre**, chaque étape dépendant du résultat de la précédente.

### Étape 1 — Télécharger les données brutes

```bash
cd src
python download_data.py
```

Télécharge le dataset depuis Kaggle et le place dans `Data/raw/telco_churn_raw.csv`.

### Étape 2 — Exploration et préparation des données

Ouvrir et exécuter entièrement (*Run All*) :

```
notebooks/01_exploration.ipynb
```

Ce notebook nettoie les données, réalise l'analyse exploratoire (EDA) et génère :
- `Data/processed/telco_churn_train.csv`
- `Data/processed/telco_churn_test.csv`

### Étape 3 — Entraînement et sélection du modèle

Ouvrir et exécuter entièrement (*Run All*):

```
notebooks/02_modelisation.ipynb
```

Compare plusieurs algorithmes, optimise le meilleur, et sauvegarde le modèle final dans :
- `models/best_model.joblib`

### Étape 4 — Validation du modèle

Ouvrir et exécuter entièrement (*Run All*) :

```
notebooks/03_validation.ipynb
```

Vérifie la fiabilité du modèle final (validation croisée + test final) avant toute utilisation.

### Étape 5 — Visualiser les résultats

```bash
cd notebooks
streamlit run dashboard.py
```