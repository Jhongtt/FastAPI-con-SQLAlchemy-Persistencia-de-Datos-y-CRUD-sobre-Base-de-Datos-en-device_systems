
# device_systems

API REST para la gestión de usuarios desarrollada con **FastAPI**, **SQLAlchemy** y **Pydantic v2**. Implementa operaciones CRUD completas con persistencia en base de datos SQLite, validaciones, constraints, manejo profesional de errores, Dependency Injection y documentación automática Swagger/OpenAPI.

## Tecnologías utilizadas

- **Python 3.10+**
- **FastAPI** — Framework web moderno y rápido
- **Uvicorn** — Servidor ASGI
- **SQLAlchemy** — ORM para persistencia en base de datos
- **Pydantic v2** — Validación de datos y modelos (schemas)
- **SQLite** — Base de datos ligera embebida
- **Swagger UI / ReDoc** — Documentación interactiva automática

## Requisitos

- Python 3.10+
- Editor de código (VS Code, PyCharm, etc.)
- Cliente HTTP (Postman, Thunder Client, curl)
- Git y GitHub

## Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd device_systems

# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución del servidor

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

El servidor arranca en `http://127.0.0.1:8000`. La base de datos SQLite se crea automáticamente al iniciar.

## Documentación interactiva

| Herramienta | URL |
|-------------|-----|
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |

## Endpoints

| Método | Ruta | Descripción | Códigos de respuesta |
|--------|------|-------------|---------------------|
| `GET` | `/users` | Listar todos los usuarios (con paginación, filtros y ordenamiento) | `200` |
| `GET` | `/users/{user_id}` | Obtener un usuario por ID | `200`, `404` |
| `POST` | `/users` | Crear un nuevo usuario | `201`, `400`, `422` |
| `PUT` | `/users/{user_id}` | Actualizar un usuario completamente (todos los campos requeridos) | `200`, `400`, `404`, `422` |
| `PATCH` | `/users/{user_id}` | Actualizar un usuario parcialmente (solo campos enviados) | `200`, `400`, `404`, `422` |
| `DELETE` | `/users/{user_id}` | Eliminar un usuario | `204`, `404` |

### Códigos de estado HTTP utilizados

| Código | Descripción |
|--------|-------------|
| `200 OK` | Operación exitosa (GET, PUT, PATCH) |
| `201 Created` | Recurso creado exitosamente (POST) |
| `204 No Content` | Recurso eliminado sin cuerpo de respuesta (DELETE) |
| `400 Bad Request` | Error del cliente (correo duplicado, rol inválido, PATCH sin datos) |
| `404 Not Found` | Recurso no encontrado |
| `422 Unprocessable Entity` | Error de validación de datos (Pydantic) |

