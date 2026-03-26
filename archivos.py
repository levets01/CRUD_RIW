"""
Funciones para guardar y cargar el inventario en archivos CSV.
"""

import csv
import os


def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.

    Formato:
        nombre,precio,cantidad

    Parámetros:
        inventario (list): Lista de productos.
        ruta (str): Ruta del archivo CSV.
        incluir_header (bool): Si se escribe encabezado.

    Retorna:
        bool: True si se guardó correctamente, False si ocurrió error.
    """
    if not inventario:
        print("No se puede guardar: el inventario está vacío.")
        return False

    try:
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)

            if incluir_header:
                writer.writerow(["nombre", "precio", "cantidad"])

            for producto in inventario:
                writer.writerow([
                    producto["nombre"],
                    producto["precio"],
                    producto["cantidad"]
                ])

        print(f"Inventario guardado en: {ruta}")
        return True

    except PermissionError:
        print("Error: no tienes permisos para escribir en esa ruta.")
    except OSError as e:
        print(f"Error del sistema al guardar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado al guardar: {e}")

    return False


def cargar_csv(ruta):
    """
    Carga un inventario desde un archivo CSV.

    Reglas:
        - Debe tener encabezado válido: nombre,precio,cantidad
        - Cada fila debe tener exactamente 3 columnas
        - precio -> float no negativo
        - cantidad -> int no negativo

    Parámetros:
        ruta (str): Ruta del archivo CSV.

    Retorna:
        tuple: (productos_cargados, filas_invalidas)
            productos_cargados (list)
            filas_invalidas (int)
    """
    productos = []
    filas_invalidas = 0

    try:
        with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
            reader = csv.reader(archivo)

            encabezado = next(reader, None)

            if encabezado != ["nombre", "precio", "cantidad"]:
                print("Error: encabezado inválido. Debe ser: nombre,precio,cantidad")
                return [], 0

            for fila in reader:
                try:
                    if len(fila) != 3:
                        filas_invalidas += 1
                        continue

                    nombre, precio, cantidad = fila

                    precio = float(precio)
                    cantidad = int(cantidad)

                    if precio < 0 or cantidad < 0:
                        filas_invalidas += 1
                        continue

                    productos.append({
                        "nombre": nombre.strip(),
                        "precio": precio,
                        "cantidad": cantidad
                    })

                except ValueError:
                    filas_invalidas += 1

        return productos, filas_invalidas

    except FileNotFoundError:
        print("Error: archivo no encontrado.")
    except UnicodeDecodeError:
        print("Error: el archivo no tiene una codificación válida (UTF-8).")
    except Exception as e:
        print(f"Error inesperado al cargar el archivo: {e}")

    return [], 0
