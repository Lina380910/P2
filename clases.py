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
        llaves = self.mostrar_llaves()
        llaves_validas = [l for l in llaves if not l.startswith('__') ]
        for i, l in enumerate(llaves_validas):
            print(f"{i}: {l}")
        idx=validar_entero("Seleccione el indice de la llave a cargar: ", 0, len(llaves_validas)-1)
        self.llave=llaves_validas [idx]
        self.matriz=self.data[self.llave]
        print(f"llave '{self.llave}' cargada con forma {self.matriz.shape}")

    def sumar_canales (self,guardar=False,carpeta="graficos"):
        if self.matriz is None:
            print("Primero seleccione una llave con 'seleccionar_llave()'.")
            return
        mat=self.matriz
        if mat.ndim ==3:
            mat=mat.reshape (mat.shape[0],-1)
        elif mat.ndim ==1:
            mat=mat.reshape (-1,1)
        n_canales,n_muestras=mat.shape
        print (f"\n Matriz convertida a 2D:{n_canales}canales x {n_muestras} muestras")

        canales=[]
        for i in range (1,4):
            c=validar_entero (
                f"Canal {i} (0 a {n_canales-1}):",0, n_canales-1)
            canales.append(c)
        
        print(f"\n Rango disponible: 0 a {n_muestras-1} muestras")
        p_min = validar_entero ("Punto minimo (muestra):",0, n_muestras-2)
        p_max = validar_entero ("Punto maximo (muestra):",p_min+1, n_muestras-1)

        t=np.arange (p_min,p_max)/self.FS

        segmentos =[mat[c,p_min:p_max]for c in canales]
        suma=segmentos[0]+segmentos[1]+segmentos[2]

        fig, (ax1,ax2)=plt.subplots (2,1, figsize=(13,7), sharex=True)
        fig.suptitle (f"Suma de canales {self.nombre}",fontsize=13, fontweight="bold")

        colores=['blue','orange','green']
        for seg,c,color in zip (segmentos,canales,colores):
            ax1.plot (t,seg,label=f"Canal {c}",color=color)
        ax1.set_title("Canales individuales")
        ax1.set_ylabel("Amplitud")
        ax1.legend()

        ax2.plot (t,suma,label="Suma",color='crimson')
        ax2.set_title("Suma de canales")
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel("Amplitud")
        ax2.legend()

        plt.tight_layout()
        if guardar:
            os.makedirs(carpeta, exist_ok=True)
            ruta=os.path.join(carpeta, f"suma_canales_{self.nombre}.png")
            plt.savefig(ruta)
            print(f"Grafico guardado en: {ruta}")
        plt.show()


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
    


