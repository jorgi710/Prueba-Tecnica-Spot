# Aplicación de Mensajes con Imágenes

Esta es una aplicación que permite recibir mensajes con imágenes, guardar las imágenes en Azure Blob Storage y almacenar los detalles en una base de datos SQLite.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalado lo siguiente:

- Python 3.7 o superior
- Todas las dependencias especificadas en el archivo `requirements.txt`

## Configuración

Antes de ejecutar la aplicación, debes realizar algunas configuraciones:

1. Configura las credenciales de Azure Blob Storage:
   - Abre el archivo `main.py` y busca las variables `account_name`, `account_key` y `container_name`.
   - Reemplaza los valores por tus propias credenciales de Azure Blob Storage.

2. Base de datos SQLite:
   - No se requiere ninguna configuración adicional para la base de datos SQLite. El archivo `database.db` se creará automáticamente al ejecutar la aplicación.

## Instalación

1. Crea un entorno virtual (opcional, pero se recomienda):
   ```shell
   python -m venv myenv
   source myenv/bin/activate  # Linux/Mac
   myenv\Scripts\activate  # Windows

2. Instala las dependencias:
    ```shell
    pip install -r requirements.txt
## Ejecución

1. Asegúrate de haber activado el entorno virtual (si lo creaste en el paso anterior).

2. Ejecuta la aplicación:
   ```shell
    python main.py
3. La aplicación se ejecutará en http://localhost:8000.

## Uso

Puedes interactuar con la API utilizando herramientas como cURL, Postman, Thunder Client o cualquier otro cliente HTTP.

Endpoint /messages/
- Método: POST
- URL: http://localhost:8000/messages/
Envía una solicitud POST a esta URL para enviar mensajes con imágenes. El cuerpo de la solicitud debe tener el siguiente formato: 
    ```json
    [
        {
            "date": "2023-05-23T12:00:00",
            "image": {
            "image_base64": "base64_encoded_image_data"
            },
            "camera_id": 1
        },
        {
            "date": "2023-05-23T12:00:00",
            "image": {
            "image_base64": "base64_encoded_image_data"
            },
            "camera_id": 2
        }
    ]

- Asegúrate de reemplazar "base64_encoded_image_data" con la representación en base64 de la imagen que deseas enviar.

## JSON de Prueba

Se adjunta un archivo JSON de prueba (`sample_payload.json`) que puedes utilizar para probar la API. Este archivo contiene un ejemplo de solicitud válida para el endpoint `/messages/`. Puedes utilizar este JSON como referencia para crear tus propias solicitudes y probar la funcionalidad del sistema.

**Nota:** Asegúrate de ajustar los valores dentro del JSON según sea necesario para que se ajusten a tus necesidades y configuración.

### Uso del JSON de Prueba

Puedes utilizar el JSON de prueba en combinación con herramientas como cURL, Postman o cualquier cliente HTTP para realizar solicitudes a la API. Asegúrate de establecer los encabezados adecuados y enviar la solicitud POST al endpoint `/messages/` con el contenido del JSON como cuerpo de la solicitud.

Ejemplo de solicitud cURL:

```bash
curl -X POST -H "Content-Type: application/json" -d @sample_payload.json http://localhost:8000/messages/
