def generar_consejo_editorial(producto):
    titulo = producto.get("titulo", "Producto sin título")
    categoria = producto.get("categoria", "Sin categoría")
    precio = producto.get("precio", "Precio desconocido")
    valoracion = producto.get("valoracion", 0)
    n_opiniones = producto.get("n_opiniones", 0)
    bullets = producto.get("bullets", [])[:3]

    enfoque = f"Incluye este producto en una guía de \"Los mejores productos de {categoria.lower()} por menos de {precio}\"."
    titular = f"Este {titulo.lower()} sorprende por su utilidad y buenas valoraciones"
    visuales = "Usa imágenes que lo muestren en su contexto real de uso, con fondo limpio o en manos de personas."
    seo = f"Frases como “{titulo.lower()} opiniones”, “¿merece la pena comprar {titulo.lower()}?” o “mejor {categoria.lower()} relación calidad-precio”."

    return f"""📰 Consejo editorial para El Comprador:

🎯 Enfoque recomendado:
{enfoque}

📝 Titular sugerido:
{titular}

📌 Ángulos de contenido a destacar:
- {bullets[0] if len(bullets) > 0 else "Información no disponible"}
- {bullets[1] if len(bullets) > 1 else "Información no disponible"}
- {bullets[2] if len(bullets) > 2 else "Información no disponible"}

🖼️ Recomendaciones visuales:
{visuales}

🔍 Extra para SEO y Discover:
{seo}
"""