### Parámetros de consulta (`GET /users`)

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `skip` | `int` | Número de registros a saltar (defecto: 0) |
| `limit` | `int` | Máximo de registros a retornar (defecto: 10, máx: 100) |
| `role` | `str` | Filtrar por rol (`admin`, `support`, `user`) |
| `is_active` | `bool` | Filtrar por estado activo/inactivo |
| `sort_by` | `str` | Ordenar por campo (`name`, `created_at`) |
| `sort_order` | `str` | Dirección del orden (`asc`, `desc`) |

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── __init__.py
│   ├── main.py                            # Punto de entrada, configuración y creación de tablas
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py                  # Engine, SessionLocal, Base declarativa
│   ├── models/
│   │   ├── __init__.py
│   │   └── user_model.py                  # Modelo SQLAlchemy User
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py                 # Schemas Pydantic (UserCreate, UserUpdate, UserUpdateFull, UserResponse)
│   │   └── response_schema.py             # Modelo de respuesta estandarizado
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py               # Lógica de negocio CRUD con SQLAlchemy
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py                # Definición de endpoints con inyección de DB
│   └── dependencies/
│       ├── __init__.py
│       ├── database_dependency.py         # Dependencia get_db() para sesiones de BD
│       └── user_dependencies.py           # Validaciones (rol, config)
├── requirements.txt
└── README.md
```

## Cambios respecto a la versión anterior

| Aspecto | Versión anterior (v2) | Versión actual (v3) |
|---------|----------------------|---------------------|
| Almacenamiento | En memoria (lista de diccionarios) | Base de datos SQLite con SQLAlchemy |
| Modelo de datos | Diccionarios Python | Modelo SQLAlchemy `User` con tipos y constraints |
| Operaciones CRUD | Manipulación directa de listas | Consultas ORM con sesión de base de datos |
| Dependencia de BD | No existía | `get_db()` inyectada con `Depends()` |
| Ordenamiento | No soportado | Por nombre o fecha de creación |
| Archivo `data/` | `app/data/users_db.py` | Eliminado (reemplazado por BD) |

## Diferencia entre modelo SQLAlchemy y schema Pydantic

- **Modelo SQLAlchemy** (`app/models/user_model.py`): Define la estructura de la tabla en la base de datos. Incluye tipos de datos SQL (`Column(Integer)`, `Column(String)`), restricciones (`nullable=False`, `unique=True`, `primary_key=True`) y valores por defecto. Representa cómo se almacenan y relacionan los datos a nivel de base de datos.

- **Schema Pydantic** (`app/schemas/user_schema.py`): Define la estructura de los datos que entran y salen de la API. Incluye validaciones de dominio (`min_length=3`, formato de email, roles permitidos), documentación para Swagger y serialización/deserialización JSON. Controla qué datos expone la API al cliente.

Ambos son complementarios: el modelo SQLAlchemy se encarga de la persistencia, mientras que el schema Pydantic se encarga de la validación y presentación de datos.

## Dependency Injection con Depends()

Se aplicó **Dependency Injection** para inyectar la sesión de base de datos y validaciones en los endpoints usando `Depends()`.

### Dependencias implementadas

| Función | Descripción |
|---------|-------------|
| `get_db()` | Entrega una sesión de SQLAlchemy y la cierra automáticamente al finalizar |
| `validate_role_allowed(role)` | Valida que el rol sea uno de los permitidos (`admin`, `support`, `user`) |
| `get_api_config()` | Retorna configuración general de la API |

## Manejo de errores implementado

La API utiliza `HTTPException` de FastAPI para manejar errores de forma profesional:

- **Usuario no encontrado** — `HTTPException(404)` en `user_service.get_user()` y `user_service.delete_user()`
- **Correo duplicado** — `HTTPException(400)` en `user_service.create_user()` y `user_service.update_user()`
- **Rol no permitido** — `HTTPException(400)` en `validate_role_allowed()`
- **PATCH sin datos** — `HTTPException(400)` verificado directamente en la ruta
- **Datos inválidos** — Validación automática de Pydantic devuelve `422 Unprocessable Entity`

## Cabeceras HTTP personalizadas

Todas las respuestas incluyen:

- `X-App-Name: device_systems`
- `X-API-Version: 3.0`

## Reflexión final

La incorporación de **SQLAlchemy** y persistencia en base de datos transformó `device_systems` de una API con datos volátiles en memoria a una aplicación robusta con almacenamiento permanente. Las principales ventajas de usar un ORM y base de datos relacional en una API REST son:

1. **Persistencia real**: Los datos sobreviven a reinicios del servidor.
2. **Integridad referencial**: Constraints como `unique=True` y `nullable=False` garantizan calidad de datos.
3. **Consultas optimizadas**: El ORM permite filtrado, ordenamiento y paginación eficientes.
4. **Separación de responsabilidades**: Modelos SQLAlchemy para BD, schemas Pydantic para API.
5. **Escalabilidad**: La misma lógica puede migrarse a PostgreSQL, MySQL u otros motores cambiando solo la URL de conexión.
6. **Transacciones**: Las operaciones CRUD se ejecutan dentro de sesiones con commit/rollback.
