device_systems
API REST con FastAPI para gestionar usuarios, dispositivos tecnologicos y prestamos.

Como ejecutar el proyecto
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
Abrir http://127.0.0.1:8000/docs
Endpoints de la API
/users GET /users/ - lista todos los usuarios, se puede filtrar por rol o estado GET /users/{id} - obtiene un usuario por ID POST /users/ - crea un usuario nuevo PUT /users/{id} - actualiza un usuario completo PATCH /users/{id} - actualiza solo algunos campos DELETE /users/{id} - elimina un usuario GET /users/{id}/loans - prestamos de un usuario

/devices GET /devices/ - lista dispositivos, filtros por tipo, marca, disponible o busqueda GET /devices/{id} - obtiene un dispositivo por ID POST /devices/ - crea un dispositivo PUT /devices/{id} - actualiza un dispositivo completo PATCH /devices/{id} - actualiza solo algunos campos DELETE /devices/{id} - elimina un dispositivo GET /devices/{id}/loans - historial de prestamos de un dispositivo

/loans GET /loans/ - lista prestamos, filtros por estado, email de usuario o tipo de dispositivo GET /loans/details - lista prestamos con informacion del usuario y dispositivo GET /loans/{id} - obtiene un prestamo por ID POST /loans/ - crea un prestamo, valida que el dispositivo este disponible PATCH /loans/{id}/return - devuelve un dispositivo

Migraciones con Alembic
Para crear las tablas users, devices y loans se uso Alembic.

Pasos: alembic init alembic alembic revision --autogenerate -m "crear tablas" alembic upgrade head

Para ver el historial de migraciones: alembic history

Tecnologias usadas
Python, FastAPI, SQLAlchemy, Alembic, Pydantic, SQLite, Uvicorn.

Estructura del proyecto
app/main.py - inicio de la API app/database/connection.py - conexion a SQLite app/models/ - modelos User, Device y Loan app/schemas/ - validacion de datos con Pydantic app/services/ - logica de negocio app/routes/ - rutas de la API alembic/ - migraciones de base de datos requirements.txt - dependencias del proyecto

Codigos de estado HTTP
200 - consulta exitosa 201 - registro creado 204 - eliminacion exitosa 400 - dato duplicado o filtro invalido 404 - recurso no encontrado 409 - regla de negocio incumplida (dispositivo no disponible, prestamo ya devuelto) 422 - error de validacion

Notas
Los nombres de las tablas estan en ingles porque SQLAlchemy funciona asi pero las descripciones y mensajes de la API estan en español. La base de datos es SQLite y se guarda en el archivo device_systems.db.
