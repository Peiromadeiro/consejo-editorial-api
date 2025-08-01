from fastapi import FastAPI
from app.amazon_client import obtener_datos_producto
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "✅ API de Consejo Editorial activa"}

@app.get("/producto/{asin}")
def producto(asin: str):
    resultado = obtener_datos_producto(asin)
    if resultado:
        return resultado
    return {"error": "❌ No se pudo obtener el producto"}
