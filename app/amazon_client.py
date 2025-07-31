from amazon_paapi import AmazonApi
from app import config

amazon = AmazonApi(
    config.ACCESS_KEY,
    config.SECRET_KEY,
    config.ASSOCIATE_TAG,
    config.REGION
)

def obtener_datos_producto(asin: str):
    try:
        item = amazon.get_items(asin)[0]

        return {
            "titulo": item.title,
            "precio": f"{item.prices.amount} {item.prices.currency}" if item.prices else "Desconocido",
            "valoracion": item.reviews.rating if item.reviews else 0,
            "n_opiniones": item.reviews.count if item.reviews else 0,
            "categoria": " > ".join(item.browse_node) if item.browse_node else "Sin categoría",
            "bullets": item.features if item.features else [],
            "descripcion": item.editorial_reviews[0].content if item.editorial_reviews else "",
        }
    except Exception as e:
        print(f"Error al obtener el producto: {e}")
        return None
