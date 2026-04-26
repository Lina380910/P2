import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio
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

def validar_columna (df,nombre_col):
    if nombre_col not in df.columns:
        raise KeyError(
            f"Columna '{nombre_col}' no encontrada. \n"
            f"Columnas disponibles: {list(df.columns)}"
        )
    return True

def validar_float (mensaje,minimo=None,maximo=None):
    while True:
        try:
            valor=float(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"El valor debe ser >={minimo}");continue
            if maximo is not None and valor >maximo:
                print (f"El valor debe ser <={maximo}");continue
            return valor
        except ValueError:
            print("Ingrese un numero decimal valido")

class ArchivoSIATA:

    def __init__(self, ruta_cvs):
        validar_archivo(ruta_cvs, ['.csv'])
        self.ruta_cvs = ruta_cvs
        self.nombre = os.path.basename(ruta_cvs)
        self.df = pd.read_csv(ruta_cvs)
        self._configurar_indice_fecha()
        
    def _configurar_indice_fecha(self):
        candidatos = [c for c in self.df.columns if any (p in c.lower() for p in ['fecha', 'date'])]
        if candidatos:
            self.df[candidatos[0]] = pd.to_datetime(self.df[candidatos[0]], errors='coerce')
            self.df.set_index(candidatos[0], inplace=True)
        else:
            raise ValueError("No se encontró una columna de fecha válida en el archivo.")
        
    def graficar_columna(self, col, guardar=False):
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        serie = self.df[col].dropna()
        axes[0].plot(serie)
        axes[1].boxplot(serie)
        axes[2].hist(serie, bins=20)
        plt.tight_layout()
        if guardar: plt.savefig(f"{col}_plot.png")
        plt.show()

    def operaciones(self,col):
        max_v = self.df[col].max()
        self.df[f'{col}_norm'] = self.df[col].apply(lambda x: x / max_v if max_v !=0 else 0)
        umbral = self.df[col].median()
        self.df[f'{col}_bin'] = self.df[col].apply(lambda x: 'Alto' if x > umbral else 'Bajo')
        print("operaciones aplicadas existosamente")

    def graficar_remuestreo(self, col):
        if not isinstance (self.df.index, pd.DatetimeIndex): return
        diario = self.df[col].resample('D').mean()
        mensueal = self.df[col].resample('ME').mean()
        plt.figure(figsize=(10, 5))
        plt.plot(diario, label='Diario')
        plt.plot(mensueal, label='Mensual', linewidth=3)
        plt.legend()
        plt.show()

class ArchivoEEG:

    FS=1000

    def __init__(self, ruta_mat):
        validar_archivo(ruta_mat, ['.mat'])
        self.nombre = os.path.basename(ruta_mat)
        self.data = sio.loadmat(ruta_mat)
        self.matriz = None
    def mostrar_llaves(self):
        print(f"\n Llaves en '{self.nombre}' (whosmat):")
        info=sio.whosmat(self.ruta)
        for nombre,forma,tipo in info:
            print(f" .{nombre:20s}|forma:{str(forma):20s} |tipo:{tipo}")
        return [i[0]for i in info]

    def seleccionar_llave(self):
        llaves = [l for l in self.data.keys() if not l.startswith('__') ]
        for i, l in enumerate(llaves): print(f"{i}: {l}")
        idx = validar_entero("Seleccione el indice de la matriz a analizar: ", 0, len(llaves)-1 )
        self.matriz = self.data[llaves[idx]]

    def sumar_canales (self,c1,c2,p_min,p_max):
        if self.matriz is None:return
        segmento=self.matriz[c1,p_min:p_max]+self.matriz [c2,p_min:p_max]
        plt.plot(segmento)
        plt.title (f"Suma Canales{c1} y {c2}")
        plt.show ()

import numpy as np
def estadisticas_3d (self,eje):
    if self.matriz.ndim < 3:return
    promedio=np.mean (self.matriz,axis=eje).flatten()
    plt.stem(promedio)
    plt.title(f"Promedio en eje {eje}")
    plt.show()

class AlmacenObjetos:
    def __init__(self):
        self.objetos={}
    def agregar (self,obj):
        self.objetos [obj.nombre]=obj
    def buscar (self,nombre):
        return self._objetos.get (nombre)
    def listar (self):
        return list (self._objetos.keys())
    


