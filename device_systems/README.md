
# device_systems

API REST para la gestión de usuarios desarrollada con **FastAPI** y **Pydantic 2**. Implementa operaciones CRUD completas con validación de datos, modelos de respuesta estandarizados, manejo profesional de errores, Dependency Injection y documentación automática Swagger/OpenAPI.

## Tecnologías utilizadas

- **Python 3.10+**
- **FastAPI** — Framework web moderno y rápido
- **Uvicorn** — Servidor ASGI
- **Pydantic v2** — Validación de datos y modelos
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

El servidor arranca en `http://127.0.0.1:8000`.

## Documentación interactiva

| Herramienta | URL |
|-------------|-----|
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |

## Endpoints

| Método | Ruta | Descripción | Códigos de respuesta |
|--------|------|-------------|---------------------|
| `GET` | `/users` | Listar todos los usuarios (con paginación y filtros) | `200` |
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

## Ejemplos de peticiones y respuestas

### GET /users — Listar todos los usuarios

```bash
curl -s http://127.0.0.1:8000/users | python -m json.tool
```

Respuesta:
```json
{
    "message": "Users retrieved successfully",
    "data": [],
    "status_code": 200
}
```

### GET /users/{user_id} — Obtener usuario por ID

```bash
curl -s http://127.0.0.1:8000/users/1 | python -m json.tool
```

Respuesta:
```json
{
    "message": "User retrieved successfully",
    "data": {
        "id": 1,
        "name": "Juan Pérez",
        "email": "juan@example.com",
        "role": "user",
        "is_active": true,
        "created_at": "2026-06-03T12:00:00Z"
    },
    "status_code": 200
}
```

### POST /users — Crear un usuario

```bash
curl -s -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "password": "Pass1234",
    "role": "user"
}' | python -m json.tool
```

Respuesta:
```json
{
    "message": "User created successfully",
    "data": {
        "id": 1,
        "name": "Juan Pérez",
        "email": "juan@example.com",
        "role": "user",
        "is_active": true,
        "created_at": "2026-06-03T12:00:00Z"
    },
    "status_code": 201
}
```

### PUT /users/{user_id} — Actualizar usuario completamente

```bash
curl -s -X PUT http://127.0.0.1:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez Actualizado",
    "email": "juan.actualizado@example.com",
    "role": "admin",
    "is_active": true
}' | python -m json.tool
```

Respuesta:
```json
{
    "message": "User updated successfully",
    "data": {
        "id": 1,
        "name": "Juan Pérez Actualizado",
        "email": "juan.actualizado@example.com",
        "role": "admin",
        "is_active": true,
        "created_at": "2026-06-03T12:00:00Z"
    },
    "status_code": 200
}
```

### PATCH /users/{user_id} — Actualizar usuario parcialmente

```bash
curl -s -X PATCH http://127.0.0.1:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"role": "support"}' | python -m json.tool
```

Respuesta:
```json
{
    "message": "User updated partially",
    "data": {
        "id": 1,
        "name": "Juan Pérez Actualizado",
        "email": "juan.actualizado@example.com",
        "role": "support",
        "is_active": true,
        "created_at": "2026-06-03T12:00:00Z"
    },
    "status_code": 200
}
```

### DELETE /users/{user_id} — Eliminar un usuario

```bash
curl -s -o /dev/null -w "%{http_code}" -X DELETE http://127.0.0.1:8000/users/1
```

Respuesta: `204` (sin contenido)

### Escenarios de error

**Usuario no encontrado:**
```json
{
    "detail": "User with id 999 not found"
}
```

**Correo duplicado:**
```json
{
    "detail": "Email 'juan@example.com' already exists"
}
```

**Rol no permitido:**
```json
{
    "detail": "Role must be one of: admin, support, user"
}
```

**PATCH sin datos:**
```json
{
    "detail": "No fields provided for update"
}
```

