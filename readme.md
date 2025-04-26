# Proyecto Django Sencillo: Conexión a Redis Cloud

Este proyecto es un ejemplo mínimo de una aplicación web Django que demuestra cómo conectar y interactuar con una base de datos Redis alojada en la nube utilizando la librería `django-redis` y gestionando la configuración sensible con `django-environ`.

El objetivo principal es mostrar la configuración básica y probar que se puede guardar y recuperar un valor en Redis desde una vista de Django.

## Prerrequisitos

Asegúrate de tener instalado:

* Python 3.x
* Git
* Una base de datos Redis en la nube (AWS ElastiCache, Redis Enterprise Cloud, etc.) con sus detalles de conexión (host, puerto, usuario, contraseña, número de base de datos).

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
    Con el entorno virtual activo y dentro del directorio `my_django_redis_app/`, instala las librerías necesarias usando el archivo `requirements.txt` que generaste:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración de la Conexión a Redis Cloud

1.  **Crea un archivo `.env`:**
    En el directorio **raíz del proyecto Django** (`my_django_redis_app/`, donde está `manage.py`), crea un nuevo archivo llamado `.env`.

2.  **Añade la URL de conexión a Redis:**
    Edita el archivo `.env` y añade la siguiente línea, **reemplazando los valores con los de tu base de datos Redis en la nube**:

    ```dotenv
    # .env - ¡No subas este archivo a Git si contiene credenciales reales!

    # URL de conexión a tu base de datos Redis en la nube
    # Formato: redis://[usuario:contraseña@]host:puerto[/numero_db]
    REDIS_URL=redis://tu_usuario:tu_contraseña@tu_host_redis.com:tu_puerto/0
    ```
    Asegúrate de que esta URL sea exactamente la que necesitas para conectar a tu instancia de Redis Cloud. Si no tienes usuario/contraseña, la URL podría ser `redis://tu_host_redis.com:tu_puerto/0`. Si la contraseña está vacía con un usuario, puede ser `redis://tu_usuario:@tu_host_redis.com:tu_puerto/0`.

3.  **(Recomendado) Añade `.env` a `.gitignore`:**
    Si usas Git, es una buena práctica añadir el archivo `.env` a tu `.gitignore` para evitar subir tus credenciales al repositorio. Si no tienes un archivo `.gitignore` en la raíz de tu repositorio (`django-redis/`), créalo y añade la línea `/my_django_redis_app/.env`.

## Ejecutar la Aplicación

1.  **Asegúrate de estar en el directorio del proyecto Django** (`my_django_redis_app/`) y con el entorno virtual activo.

2.  **Ejecuta las migraciones de la base de datos** (paso estándar de Django, aunque no se use para Redis):
    ```bash
    python manage.py migrate
    ```

3.  **Inicia el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
    El servidor se iniciará en `http://127.0.0.1:8000/`.

## Probar la Conexión a Redis

1.  Con el servidor de desarrollo corriendo, abre tu navegador web.
2.  Ve a la siguiente URL:
    ```
    [http://127.0.0.1:8000/redis/test/](http://127.0.0.1:8000/redis/test/)
    ```

3.  Deberías ver una página que muestra los resultados del intento de guardar y recuperar un valor en tu base de datos Redis en la nube. Si la configuración es correcta, verás mensajes de éxito indicando que el valor fue guardado y luego recuperado.

## Tecnologías Utilizadas

* Django
* Redis
* django-redis
* django-environ

Este proyecto es un punto de partida sencillo para entender la integración básica de Django con Redis.

---

Espero que este `README.md` sea útil para ti y para cualquier persona que quiera usar tu repositorio para aprender.
