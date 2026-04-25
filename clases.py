import os

def validar_entero(mensaje, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"Por favor, ingrese un número mayor o igual a {minimo}"); continue
            if maximo is not None and valor > maximo:
                print(f"Por favor, ingrese un número menor o igual a {maximo}"); continue
            return valor
        except ValueError: print("Entrada no válida. Por favor, ingrese un número entero.")
    
def validar_archivo(ruta, extensiones):
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    if os.path.splitext(ruta)[1].lower() not in extensiones:
        raise ValueError("Extension no valida")
    return True
