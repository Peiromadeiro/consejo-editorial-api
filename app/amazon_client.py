import os
from amazon_paapi import AmazonApi
from app import config
import google.generativeai as genai

# Obtienes la API key desde la variable de entorno y configuras Gemini
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

amazon = AmazonApi(
    config.ACCESS_KEY,
    config.SECRET_KEY,
    config.ASSOCIATE_TAG,
    config.REGION
)

def generar_descripcion_periodistica_gemini(datos_producto):
    prompt = (
        f"Eres un periodista especializado en análisis de productos electrónicos para afiliación.\n"
        f"Escribe una descripción periodística, profesional y atractiva, de máximo 6 frases, "
        f"sobre este producto de Amazon:\n\n"
        f"TÍTULO: {datos_producto.get('titulo', '')}\n"
        f"MARCA: {datos_producto.get('marca', '')}\n"
        f"CARACTERÍSTICAS PRINCIPALES: {', '.join(datos_producto.get('bullets', []))}\n"
        f"VALORACIÓN MEDIA: {datos_producto.get('valoracion', 'sin datos')}/5 basada en {datos_producto.get('n_opiniones', 'varias')} opiniones.\n"
        f"El texto debe ser objetivo, claro y motivar a comprar a través del enlace afiliado."
    )
    model = genai.GenerativeModel("gemini-1.5-flash")  # O "gemini-2.5-flash" si tienes acceso
    response = model.generate_content(prompt)
    return response.text.strip()

def obtener_datos_producto(asin: str):
    try:
        # Consulta PAAPI
        result = amazon.get_items(asin)
        item = result[0] if result else None
        if not item:
            print(f"[Amazon PAAPI] No se encontró el producto para el ASIN {asin}")
            return None
        
        # Protecciones para evitar errores de atributos faltantes
        item_info = item.item_info or {}
        product_info = getattr(item_info, "product_info", None) or {}
        offers = item.offers or {}
        offer_listing = offers.listings[0] if offers.listings else None
        customer_reviews = item.customer_reviews or {}
        browse_node_info = item.browse_node_info or {}
        browse_nodes = browse_node_info.browse_nodes or []

        # Construir datos base de Amazon
        datos = {
            "asin": asin,
            "titulo": item_info.title.display_value if hasattr(item_info, "title") and item_info.title else "Sin título",
            "marca": item_info.by_line_info.brand.display_value if hasattr(item_info, "by_line_info") and item_info.by_line_info and item_info.by_line_info.brand else "",
            "fabricante": item_info.by_line_info.manufacturer.display_value if hasattr(item_info, "by_line_info") and item_info.by_line_info and item_info.by_line_info.manufacturer else "",
            "precio": f"{offer_listing.price.amount} {offer_listing.price.currency}" if offer_listing and offer_listing.price else "Desconocido",
            "imagen": item.images.primary.large.url if item.images and item.images.primary and item.images.primary.large else "",
            "url_producto": item.detail_page_url if hasattr(item, "detail_page_url") else "",
            "valoracion": customer_reviews.star_rating.display_value if hasattr(customer_reviews, "star_rating") and customer_reviews.star_rating else 0,
            "n_opiniones": customer_reviews.total_reviews.display_value if hasattr(customer_reviews, "total_reviews") and customer_reviews.total_reviews else 0,
            "categoria": browse_nodes[0].display_name if browse_nodes else "Sin categoría",
            "bullets": item_info.features.display_values if hasattr(item_info, "features") and item_info.features else [],
            "descripcion": product_info.product_description.display_value if hasattr(product_info, "product_description") and product_info.product_description else "",
            "detalles_tecnicos": item_info.technical_info.display_values if hasattr(item_info, "technical_info") and item_info.technical_info else [],
            "dimensiones": product_info.item_dimensions.display_value if hasattr(product_info, "item_dimensions") and product_info.item_dimensions else "",
            "peso": product_info.item_weight.display_value if hasattr(product_info, "item_weight") and product_info.item_weight else "",
            "fecha_lanzamiento": product_info.release_date.display_value if hasattr(product_info, "release_date") and product_info.release_date else "",
            "ean": product_info.ean.display_value if hasattr(product_info, "ean") and product_info.ean else "",
            "upc": product_info.upc.display_value if hasattr(product_info, "upc") and product_info.upc else "",
            "contras": [],  # Amazon no ofrece contras explícitos
        }

        # Generar la descripción periodística mediante Gemini
        descripcion_ia = generar_descripcion_periodistica_gemini(datos)
        datos['descripcion_periodistica'] = descripcion_ia

        return datos

    except Exception as e:
        print(f"[Amazon PAAPI ERROR] ASIN: {asin} - Excepción: {e}")
        return None

