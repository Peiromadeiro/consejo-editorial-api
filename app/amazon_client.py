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
        result = amazon.get_items(asin)
        item = result[0] if result else None
        if not item:
            return None

        return {
            "titulo": item.item_info.title.display_value if item.item_info and item.item_info.title else "Sin título",
            "precio": (
                f"{item.offers.listings[0].price.amount} {item.offers.listings[0].price.currency}"
                if item.offers and item.offers.listings else "Desconocido"
            ),
            "valoracion": item.customer_reviews.star_rating.display_value
            if item.customer_reviews and item.customer_reviews.star_rating else 0,
            "n_opiniones": item.customer_reviews.total_reviews.display_value
            if item.customer_reviews and item.customer_reviews.total_reviews else 0,
            "categoria": item.browse_node_info.browse_nodes[0].display_name
            if item.browse_node_info and item.browse_node_info.browse_nodes else "Sin categoría",
            "bullets": item.item_info.features.display_values
            if item.item_info and item.item_info.features else [],
            "descripcion": (
                item.item_info.product_info.product_description.display_value
                if item.item_info
                and hasattr(item.item_info, "product_info")
                and hasattr(item.item_info.product_info, "product_description")
                else ""
),
        }

    except Exception as e:
        print(f"Error general: {e}")
        return None

