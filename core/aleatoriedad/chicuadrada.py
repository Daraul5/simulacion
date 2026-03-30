import numpy as np
import pandas as pd
from scipy.stats import chi2


class Prueba_chi2:
    def __init__(self, numeros, alpha):
        self.datos = np.array(numeros)
        self.n = len(self.datos)
        self.alpha = alpha

        if self.n < 5:
            raise ValueError(
                "Se requieren al menos 5 datos para realizar las pruebas de confianza."
            )

        self.m = int(np.sqrt(self.n))

    def calcular(self):

        frecuenciaob, limites_intervalos = np.histogram(
            self.datos, bins=self.m, range=(0.0, 1.0)
        )
        frecuenciaes = self.n / self.m
        chicalculada = np.sum(((frecuenciaob - frecuenciaes) ** 2) / frecuenciaes)
        grados_libertad = self.m - 1
        valor_critico = chi2.ppf(1 - self.alpha, grados_libertad)

        etiquetas_intervalos = [
            f"[{limites_intervalos[i]:.4f}, {limites_intervalos[i+1]:.4f})"
            for i in range(self.m)
        ]

        # DataFrame temporal para organizar los datos
        df_resultados = pd.DataFrame(
            {
                "intervalo": etiquetas_intervalos,
                "oi": frecuenciaob,
                "ei": frecuenciaes,
                "chi_parcial": ((frecuenciaob - frecuenciaes) ** 2) / frecuenciaes,
            }
        )

        aprobado = bool(chicalculada < valor_critico)

        return {
            "estadistico_chi2": float(chicalculada),
            "valor_critico": float(valor_critico),
            "grados_libertad": int(grados_libertad),
            "aprobado": aprobado,
            # Convertimos el DataFrame a una lista de diccionarios para iterar en Flet
            "tabla": df_resultados.to_dict(orient="records"),
        }
