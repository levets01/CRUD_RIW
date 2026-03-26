"""
servicios.py
Funciones de negocio para gestionar un inventario en memoria.
El inventario se representa como una lista de diccionarios:
{"nombre": str, "precio": float, "cantidad": int}
"""


def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un producto al inventario si no existe.
    Si ya existe, suma la cantidad y actualiza el precio.

    Parámetros:
        inventario (list): Lista de productos.
        nombre (str): Nombre del producto.
        precio (float): Precio del producto.
        cantidad (int): Cantidad del producto.

    Retorna:
        str: Mensaje de resultado.
    """
    producto = buscar_producto(inventario, nombre)

    if producto:
        producto["cantidad"] += cantidad
        producto["precio"] = precio
        return f"Producto existente actualizado: {nombre}"
    else:
        inventario.append({
            "nombre": nombre.strip(),
            "precio": float(precio),
            "cantidad": int(cantidad)
        })
        return f"Producto agregado correctamente: {nombre}"


def mostrar_inventario(inventario):
    """
    Genera un texto con el contenido del inventario.

    Parámetros:
        inventario (list): Lista de productos.

    Retorna:
        str: Representación legible del inventario.
    """
    if not inventario:
        return "El inventario está vacío."

    salida = "\n===== INVENTARIO =====\n"
    for i, producto in enumerate(inventario, start=1):
        subtotal = producto["precio"] * producto["cantidad"]
        salida += (
            f"{i}. Nombre: {producto['nombre']}\n"
            f"   Precio: ${producto['precio']:.2f}\n"
            f"   Cantidad: {producto['cantidad']}\n"
            f"   Subtotal: ${subtotal:.2f}\n\n"
        )
    return salida


def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre (sin importar mayúsculas/minúsculas).

    Parámetros:
        inventario (list): Lista de productos.
        nombre (str): Nombre a buscar.

    Retorna:
        dict | None: Producto encontrado o None.
    """
    nombre = nombre.strip().lower()

    for producto in inventario:
        if producto["nombre"].strip().lower() == nombre:
            return producto

    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio y/o la cantidad de un producto existente.

    Parámetros:
        inventario (list): Lista de productos.
        nombre (str): Nombre del producto.
        nuevo_precio (float | None): Nuevo precio.
        nueva_cantidad (int | None): Nueva cantidad.

    Retorna:
        bool: True si se actualizó, False si no se encontró.
    """
    producto = buscar_producto(inventario, nombre)

    if not producto:
        return False

    if nuevo_precio is not None:
        producto["precio"] = float(nuevo_precio)

    if nueva_cantidad is not None:
        producto["cantidad"] = int(nueva_cantidad)

    return True


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.

    Parámetros:
        inventario (list): Lista de productos.
        nombre (str): Nombre del producto.

    Retorna:
        bool: True si se eliminó, False si no se encontró.
    """
    producto = buscar_producto(inventario, nombre)

    if producto:
        inventario.remove(producto)
        return True

    return False


def calcular_estadisticas(inventario):
    """
    Calcula estadísticas generales del inventario.

    Métricas:
        - unidades_totales
        - valor_total
        - producto_mas_caro (nombre, precio)
        - producto_mayor_stock (nombre, cantidad)

    Parámetros:
        inventario (list): Lista de productos.

    Retorna:
        dict: Diccionario con estadísticas.
    """
    if not inventario:
        return {
            "unidades_totales": 0,
            "valor_total": 0.0,
            "producto_mas_caro": None,
            "producto_mayor_stock": None
        }

    subtotal = lambda p: p["precio"] * p["cantidad"]

    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)

    producto_mas_caro = max(inventario, key=lambda p: p["precio"])
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": (producto_mas_caro["nombre"], producto_mas_caro["precio"]),
        "producto_mayor_stock": (producto_mayor_stock["nombre"], producto_mayor_stock["cantidad"])
    }
