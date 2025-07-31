from app.amazon_client import obtener_datos_producto

asin = "B09P8GPDHP"
producto = obtener_datos_producto(asin)

if producto:
    print("✅ Producto obtenido correctamente:")
    for clave, valor in producto.items():
        print(f"{clave}: {valor}")
else:
    print("❌ No se pudo obtener el producto desde Amazon.")
