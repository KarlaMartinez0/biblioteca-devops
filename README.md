## 🧪 Ejecutar las pruebas localmente

Desde la raíz del repositorio:

```bash
pip install -r app/requerimientos.txt
python -m pytest -v
```

> Si no hay un PostgreSQL accesible, la aplicación usa automáticamente una base SQLite en memoria como respaldo, por lo que las pruebas se pueden ejecutar sin configurar nada más.
>
> Para correrlas contra PostgreSQL real (como en GitHub Actions), definir antes las variables `DB_HOST`, `DB_NAME`, `DB_USER` y `DB_PASSWORD`, y crear la tabla con `db/init.sql`.

### Categorías de pruebas

| Categoría | Archivo | Qué verifica |
| --- | --- | --- |
| **Unitarias** | `tests/test_unit.py` | La función `validar_libro` de forma aislada: título vacío, autor vacío y datos completos. |
| **Integración** | `tests/test_integration.py` | Que las rutas de la aplicación respondan correctamente: página principal, formulario de nuevo libro, búsqueda por autor y filtro de disponibles. |

Al ejecutar toda la suite después de cada cambio, estas pruebas también actúan como **pruebas de regresión**: si una modificación rompe algo que antes funcionaba, alguna prueba fallará.

---

## ⚙️ Workflows de GitHub Actions

| Workflow | Archivo | Se activa con | Qué hace |
| --- | --- | --- | --- |
| **CI** | `.github/workflows/ci.yml` | Pull request hacia `main` y push a `main` | Instala dependencias, levanta un PostgreSQL de prueba, crea la tabla y ejecuta `pytest`. Si una prueba falla, el workflow queda en rojo. |
| **CD** | `.github/workflows/cd.yml` | Push a `main` (incluye el merge de un PR) | Job `test`: vuelve a correr las pruebas. Job `build-and-push`: **solo si `test` pasó**, construye la imagen con el `Dockerfile` y la publica en GHCR. |

La imagen **no se publica** si las pruebas fallan, porque el job `build-and-push` depende del job `test` (`needs: test`).

### Flujo completo

```
Código → commit/push → Pull request → CI (pruebas) → merge a main → CD (pruebas + build) → imagen en GHCR → docker pull / run
```

* **Automatizado:** ejecución de pruebas, construcción de la imagen, publicación y etiquetado.
* **Manual:** escribir el código, abrir y aprobar el pull request, y ejecutar la imagen descargada.

---

## 🐳 Imagen publicada en GHCR

```
ghcr.io/karlamartinez0/biblioteca-devops
```

Etiquetas disponibles:

* `latest`: última versión publicada desde `main`.
* `sha-<commit>`: etiqueta asociada al commit que generó la imagen (por ejemplo `sha-1a2b3c4`).

Ver todas las versiones en la pestaña **Packages** del repositorio.

### Descargar la imagen

```bash
docker pull ghcr.io/karlamartinez0/biblioteca-devops:latest
```

### Ejecutar la aplicación a partir de la imagen descargada

La aplicación necesita una base PostgreSQL. La forma más simple es levantar solo el servicio `db` del `docker-compose.yml` y conectar el contenedor a su misma red.

1. Clonar el repositorio (necesario solo para obtener `docker-compose.yml` y `db/init.sql`):

```bash
git clone https://github.com/KarlaMartinez0/biblioteca-devops.git
cd biblioteca-devops
```

2. Levantar únicamente la base de datos:

```bash
docker compose up -d db
```

3. Ejecutar la imagen descargada conectada a esa red:

```bash
docker run -d --name biblioteca-ghcr \
  --network biblioteca-devops_red_biblioteca \
  -p 8080:5000 \
  -e DB_HOST=db \
  -e DB_NAME=biblioteca_db \
  -e DB_USER=postgres \
  -e DB_PASSWORD=postgres_password \
  -e PORT=5000 \
  ghcr.io/karlamartinez0/biblioteca-devops:latest
```

4. Abrir **http://localhost:8080**.

5. Para limpiar:

```bash
docker rm -f biblioteca-ghcr
docker compose down
```

> **Nota:** el nombre de la red (`biblioteca-devops_red_biblioteca`) se forma con el nombre de la carpeta del proyecto. Si se clonó en una carpeta con otro nombre, verificarlo con `docker network ls`.

### Parámetros del contenedor

| Parámetro | Valor | Descripción |
| --- | --- | --- |
| Puerto interno | `5000` | Puerto en el que escucha Flask dentro del contenedor |
| Puerto publicado | `8080` | Puerto del equipo anfitrión (`-p 8080:5000`) |
| `DB_HOST` | `db` | Nombre del servicio de PostgreSQL en la red de Docker |
| `DB_NAME` | `biblioteca_db` | Nombre de la base de datos |
| `DB_USER` | `postgres` | Usuario de la base de datos |
| `DB_PASSWORD` | `postgres_password` | Contraseña de la base de datos |
| `PORT` | `5000` | Puerto de la aplicación |

> Si la imagen es privada, autenticarse antes con `docker login ghcr.io` usando un Personal Access Token con permiso `read:packages`.

---

## 📂 Estructura del proyecto

```
biblioteca-devops/
├── .github/workflows/
│   ├── ci.yml            # Integración continua (pruebas)
│   └── cd.yml            # Entrega continua (build + push a GHCR)
├── app/                  # Código fuente Flask
│   ├── app.py
│   ├── requerimientos.txt
│   └── templates/
├── db/init.sql           # Creación de tabla y datos iniciales
├── tests/                # Pruebas unitarias y de integración
├── .dockerignore
├── docker-compose.yml    # Orquestación local (web + db)
├── Dockerfile            # Construcción de la imagen
└── README.md
```