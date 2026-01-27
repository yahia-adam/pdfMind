# Backend - QualiBat API

Ce dossier contient le backend de l'application QualiBat, une API FastAPI avec un système RAG (Retrieval-Augmented Generation).

## 📋 Prérequis

- **Python** >= 3.12
- **UV** (recommandé pour la gestion des dépendances)

## 🚀 Installation & Démarrage

### Avec Docker

1. installer avec docker
    ```bash
    docker build -t qualibat-backend .
    docker run -p 8000:8000 --env-file .env qualibat-backend
    ```

### Localement

1.  **Installer les dépendances**
    ```bash
    uv sync
    ```
    *Ou avec pip :*
    ```bash
    pip install .
    ```

2.  **Configuration**
    Créez un fichier `.env` dans ce dossier (voir `.env.example`) et configurez vos clés API et chemins.
    ```env
    # Exemple de variables d'environnement
    DEBUG_MODE=True
    ```

3.  **Initialisation du RAG**
    Avant de lancer l'API, construisez la base de données vectorielle :
    ```bash
    python -m src.build_rag
    ```

4.  **Lancer le serveur**
    ```bash
    fastapi dev src/fast_api.py
    ```
    Le serveur sera accessible à : `http://localhost:8000`


## 📚 Documentation de l'API

### 1. Health Check
- **URL** : `/health`
- **Méthode** : `GET`
- **Description**: Vérifie que le modèle et le retriever sont prêts.

### 2. Poser une question (/ask)
- **URL** : `/ask`
- **Méthode** : `POST`
- **Content-Type** : `application/json`
- **Corps** : `{"question": "Votre question ici"}`
- **Exemple de requête** :
  ```bash
  curl -X POST "http://localhost:8000/ask" \
       -H "Content-Type: application/json" \
       -d '{"question": "Quel est le code de qualification pour la maçonnerie ?"}'
  ```
