# Proyecto Django: Notas con PostgreSQL y Redis

Este proyecto es un ejemplo de aplicación web Django que demuestra la integración y uso conjunto de:

* **PostgreSQL:** Como base de datos principal para almacenar datos persistentes (Notas).
* **Redis:** Para implementar una funcionalidad de "notas visitadas recientemente" (caché de acceso rápido).
* **django-redis:** Para usar Redis como backend de caché de Django.
* **django-environ:** Para gestionar la configuración sensible (URLs de bases de datos) mediante variables de entorno.

El proyecto incluye una aplicación de Notas simple con operaciones CRUD (Crear, Leer, Actualizar, Eliminar) y una funcionalidad que muestra las últimas notas visitadas utilizando Redis. También conserva una vista básica para probar la conexión directa a Redis configurada.

## Prerrequisitos

Asegúrate de tener instalado:

* Python 3.x
* Git
* Un servidor de base de datos PostgreSQL accesible (local o en la nube).
* Una base de datos Redis accesible (local o en la nube).

## Configuración del Entorno

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DE_TU_REPOSITORIO>
    cd <nombre_del_directorio_clonado> # Probablemente 'django-redis'
    ```

2.  **Crea un entorno virtual:**
    ```bash
    python -m venv env
    ```
    *(En algunos sistemas, podrías usar `python3 -m venv env`)*

3.  **Activa el entorno virtual:**
    * **En macOS/Linux:**
        ```bash
        source env/bin/activate
        ```
    * **En Windows:**
        ```bash
        env\Scripts\activate
        ```
    Verás `(env)` al inicio de tu línea de comandos.

4.  **Navega al directorio del proyecto Django:**
    ```bash
    cd my_django_redis_app
    ```
    Asegúrate de estar en el mismo directorio donde se encuentra el archivo `manage.py`.

5.  **Instala las dependencias:**
    Con el entorno virtual activo y dentro del directorio `my_django_redis_app/`, instala las librerías necesarias listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    Esto instalará Django, `django-redis`, `django-environ`, `psycopg2-binary` (para PostgreSQL) y `django-widget-tweaks`.

## Configuración de Bases de Datos (PostgreSQL y Redis)

El proyecto usa `django-environ` para cargar la configuración de tus bases de datos desde un archivo `.env`.

1.  **Crea un archivo `.env`:**
    En el directorio **raíz del proyecto Django** (`my_django_redis_app/`, donde está `manage.py`), crea un nuevo archivo llamado `.env`.

2.  **Añade las URLs de conexión:**
    Edita el archivo `.env` y añade las siguientes líneas, **reemplazando los valores con los detalles de tus bases de datos PostgreSQL y Redis**:

    ```dotenv
    # .env - ¡No subas este archivo a Git si contiene credenciales reales!

    # URL de conexión a tu base de datos PostgreSQL
    # Formato típico: postgres://usuario:contraseña@host:puerto/nombre_bd
    DATABASE_URL=postgres://tu_usuario_pg:tu_contraseña_pg@tu_host_pg.com:tu_puerto_pg/nombre_de_tu_bd

    # URL de conexión a tu base de datos Redis
    # Formato típico: redis://[usuario:contraseña@]host:puerto[/numero_db]
    REDIS_URL=redis://tu_usuario_redis:tu_contraseña_redis@tu_host_redis.com:tu_puerto_redis/0
    ```
    Asegúrate de que estas URLs sean exactamente las que necesitas para conectar a tus instancias de base de datos.

3.  **(Recomendado) Añade `.env` a `.gitignore`:**
    Si usas Git, es una buena práctica añadir el archivo `.env` a tu `.gitignore` para evitar subir tus credenciales al repositorio. Si no tienes un archivo `.gitignore` en la raíz de tu repositorio (`django-redis/`), créalo y añade la línea `/my_django_redis_app/.env`.

## Preparar la Base de Datos PostgreSQL

Antes de que Django pueda usar PostgreSQL, la base de datos en el servidor PostgreSQL debe ser creada.

1.  **Crea la base de datos vacía:**
    Conéctate a tu servidor PostgreSQL usando la terminal (`psql`) o una herramienta gráfica (`pgAdmin`) y crea una nueva base de datos con el mismo nombre que especificaste en tu `DATABASE_URL` en el archivo `.env`.
    Ejemplo usando `createdb` en la terminal (si tienes acceso):
    ```bash
    createdb <nombre_de_tu_bd> -U tu_usuario_pg -h tu_host_pg.com -p tu_puerto_pg
    ```
    *(Reemplaza los placeholders y opciones según tu configuración de PostgreSQL)*

2.  **Ejecuta las migraciones de Django:**
    Asegúrate de estar en el directorio del proyecto Django (`my_django_redis_app/`) y con el entorno virtual activo. Ejecuta las migraciones para crear las tablas (incluyendo la tabla de Notas) en tu base de datos PostgreSQL:
    ```bash
    python manage.py migrate
    ```

## Ejecutar la Aplicación

1.  Asegúrate de que tu entorno virtual esté activo, estés en el directorio `my_django_redis_app/` y que tus servicios de PostgreSQL y Redis estén corriendo y accesibles.
2.  Inicia el servidor de desarrollo de Django:
    ```bash
    python manage.py runserver
    ```
    El servidor se iniciará en `http://127.0.0.1:8000/`.

## Probar la Aplicación de Notas

1.  Con el servidor de desarrollo corriendo, abre tu navegador web.
2.  Ve a la siguiente URL para acceder a la aplicación de Notas:
    ```
    [http://127.0.0.1:8000/notes/](http://127.0.0.1:8000/notes/)
    ```
3.  **Crea notas:** Haz clic en "Crear Nueva Nota" para añadir algunas notas a la base de datos PostgreSQL.
4.  **Ver lista:** Verifica que las notas aparecen en la lista principal.
5.  **Ver detalle y funcionalidad "Recientes" con Redis:** Haz clic en los títulos de algunas notas para ver sus detalles. Vuelve a la lista (`/notes/`) y verifica que la sección "Notas Visitadas Recientemente" muestre las últimas notas que visitaste (esta lista se mantiene en Redis).
6.  **Editar y Eliminar:** Prueba las funcionalidades de edición y eliminación de notas. La eliminación también limpia la lista de Redis si la nota estaba en la lista reciente.
7.  **(Opcional) Prueba básica de conexión Redis:** La vista original en `http://127.0.0.1:8000/redis/` sigue activa para probar la conexión básica a Redis por separado.

## Ejecutar los Tests

El proyecto incluye tests para la aplicación de Notas que verifican las operaciones CRUD y la lógica de Redis.

1.  Asegúrate de que tus servicios de PostgreSQL y Redis estén corriendo y accesibles.
2.  Asegúrate de estar en el directorio del proyecto Django (`my_django_redis_app/`) y con el entorno virtual activo.
3.  Ejecuta los tests para la aplicación `notes`:
    ```bash
    python manage.py test notes
    ```
    Verifica que todos los tests pasen (`OK`).

## Tecnologías Utilizadas

* Django
* PostgreSQL
* Psycopg2-binary
* Redis
* django-redis
* django-environ
* django-widget-tweaks
* Tailwind CSS (vía CDN en base.html para estilos básicos)

Este proyecto sirve como un ejemplo práctico para entender la integración de estos componentes en un proyecto Django.

---
