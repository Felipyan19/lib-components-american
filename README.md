# lib-components-american

Microservicio REST que expone la librería de componentes HTML para emails AMEX Argentina.
Pensado para integrarse con flujos de n8n que convierten PDFs en emails HTML ensamblando bloques como fichas de Lego.

## Estructura

```
lib-components-american/
├── api/
│   ├── app.py              # Flask app
│   ├── Dockerfile
│   └── requirements.txt
├── libs/
│   └── components/
│       ├── catalog.json    # Registro de todos los componentes
│       ├── hero-banner/
│       ├── brand-panel/
│       └── ...             # 33 componentes en total
└── docker-compose.yml
```

## Levantar

```bash
docker compose up --build
```

El servicio queda disponible en `http://localhost:5050`.

## Endpoints

### 1. Listar todos los componentes
```
GET /components
```
Devuelve el `catalog.json` completo con metadata visual de cada componente.
Útil para pasarle al OCR/LLM como contexto para categorizar un PDF.

```bash
curl http://localhost:5050/components
```

---

### 2. Listar variantes de un componente
```
GET /components/<folder>
```
Devuelve los archivos HTML disponibles en esa carpeta junto con su metadata del catálogo.
Útil para que el LLM elija qué variante usar (ej: v4.0 vs v4.2).

```bash
curl http://localhost:5050/components/hero-banner
curl http://localhost:5050/components/hotel-card
```

---

### 3. Obtener HTML puro de un componente
```
GET /html/<id>
```
Devuelve el HTML listo para usar, identificado por su `id` del catálogo.

```bash
curl http://localhost:5050/html/hero-banner-overlay-v42
curl http://localhost:5050/html/brand-panel-gold
curl http://localhost:5050/html/footer-combined
```

---

### 4. Obtener página 1 de un PDF como PNG
```
GET /pdf/page-1?pdf_url=<url-encoded>
POST /pdf/page-1
```
Devuelve la página 1 renderizada en `image/png`.
Útil para OCR por imagen (Claude Image Analyze) cuando el PDF completo falla o pesa demasiado.

Ejemplo GET:
```bash
curl "http://localhost:5050/pdf/page-1?pdf_url=https%3A%2F%2Fdocs.149-130-164-187.sslip.io%2Ffiles%2Fdownload%2Fby-name%2FMERCHANT-Newsletter-Dic25_promos%2520en%2520imagenes.pdf" -o page1.png
```

Ejemplo POST:
```bash
curl -X POST http://localhost:5050/pdf/page-1 \
  -H "Content-Type: application/json" \
  -d '{"pdf_url":"https://docs.149-130-164-187.sslip.io/files/download/by-name/MERCHANT-Newsletter-Dic25_promos%20en%20imagenes.pdf"}' \
  -o page1.png
```

## Flujo n8n

```
PDF → OCR (GET /components como contexto)
    → LLM elige componentes por tipo
    → OCR variante (GET /components/<folder>)
    → LLM elige id específico
    → GET /html/<id> × N bloques
    → Concatenar → Email HTML final
```
