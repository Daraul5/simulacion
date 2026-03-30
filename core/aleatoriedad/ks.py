import numpy as np
import pandas as pd
from scipy.stats import ksone


class KS_metodo:
    def __init__(self, numeros, alpha):
        # La prueba KS exige que los datos estén ordenados de menor a mayor
        self.datos = sorted(np.array(numeros))
        self.n = len(self.datos)
        self.alpha = float(alpha)

        # Lanzamos el error directamente para que Flet lo atrape en la interfaz
        if self.n > 40:
            raise ValueError(
                "El método KS está limitado a un máximo de 40 números para esta prueba."
            )
        if self.n == 0:
            raise ValueError("No hay datos para evaluar.")

    def calcular(self):
        """
        Ejecuta la prueba de Kolmogorov-Smirnov y devuelve un diccionario
        con los estadísticos y la tabla de resultados lista para Flet.
        """
        d_plus = []
        d_minus = []

        for i in range(1, self.n + 1):
            ri = self.datos[i - 1]
            d_plus.append((i / self.n) - ri)
            d_minus.append(ri - ((i - 1) / self.n))

        max_d_plus = max(d_plus)
        max_d_minus = max(d_minus)
        d_estadistico = max(max_d_plus, max_d_minus)

        # Obtenemos el valor crítico de la tabla KS
        valor_critico = ksone.ppf(1 - self.alpha / 2, self.n)

        # Criterio de aceptación: Estadístico D < Valor crítico
        aprobado = bool(d_estadistico < valor_critico)

        # Preparamos el DataFrame y lo convertimos a diccionarios
        df_resultados = pd.DataFrame(
            {
                "i": range(1, self.n + 1),
                "ri": self.datos,
                "d_mas": d_plus,
                "d_menos": d_minus,
            }
        )

        return {
            "estadistico_ks": float(d_estadistico),
            "valor_critico": float(valor_critico),
            "aprobado": aprobado,
            "tabla": df_resultados.to_dict(orient="records"),
        }
