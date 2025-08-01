from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from app.amazon_client import obtener_datos_producto

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/producto/{asin}")
async def api_producto_json(asin: str):
    # Esta ruta sigue devolviendo JSON para uso API o fetch
    datos = obtener_datos_producto(asin)
    if not datos:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return JSONResponse(content=datos)

@app.get("/producto/{asin}")
async def pagina_producto(asin: str, request: Request):
    # Nueva ruta que renderiza la ficha producto en HTML
    datos = obtener_datos_producto(asin)
    if not datos:
        # Aquí puedes devolver un 404 bonito o redirigir a /
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return templates.TemplateResponse("producto.html", {"request": request, "producto": datos})
