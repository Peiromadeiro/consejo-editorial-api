from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from .utils import generar_consejo_editorial

app = FastAPI()

class Producto(BaseModel):
    titulo: str
    precio: str
    valoracion: float
    n_opiniones: int
    categoria: str
    bullets: List[str]
    descripcion: str

@app.post("/consejo-editorial")
def generar_consejo(producto: Producto):
    consejo = generar_consejo_editorial(producto.dict())
    return {"consejo": consejo}
