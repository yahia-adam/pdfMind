# Frontend - QualiBat Interface

Ce dossier contient le frontend de l'application QualiBat, une application Next.js qui permet d'interagir avec l'API RAG.

## 📋 Prérequis

- **Node.js** >= 22
- **NPM**, **Yarn**, **PNPM**, ou **Bun**

## 🚀 Installation & Démarrage

### Localement

1.  **Installer les dépendances**
    ```bash
    npm install
    # ou
    yarn install
    # ou
    pnpm install
    ```

2.  **Configuration**
    Créez un fichier `.env.local` à la racine de ce dossier avec l'URL du backend :
    ```env
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

3.  **Lancer le serveur de développement**
    ```bash
    npm run dev
    # ou
    yarn dev
    # ou
    pnpm dev
    ```
    Ouvrez [http://localhost:3000](http://localhost:3000) dans votre navigateur.

### Avec Docker

```bash
docker build -t qualibat-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 qualibat-frontend
```

## 🛠️ Stack Technique

- **Framework**: [Next.js](https://nextjs.org) (App Router)
- **Langage**: TypeScript
- **Styling**: Tailwind CSS, Lucide React
- **Gestionnaire de paquets**: Configuré pour npm/yarn/pnpm
