from fastapi import FastAPI
from pydantic import BaseModel, validator
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
import base64
import uvicorn
from typing import List
from database import crear_tabla, agregar_mensaje

import asyncio

app = FastAPI()

# Configuración de Azure Blob Storage
account_name = "stdevtestaccount"
account_key = "M7G3GR77/JsCrWZJq6p5Nku0YiiS5o9WiwMTSjchDhfz9u2+mHS+rv51gdhVHHMDzx3kWlHQjNAB+AStpT49LQ=="
container_name = "test-container"

class Image(BaseModel):
    image_base64: str

class Message(BaseModel):
    date: datetime
    image: Image
    camera_id: int

    @validator('date')
    def validate_date(cls, value):
        # Verificar si la fecha está en el pasado
        if value < datetime.now():
            raise ValueError("La fecha no puede ser anterior a la fecha actual")
        return value

    @validator('camera_id')
    def validate_camera_id(cls, value):
        # Verificar si el ID de la cámara es un entero positivo
        if value <= 0:
            raise ValueError("El ID de la cámara debe ser un entero positivo")
        return value

def guardar_imagen_en_azure(image_base64: str, camera_id: int):
    # Decodificar la imagen base64
    image_data = base64.b64decode(image_base64)

    # Crear una instancia de BlobServiceClient
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

    # Obtener una referencia al contenedor en Azure Blob Storage
    container_client = blob_service_client.get_container_client(container_name)

    # Generar un nombre de archivo único para la imagen (puedes usar el ID de la cámara y la fecha actual, por ejemplo)
    file_name = f"image_{camera_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

    # Subir la imagen al contenedor en Azure Blob Storage
    blob_client = container_client.upload_blob(name=file_name, data=image_data)
    print(f"Imagen guardada en Azure Blob Storage: {blob_client.url}")

    # Subir a la base de datos
    agregar_mensaje(str(datetime.now(timezone.utc)), camera_id, blob_client.url)

async def guardar_imagen_en_azure_async(image_base64: str, camera_id: int):
    guardar_imagen_en_azure(image_base64, camera_id)

@app.post("/messages/")
async def create_message(messages: List[Message]):
    try:
        print("Nuevos mensajes recibidos:")
        for message in messages:
            print(f"Fecha: {message.date}")
            print(f"ID de la cámara: {message.camera_id}")

        tasks = []
        for message in messages:
            tasks.append(guardar_imagen_en_azure_async(message.image.image_base64, message.camera_id))

        await asyncio.gather(*tasks)

        return {"message": "Mensajes recibidos correctamente"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "Ocurrió un error durante el procesamiento de la solicitud"}

if __name__ == "__main__":
    crear_tabla()
    uvicorn.run(app, host="localhost", port=8000)
