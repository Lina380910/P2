import os
from clases import (
    ArchivoSIATA, ArchivoEEG, AlmacenObjetos, validar_entero
)
CARPETA_CONTROL = "control"
CARPETA_PARKINSON = "parkinson"
CARPETA_CSV = "csv"

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

def seleccionar_archivo_csv():
    separador("Seleccionar archivo SIATA")
    rutas = listar_archivos(CARPETA_CSV,".csv")
    if not rutas:
         return None
    idx = validar_entero("\n Ingrese el número del archivo SIATA a cargar: ", 0, len(rutas)-1)
    return rutas[idx]

def seleccionar_archivo_mat():
     separador("Seleccionar archivo mat (EEG)")
     print(" ")

def menu_siata(siata:ArchivoSIATA):
    while True:
        print("\n Opciones de análisis SIATA:")
        print("1. Mostrar información del archivo")
        print("2. Mostrar datos estadísticos")
        print("3. Graficar serie de tiempo")
        print("0. Volver al menú principal")

        op = validar_entero("\n Opcion:", 0, 3)
        if op == 1:
            siata.mostrar_info()
        elif op == 2:
            siata.mostrar_estadisticas()
        elif op == 3:
            guardar=preguntar_guardar()
            siata.graficar_serie(guardar=guardar)
        elif op == 0:
            print("Saliendo del programa.")
            break

def menu_eeg(eeg:ArchivoEEG):
    eeg.mostrar_llaves()
    print("\n Seleccione la variable principal a trabajar:")
    eeg.seleccionar_llave()

    while True:
        print("\n Opciones de análisis:")
        print("1. Mostrar llaves del archivo")
        print("2. Suma de tres canales y gráfico")
        print("3. Promedio y desviación estándar 3D con stem")
        print("0. Volver al menú principal")

        op = validar_entero ("\n Opcion:", 0, 3)
        if op == 1:
            eeg.mostrar_llaves()
        elif op == 2:
            guardar=preguntar_guardar()
            eeg.sumar_canales(guardar=guardar)
        elif op == 3:
            guardar=preguntar_guardar()
            eeg.estadisticas_3d(guardar=guardar)
        elif op == 0:
            print("Saliendo del programa.")
            break

def menu_almacen():
    while True:
        print ("1.Listar todos los objetos guardados")
        print ("2.Buscar objeto por nombre")
        print ("3.Eliminar ojeto del almacen")
        print ("0.Volver al menu principal")
        op = validar_entero ("\n Opcion:", 0, 3)
        if op == 1:
            almacen.listar()

        elif op == 2:
            nombre=input ("Nombre del archivo (con extension): ").strip()
            obj=almacen.buscar(nombre)
            if obj is not None:
                tipo=type(obj).__name__
                print(f"Tipo: {tipo}|Ruta: {obj.ruta}")
                if isinstance(obj, ArchivoSIATA):
                    continuar=input ("Desea abrir el submenú SIATA? (s/n): ").lower()
                    if continuar == 's':
                        menu_siata(obj) 
                elif isinstance(obj, ArchivoEEG):
                    continuar=input ("Desea abrir el submenú EEG? (s/n): ").lower()
                    if continuar == 's':
                        menu_eeg(obj)
        elif op == 3:
            almacen.listar()
            nombre=input("Nomre del archivo a eliminar: ").strip()
            almacen.eliminar(nombre)
        elif op == 0:
            print("Volviendo al menú principal.")
            break

def menu_principal():
    while True:
        print("\n Menú Principal:")
        print("1. Cargar archivo SIATA")
        print("2. Cargar archivo EEG")
        print("3. Almacén de objetos")
        print("0. Salir")

        op = validar_entero ("\n Opcion:", 0, 3)
        if op == 1:
            ruta=seleccionar_archivo_csv()
            if ruta:
                try:
                    siata=ArchivoSIATA(ruta)
                    almacen.agregar(siata)
                    menu_siata(siata)

                except (FileNotFoundError, ValueError) as e:
                    print(f"Error al cargar el archivo: {e}")

        elif op == 2:
            ruta=seleccionar_archivo_mat()
            if ruta:
                try:
                    eeg=ArchivoEEG(ruta)
                    almacen.agregar(eeg)
                    menu_eeg(eeg)
                except (FileNotFoundError, ValueError) as e:
                    print(f"Error al cargar el archivo: {e}")

        elif op == 3:
            menu_almacen()

        elif op == 0:
            print("Saliendo del programa.")
            break

if __name__=="__main__":
    menu_principal()

