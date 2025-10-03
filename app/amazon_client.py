import os
from amazon_paapi import AmazonApi
from app import config
import google.generativeai as genai

# Configura la API key de Gemini desde variable de entorno
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

amazon = AmazonApi(
    config.ACCESS_KEY,
    config.SECRET_KEY,
    config.ASSOCIATE_TAG,
    config.REGION
)

def safe_display_value(obj):
    """
    Función para obtener el atributo display_value de forma segura,
    manejando tipos variables y evitando fallos por atributos ausentes.
    """
    if not obj:
        return ""
    if hasattr(obj, "display_value"):
        val = getattr(obj, "display_value")
        if val is None:
            return ""
        return str(val)
    if isinstance(obj, (list, tuple)):
        valores = []
        for o in obj:
            if hasattr(o, "display_value"):
                val = getattr(o, "display_value")
                if val:
                    valores.append(str(val))
            else:
                valores.append(str(o))
        return valores
    return str(obj)

def generar_descripcion_periodistica_gemini(datos_producto):
    prompt = (
        f"Eres un periodista especializado en análisis de productos electrónicos para afiliación.\n"
        f"Genera:\n"
        f"1) Una descripción periodística, profesional y atractiva, de máximo 6 frases,\n"
        f"2) Una lista de puntos destacados sobre este producto de Amazon que resuman en bullets sus mejores características.\n\n"
        f"TÍTULO: {datos_producto.get('titulo', '')}\n"
        f"MARCA: {datos_producto.get('marca', '')}\n"
        f"CARACTERÍSTICAS PRINCIPALES: {', '.join(datos_producto.get('bullets', []))}\n"
        f"VALORACIÓN MEDIA: {datos_producto.get('valoracion', 'sin datos')}/5 basada en {datos_producto.get('n_opiniones', 'varias')} opiniones.\n"
        f"Devuélveme primero la descripción separada por una línea vacía, luego la lista de puntos destacados usando guiones (-) o viñetas.\n"
        f"El texto debe ser objetivo, claro y motivar a comprar a través del enlace afiliado."
    )
    model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")  # Cambia a otro modelo si quieres y tienes acceso
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Separar descripción y lista si el texto sigue formato esperado
    if "\n\n" in text:
        descripcion, bullets_text = text.split("\n\n", 1)
        # Extraer bullets (líneas que empiezan con -, • o similar)
        bullets_ia = [line.strip("-• ").strip() for line in bullets_text.splitlines() if line.strip()]
    else:
        descripcion = text
        bullets_ia = []

    return descripcion, bullets_ia

def obtener_datos_producto(asin: str):
    try:
        result = amazon.get_items(asin)
        item = result[0] if result else None
        if not item:
            print(f"[Amazon PAAPI] No se encontró el producto para el ASIN {asin}")
            return None

        item_info = item.item_info or {}
        product_info = getattr(item_info, "product_info", None) or {}
        offers = item.offers or {}
        offer_listing = offers.listings[0] if offers.listings else None
        customer_reviews = item.customer_reviews or {}
        browse_node_info = item.browse_node_info or {}
        browse_nodes = browse_node_info.browse_nodes or []

        datos = {
            "asin": asin,
            "titulo": safe_display_value(getattr(item_info, "title", None)) or "Sin título",
            "marca": safe_display_value(getattr(getattr(item_info, "by_line_info", None), "brand", None)),
            "fabricante": safe_display_value(getattr(getattr(item_info, "by_line_info", None), "manufacturer", None)),
            "precio": (f"{offer_listing.price.amount} {offer_listing.price.currency}"
                       if offer_listing and offer_listing.price else "Desconocido"),
            "imagen": (item.images.primary.large.url if item.images and item.images.primary and item.images.primary.large else ""),
            "url_producto": safe_display_value(getattr(item, "detail_page_url", None)),
            "valoracion": safe_display_value(getattr(customer_reviews, "star_rating", None)) or 0,
            "n_opiniones": safe_display_value(getattr(customer_reviews, "total_reviews", None)) or 0,
            "categoria": safe_display_value(browse_nodes[0]) if browse_nodes else "Sin categoría",
            "bullets": safe_display_value(getattr(item_info, "features", None)) or [],
            "descripcion": safe_display_value(getattr(product_info, "product_description", None)),
            "detalles_tecnicos": safe_display_value(getattr(item_info, "technical_info", None)) or [],
            "dimensiones": safe_display_value(getattr(product_info, "item_dimensions", None)),
            "peso": safe_display_value(getattr(product_info, "item_weight", None)),
            "fecha_lanzamiento": safe_display_value(getattr(product_info, "release_date", None)),
            "ean": safe_display_value(getattr(product_info, "ean", None)),
            "upc": safe_display_value(getattr(product_info, "upc", None)),
            "contras": [],  # Amazon no ofrece contras explícitos
        }

        # Generar descripción y bullets con Gemini
        descripcion_ia, bullets_ia = generar_descripcion_periodistica_gemini(datos)
        datos['descripcion_periodistica'] = descripcion_ia
        datos['bullets_ia'] = bullets_ia  # listado de puntos destacados IA

        return datos

    except Exception as e:
        print(f"[Amazon PAAPI ERROR] ASIN: {asin} - Excepción: {e}")
        return None
