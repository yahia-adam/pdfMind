# QualiBat

Ce projet est un chatbot RAG (Retrieval-Augmented Generation) conçu pour répondre aux questions sur les codes de qualification pour les artisans du bâtiment (Qualibat, RGE, Normes).

## 📂 Structure du projet

- **[backend/](./backend/README.md)** : API FastAPI, logique RAG, et gestion de la base vectorielle (ChromaDB).
- **[frontend/](./frontend/README.md)** : Interface utilisateur Next.js pour discuter avec le chatbot.
- **docker-compose.yml** : Orchestration des conteneurs pour un déploiement facile.

## 🚀 Démarrage Rapide (Docker)

La méthode la plus simple pour lancer le projet est d'utiliser Docker Compose.

1.  **Prérequis** : Assurez-vous d'avoir Docker et Docker Compose installés.

2.  **Configuration** :
    Créez un fichier `.env` à la racine (voir `.env.example`).
    ```env
    OPENAI_API_KEY=votre_clé_api
    # Autres configurations...
    ```

3.  **Lancer l'application** :
    ```bash
    docker-compose up --build
    ```

4.  **Accéder à l'application** :
    - **Frontend (Chat)** : [http://localhost:3000](http://localhost:3000)
    - **Backend (Docs API)** : [http://localhost:8000/docs](http://localhost:8000/docs)

## 🛠️ Développement Local

Pour travailler sur le backend ou le frontend individuellement, consultez leurs README respectifs :
- [Documentation Backend](./backend/README.md)
- [Documentation Frontend](./frontend/README.md)