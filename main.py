import os
from clases import (
    ArchivoSIATA, ArchivoEEG, AlmacenObjetos, validar_entero
)
CARPETA_CONTROL = "control"
CARPETA_PARKINSON = "parkinson"
CARPETA_CVS = "csv"

almacen = AlmacenObjetos()

def separador(titulo=""):
    ancho = 50
    print("\n"+"-" * ancho)
    if titulo:
        print(f" {titulo}")
        print("-" * ancho)

def preguntar_guardar():
        resp= input("¿Desea guardar los objetos en archivos CSV? (s/n): ").strip().lower()
        return resp == 's'

def listar_archivos(carpeta,extension):
    if not os.path.exists(carpeta):
        print(f"No se encontró la carpeta '{carpeta}'.")
        return []
    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(extension)]
    archivos.sort()

    if not archivos:
        print(f"No se encontraron archivos con extensión '{extension}' en la carpeta '{carpeta}'.")
        return []
    print(f"Archivos encontrados en '{carpeta}':")
    for i, nombre in enumerate(archivos):
        print(f"{i}. {nombre}")
    return[os.path.join(carpeta, f) for f in archivos]

def seleccionar_archivo_cvs():
    separador("Seleccionar archivo SIATA")
    rutas = listar_archivos(CARPETA_CVS,".csv")
    if not rutas:
         return None
    idx = validar_entero("\n Ingrese el número del archivo SIATA a cargar: ", 0, len(rutas)-1)
    return rutas[idx]

def seleccionar_archivo_mat():
     separador("Seleccionar archivo mat (EEG)")
     print(" ")
