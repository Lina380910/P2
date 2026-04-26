import os

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
            