Aquí tienes la traducción completa al español:

# Orquestador de InternetWhisper

## Descripción del Proyecto

Este directorio contiene el servicio **Orchestrator** del proyecto InternetWhisper. El Orquestador es un backend basado en FastAPI que coordina la búsqueda, recuperación y generación de contexto para consultas de usuarios. Se integra con APIs externas (Google Custom Search, OpenAI), una caché vectorial en Redis y un servicio de scraping para proporcionar respuestas relevantes y ricas en contexto a las preguntas de los usuarios.

## Explicación Técnica

El servicio Orquestador es responsable de:

* Aceptar consultas de usuarios a través de una API REST.
* Buscar en la web usando la API de Google Custom Search.
* Extraer y analizar páginas web para obtener contenido relevante.
* Dividir e incrustar texto utilizando OpenAI u otros servicios remotos de embedding.
* Almacenar y recuperar embeddings de documentos en Redis para búsquedas por similitud eficientes.
* Transmitir respuestas al frontend utilizando Server-Sent Events (SSE).
* Formatear el contexto y generar prompts para LLMs (por ejemplo, OpenAI GPT).

**Componentes Clave:**

* `main.py`: Punto de entrada de la aplicación FastAPI. Maneja las solicitudes entrantes, orquesta la recuperación y transmite respuestas.
* `retrieval/`: Contiene módulos para búsqueda, scraping, embeddings, caché y división de texto.
* `models/`: Modelos Pydantic para datos estructurados (documentos, resultados de búsqueda).
* `util/`: Módulos utilitarios, incluyendo la configuración de logs.
* `prompt/`: Plantillas de prompts para modelos de lenguaje.
* `mocks/`: Datos simulados para desarrollo/pruebas.

## Variables de Entorno

El Orquestador depende de varias variables de entorno para llaves de API y configuración. Copia `.env.example` a `.env` y completa los valores requeridos:

```sh
cp .env.example .env
```

* Edita el archivo `.env` y configura las siguientes variables:

* `HEADER_ACCEPT_ENCODING`: Cabecera HTTP para codificación (por defecto: "gzip").

* `HEADER_USER_AGENT`: Cabecera HTTP con el user-agent.

* `GOOGLE_API_HOST`: Endpoint de la API de Google Custom Search.

* `GOOGLE_FIELDS`: Campos que se deben obtener de la API de Google.

* `GOOGLE_API_KEY`: Tu clave de API de Google Custom Search.

* `GOOGLE_CX`: Tu ID del motor de búsqueda personalizado de Google.

* `OPENAI_API_KEY`: Tu clave de API de OpenAI.

## Ejecutar la Aplicación Localmente

**Requisitos previos:**

* Docker y Docker Compose
* Llaves de API para Google Custom Search y OpenAI

**Pasos:**

1. Clona el repositorio y navega al directorio del proyecto.
2. Configura las variables de entorno:
   Copia `.env.example` a `.env` y rellena tus llaves y configuración.
3. Construye e inicia los servicios:

   ```sh
   docker-compose up --build
   ```

Esto iniciará los siguientes servicios:

* `orchestrator`: El backend FastAPI (este directorio).
* `frontend`: El frontend desarrollado en Streamlit.
* `cache`: Base de datos vectorial Redis.

4. Accede a la API y al frontend:

   * API del Orquestador: [http://localhost:8000](http://localhost:8000)
   * Interfaz del frontend: [http://localhost:8501](http://localhost:8501)

## Definición OpenAPI

El Orquestador expone el siguiente endpoint de la API:

**GET /streamingSearch**

**Descripción:**
Transmite resultados de búsqueda y contexto para una consulta utilizando Server-Sent Events (SSE).

**Parámetros de Consulta:**

* `query` (string, requerido): La consulta del usuario para buscar y recuperar contexto.

**Respuesta:**
Una secuencia de eventos que incluye:

* `search`: JSON con los resultados de búsqueda.
* `context`: Texto agregado del contexto.
* `prompt`: El prompt enviado al modelo LLM.
* `token`: Tokens incrementales de la respuesta del LLM.

**Ejemplo de Solicitud:**

```http
GET /streamingSearch?query=What is LangChain?
Accept: text/event-stream
```

**Ejemplo de Respuesta (SSE):**

```
event: search
data: {"items": [...]}

event: context
data: "Texto de contexto relevante..."

event: prompt
data: "Prompt enviado al LLM..."

event: token
data: "Primera parte de la respuesta..."

event: token
data: "Siguiente parte de la respuesta..."
```

El esquema completo de OpenAPI está disponible en `http://localhost:8000/docs` cuando el servicio está en ejecución.
