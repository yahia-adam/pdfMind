# QualiBot

Ce projet est un chatbot qui répond aux questions sur les codes de qualification pour les artisans du bâtiment. 

## 📋 Prérequis

- **Python** >= 3.12
- **UV** (recommandé pour la gestion des dépendances)

## 🚀 Installation

1.  **Cloner le projet**

    ```bash
    git clone git@github.com:yahia-adam/pdfMind.git qualiBot
    cd qualiBot
    ```

2.  **Installer les dépendances**

    ```bash
    uv sync
    ```
    *Ou avec pip :*
    ```bash
    pip install .
    ```

3.  **Configuration**
    Créez un fichier `.env` à la racine du projet (voir `.env.example`) et configurez vos clés API et chemins si nécessaire.

    ```env
    # Exemple de variables d'environnement
    ROOT_DIR=
    APP_NAME=pdfMind
    DEBUG_MODE=True
    ```

## 🤖 Initialisation du chatbot

Pour initialiser le chatbot, il faut d'abord construire le RAG.

```bash
python -m src.pdf_mind.build_rag
```

## 🗄️ Démarrage du serveur

Pour lancer le serveur de développement FastAPI :

```bash
fastapi dev src/pdf_mind/fast_api.py
```

Le serveur sera accessible à l'adresse : `http://127.0.0.1:8000`

### Documentation du serveur

### 1. Vérification du système (Health Check)
Vérifie que le modèle de chat et le retriever sont bien initialisés.

- **URL** : `/health`
- **Méthode** : `GET`
- **Exemple de requête** :
  ```bash
  curl -X GET "http://localhost:8000/health"
  ```
- **Réponse (Succès)** :
  ```json
  {
    "status": "ok",
    "question": "Quel est le code de qualification pour la maçonnerie ?",
    "answer": "La qualification pour la maçonnerie est...",
    "documents": [...]
  }
  ```

### 2. Poser une question (Ask)
interroge le chatbot RAG.

- **URL** : `/ask`
- **Méthode** : `POST`
- **Content-Type** : `application/json`
- **Corps de la requête** :
  ```json
  {
    "question": "Votre question ici"
  }
  ```
- **Exemple de requête** :
  ```bash
  curl -X POST "http://localhost:8000/ask" \
       -H "Content-Type: application/json" \
       -d '{"question": "Quel est le code de qualification pour la maçonnerie ?"}'
  ```
- **Réponse** :
  ```json
  {
      "status_code": 200,
      "response": {
          "answer": "Réponse générée par le modèle...",
          "documents": [
              {
                  "page_content": "Extrait du document source...",
                  "metadata": { "source": "...", "page": 60 }
              }
          ]
      }
  }
  ```

### 3. Accueil
Page d'accueil simple listant les endpoints disponibles.

- **URL** : `/`
- **Méthode** : `GET`


Qu'est-ce que la mention RGE ?
Quel est le code de qualification pour la maçonnerie ?
Quelles sont les activités de la Famille 5 ?
Comment décrypter le code à 4 chiffres ?
Quels travaux nécessitent une certification Amiante ?