**Datos inválidos (422):**
```json
{
    "detail": [
        {
            "type": "string_too_short",
            "loc": ["body", "name"],
            "msg": "String should have at least 3 characters",
            "input": "ab"
        }
    ]
}
```

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── __init__.py
│   ├── main.py                       # Punto de entrada, configuración y metadatos
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py            # Definición de endpoints CRUD
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py            # Modelos Pydantic (UserCreate, UserUpdate, UserUpdateFull, UserResponse)
│   │   └── response_schema.py        # Modelo de respuesta estandarizado
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py           # Lógica de negocio (CRUD)
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── user_dependencies.py      # Dependencias reutilizables con Depends()
│   └── data/
│       ├── __init__.py
│       └── users_db.py               # Simulación de base de datos en memoria
├── requirements.txt
└── README.md
```

## Dependency Injection con Depends()

Se aplicó **Dependency Injection** mediante el módulo `app/dependencies/user_dependencies.py`, creando funciones reutilizables que se inyectan en los endpoints usando `Depends()`.

### Dependencias implementadas

| Función | Descripción |
|---------|-------------|
| `get_user_or_404(user_id)` | Obtiene un usuario por ID o lanza `404 Not Found` |
| `validate_email_not_duplicate(email, exclude_user_id)` | Verifica que el email no esté registrado |
| `validate_role_allowed(role)` | Valida que el rol sea uno de los permitidos (`admin`, `support`, `user`) |
| `get_api_config()` | Retorna configuración general de la API |

### Ejemplo de uso en rutas

```python
@router.get("/{user_id}")
def get_user_route(
    user: dict = Depends(get_user_or_404),
):
    return {"data": user, "message": "User retrieved successfully", "status_code": 200}
```

La dependencia `get_user_or_404` recibe automáticamente el `user_id` del path parameter y retorna el usuario o lanza una excepción, eliminando lógica repetitiva en cada endpoint.

## Manejo de errores implementado

La API utiliza `HTTPException` de FastAPI para manejar errores de forma profesional:

- **Usuario no encontrado** — `HTTPException(404)` en `get_user_or_404`
- **Correo duplicado** — `HTTPException(400)` en `validate_email_not_duplicate`
- **Rol no permitido** — `HTTPException(400)` en `validate_role_allowed`
- **PATCH sin datos** — `HTTPException(400)` verificado directamente en la ruta
- **Datos inválidos** — Validación automática de Pydantic devuelve `422 Unprocessable Entity`

## Cabeceras HTTP personalizadas

Todas las respuestas incluyen:

- `X-App-Name: device_systems`
- `X-API-Version: 2.0`

## Capturas de Swagger UI

Para ver la documentación interactiva, ejecuta el servidor y abre en tu navegador:

```
http://127.0.0.1:8000/docs
```

Allí podrás:
- Explorar todos los endpoints disponibles con sus descripciones
- Probar cada operación directamente desde el navegador
- Ver los esquemas de datos (request/response)
- Observar los códigos de estado HTTP

## Capturas de ReDoc

```
http://127.0.0.1:8000/redoc
```

## Reflexión final

Esta evolución del proyecto **device_systems** transformó una API básica con operaciones GET y POST en una API REST profesional con:

1. **CRUD completo** — Implementación de PUT (actualización total) y PATCH (actualización parcial) correctamente diferenciados, más DELETE.
2. **Códigos HTTP apropiados** — Cada endpoint responde con el código correcto según la operación (201 para creación, 204 para eliminación, etc.).
3. **Manejo de errores** — Uso de `HTTPException` con mensajes claros y específicos para cada caso de error.
4. **Separación de responsabilidades** — Código organizado en `routes/`, `schemas/`, `services/`, `dependencies/` y `data/`.
5. **Dependency Injection** — Funciones reutilizables como `get_user_or_404()` inyectadas con `Depends()` que eliminan lógica repetitiva.
6. **Documentación automática** — Swagger UI y ReDoc configurados con metadatos completos, descripciones, summary y tags.
