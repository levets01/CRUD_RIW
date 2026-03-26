
from servicios import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    calcular_estadisticas
)

from archivos import guardar_csv, cargar_csv


def pausar():
    input("\nPresione ENTER para continuar...")


def limpiar_pantalla():
    import os
    os.system("cls" if os.name == "nt" else "clear")


def pedir_float(mensaje):
  
    # Aca se debe Solicita un número float no negativo al usuario.
   
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Debe ingresar un número.")


def pedir_int(mensaje):
    """
    Solicita un número entero no negativo al usuario.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Debe ingresar un número entero.")


def fusionar_inventarios(inventario_actual, inventario_nuevo):
    """
    Fusiona dos inventarios por nombre.

    Política:
        - Si el producto existe: suma cantidad y actualiza precio al nuevo.
        - Si no existe: lo agrega.

    Parámetros:
        inventario_actual (list): Inventario en memoria.
        inventario_nuevo (list): Inventario cargado desde CSV.

    Retorna:
        None
    """
    for nuevo in inventario_nuevo:
        existente = buscar_producto(inventario_actual, nuevo["nombre"])

        if existente:
            existente["cantidad"] += nuevo["cantidad"]
            existente["precio"] = nuevo["precio"]
        else:
            inventario_actual.append(nuevo)


def mostrar_menu():
    """
    Muestra el menú principal.
    """
    print("\n===== INVENTARIO AVANZADO =====")
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Ver estadísticas")
    print("7. Guardar CSV")
    print("8. Cargar CSV")
    print("9. Salir")


def main():
    inventario = []

    while True:
        try:
            limpiar_pantalla()
            mostrar_menu()
            opcion = input("Seleccione una opción (1-9): ").strip()

            if opcion == "1":
                print("\n--- Agregar producto ---")
                nombre = input("Nombre del producto: ").strip()
                precio = pedir_float("Precio: ")
                cantidad = pedir_int("Cantidad: ")

                mensaje = agregar_producto(inventario, nombre, precio, cantidad)
                print(mensaje)
                pausar()

            elif opcion == "2":
                print("\n--- Inventario ---")
                print(mostrar_inventario(inventario))
                pausar()

            elif opcion == "3":
                print("\n--- Buscar producto ---")
                nombre = input("Nombre del producto a buscar: ").strip()
                producto = buscar_producto(inventario, nombre)

                if producto:
                    print("\nProducto encontrado:")
                    print(producto)
                else:
                    print("Producto no encontrado.")

                pausar()

            elif opcion == "4":
                print("\n--- Actualizar producto ---")
                nombre = input("Nombre del producto a actualizar: ").strip()

                producto = buscar_producto(inventario, nombre)
                if not producto:
                    print("Producto no encontrado.")
                    pausar()
                    continue

                print("Deje vacío si no desea cambiar ese valor.")

                entrada_precio = input("Nuevo precio: ").strip()
                entrada_cantidad = input("Nueva cantidad: ").strip()

                nuevo_precio = None
                nueva_cantidad = None

                if entrada_precio != "":
                    try:
                        nuevo_precio = float(entrada_precio)
                        if nuevo_precio < 0:
                            print("El precio no puede ser negativo.")
                            pausar()
                            continue
                    except ValueError:
                        print("Precio inválido.")
                        pausar()
                        continue

                if entrada_cantidad != "":
                    try:
                        nueva_cantidad = int(entrada_cantidad)
                        if nueva_cantidad < 0:
                            print("La cantidad no puede ser negativa.")
                            pausar()
                            continue
                    except ValueError:
                        print("Cantidad inválida.")
                        pausar()
                        continue

                actualizado = actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)

                if actualizado:
                    print("Producto actualizado correctamente.")
                else:
                    print("No se pudo actualizar el producto.")

                pausar()

            elif opcion == "5":
                print("\n--- Eliminar producto ---")
                nombre = input("Nombre del producto a eliminar: ").strip()

                eliminado = eliminar_producto(inventario, nombre)

                if eliminado:
                    print("Producto eliminado correctamente.")
                else:
                    print("Producto no encontrado.")

                pausar()

            elif opcion == "6":
                print("\n--- Estadísticas del inventario ---")
                estadisticas = calcular_estadisticas(inventario)

                print(f"Unidades totales: {estadisticas['unidades_totales']}")
                print(f"Valor total del inventario: ${estadisticas['valor_total']:.2f}")

                if estadisticas["producto_mas_caro"]:
                    nombre_caro, precio_caro = estadisticas["producto_mas_caro"]
                    print(f"Producto más caro: {nombre_caro} (${precio_caro:.2f})")

                if estadisticas["producto_mayor_stock"]:
                    nombre_stock, cantidad_stock = estadisticas["producto_mayor_stock"]
                    print(f"Producto con mayor stock: {nombre_stock} ({cantidad_stock} unidades)")

                pausar()

            elif opcion == "7":
                print("\n--- Guardar inventario en CSV ---")
                ruta = input("Ingrese la ruta o nombre del archivo (ej: inventario.csv): ").strip()
                guardar_csv(inventario, ruta)
                pausar()

            elif opcion == "8":
                print("\n--- Cargar inventario desde CSV ---")
                ruta = input("Ingrese la ruta o nombre del archivo CSV: ").strip()

                productos_cargados, filas_invalidas = cargar_csv(ruta)

                if productos_cargados:
                    decision = input("¿Sobrescribir inventario actual? (S/N): ").strip().upper()

                    if decision == "S":
                        inventario = productos_cargados
                        accion = "reemplazo"
                    else:
                        fusionar_inventarios(inventario, productos_cargados)
                        accion = "fusión"

                    print("\nCarga completada.")
                    print(f"Productos cargados: {len(productos_cargados)}")
                    print(f"Filas inválidas omitidas: {filas_invalidas}")
                    print(f"Acción realizada: {accion}")
                else:
                    print("No se cargaron productos válidos.")

                pausar()

            elif opcion == "9":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción inválida. Debe ser un número entre 1 y 9.")
                pausar()

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            pausar()


if __name__ == "__main__":
    main()
