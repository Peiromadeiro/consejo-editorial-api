from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel
from .utils import generar_consejo_editorial
from .amazon_client import obtener_datos_producto

app = FastAPI()

class EntradaASIN(BaseModel):
    asin: str

@app.post("/consejo-editorial")
def generar_consejo_desde_asin(data: EntradaASIN):
    producto = obtener_datos_producto(data.asin)
    if not producto:
        return {"error": "No se pudo obtener el producto desde Amazon"}
    consejo = generar_consejo_editorial(producto)
    return {
        "asin": data.asin,
        "producto": producto,
        "consejo": consejo
    }
