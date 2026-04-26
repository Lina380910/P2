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
    print(" ¿Desea cargar un archivo de control o de parkinson?")
    print(" 1. Control")
    print(" 2. Parkinson")
    opcion = validar_entero("Ingrese el número de la opción deseada: ", 1, 2)
    carpeta = CARPETA_CONTROL if opcion == 1 else CARPETA_PARKINSON
    rutas = listar_archivos(carpeta, ".mat")
    if not rutas:
        return None
    idx = validar_entero("\n Ingrese el número del archivo EEG a cargar: ", 0, len(rutas)-1)
    return rutas[idx]

def menu_siata(siata: ArchivoSIATA):
    while True:
        separador(f"SUBMENU SIATA - {siata.nombre}")
        print("1. Mostrar información basica (info/ describe)")
        print("2. Mostrar columna (plot, boxplotx, histograma)")
        print("3. Operaciones (apply, map, suma/resta)")
        print("4. Remuestreo y gráfico (diario,mensual,trimestral")
        op = validar_entero("Ingrese el número de la opción deseada: ", 1, 3)
        if op == 1:
            siata.mostrar_info()
        elif op == 2:
            col = siata.elegir_columna()
            guardar = preguntar_guardar()
            siata.graficar_columna(nombre_col= col, guardar= guardar )
        elif op == 3:
            siata.operaciones()
        elif op == 4:
            col= siata.elegir_columna()
            guardar = preguntar_guardar()
            siata.graficar_remuestreo(nombre_col= col, guardar= guardar )
        elif op == 0:
                break
