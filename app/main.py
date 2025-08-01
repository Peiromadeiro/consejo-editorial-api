from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from app.amazon_client import obtener_datos_producto

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    """
    Ruta que sirve la página principal con el formulario de búsqueda
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/producto/{asin}")
async def api_producto(asin: str):
    """
    Endpoint API que recibe un ASIN, llama a la función que consulta Amazon PAAPI + Gemini, y devuelve JSON con datos
    """
    datos = obtener_datos_producto(asin)
    if not datos:
        # Si no se encontró el producto o hubo error, devolvemos HTTP 404 con detalle
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return JSONResponse(content=datos)
