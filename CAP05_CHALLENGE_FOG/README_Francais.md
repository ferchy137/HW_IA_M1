# Orchestrateur InternetWhisper

## Description du Projet

Ce répertoire contient le service **Orchestrateur** du projet InternetWhisper. L’Orchestrateur est un backend basé sur FastAPI qui coordonne la recherche, la récupération et la génération de contexte pour les requêtes des utilisateurs. Il s’intègre à des API externes (Google Custom Search, OpenAI), une base de cache vectoriel Redis et un service de scraping afin de fournir des réponses pertinentes et riches en contexte.

## Explication Technique

Le service Orchestrateur est responsable des tâches suivantes :

* Accepter les requêtes des utilisateurs via une API REST.
* Effectuer des recherches sur le web en utilisant l’API Google Custom Search.
* Extraire et analyser le contenu des pages web pertinentes.
* Segmenter et vectoriser les textes à l’aide d’OpenAI ou d’un service d’embedding externe.
* Mettre en cache et récupérer les embeddings de documents dans Redis pour des recherches par similarité efficaces.
* Diffuser les réponses au frontend à l’aide de Server-Sent Events (SSE).
* Formater le contexte et générer les invites (prompts) pour les modèles de langage (par ex. GPT d’OpenAI).

**Composants clés :**

* `main.py` : Point d’entrée de l’application FastAPI. Gère les requêtes entrantes, orchestre la récupération et diffuse les réponses.
* `retrieval/` : Contient les modules de recherche, scraping, embeddings, mise en cache et segmentation de texte.
* `models/` : Modèles Pydantic pour les données structurées (documents, résultats de recherche).
* `util/` : Modules utilitaires, y compris la configuration des logs.
* `prompt/` : Modèles de prompts pour les LLM.
* `mocks/` : Données simulées pour le développement/test.

## Variables d’Environnement

L’Orchestrateur repose sur plusieurs variables d’environnement pour les clés d’API et la configuration. Copiez le fichier `.env.example` en `.env` et renseignez les valeurs nécessaires :

```sh
cp .env.example .env
```

* Éditez le fichier `.env` et définissez les variables suivantes :

* `HEADER_ACCEPT_ENCODING` : En-tête HTTP pour l'encodage (par défaut : "gzip").

* `HEADER_USER_AGENT` : En-tête HTTP pour le user-agent.

* `GOOGLE_API_HOST` : URL de l’API Google Custom Search.

* `GOOGLE_FIELDS` : Champs à récupérer depuis l’API de Google.

* `GOOGLE_API_KEY` : Votre clé d’API Google Custom Search.

* `GOOGLE_CX` : L’ID de votre moteur de recherche personnalisé Google.

* `OPENAI_API_KEY` : Votre clé d’API OpenAI.

## Exécuter l’Application Localement

**Prérequis :**

* Docker et Docker Compose
* Clés d’API pour Google Custom Search et OpenAI

**Étapes :**

1. Clonez le dépôt et accédez au répertoire du projet.
2. Configurez les variables d’environnement :
   Copiez `.env.example` en `.env` et remplissez vos clés et paramètres.
3. Construisez et lancez les services :

   ```sh
   docker-compose up --build
   ```

Cela lancera les services suivants :

* `orchestrator` : Le backend FastAPI (ce répertoire).
* `frontend` : Le frontend développé avec Streamlit.
* `cache` : Base de données vectorielle Redis.

4. Accédez à l’API et à l’interface frontend :

   * API Orchestrateur : [http://localhost:8000](http://localhost:8000)
   * Interface utilisateur frontend : [http://localhost:8501](http://localhost:8501)

## Définition OpenAPI

L’Orchestrateur expose le point de terminaison suivant :

**GET /streamingSearch**

**Description :**
Diffuse les résultats de recherche et le contexte d’une requête donnée via des Server-Sent Events (SSE).

**Paramètres de requête :**

* `query` (chaîne, requis) : La requête utilisateur à rechercher et à contextualiser.

**Réponse :**
Un flux d’événements, incluant :

* `search` : JSON avec les résultats de recherche.
* `context` : Texte de contexte agrégé.
* `prompt` : L’invite (prompt) envoyée au LLM.
* `token` : Jetons incrémentaux générés par le LLM.

**Exemple de Requête :**

```http
GET /streamingSearch?query=What is LangChain?
Accept: text/event-stream
```

**Exemple de Réponse (SSE) :**

```
event: search
data: {"items": [...]}

event: context
data: "Texte de contexte pertinent..."

event: prompt
data: "Prompt envoyé au LLM..."

event: token
data: "Première partie de la réponse..."

event: token
data: "Partie suivante de la réponse..."
```

Le schéma complet OpenAPI est disponible à l’adresse suivante lorsque le service est en cours d’exécution :
**[http://localhost:8000/docs](http://localhost:8000/docs)**
