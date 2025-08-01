from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from app.amazon_client import obtener_datos_producto
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/producto/{asin}")
async def api_producto(asin: str):
    producto = obtener_datos_producto(asin)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto
