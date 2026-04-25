import pandas as pd
import matplotlib.pyplot as plt
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