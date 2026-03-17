import numpy as np
import pandas as pd
from scipy.stats import chi2


class Prueba_chi2:

    def __init__(self, numeros, alpha):
        self.datos = np.array(numeros)
        self.n = len(self.datos)
        self.alpha = alpha
        self.m = int(np.sqrt(self.n))
        if self.n < 5:
            raise ValueError(
                "SE REQUIEREN MAS DATOS PARA REALIZAR LAS PRUEBAS DE CONFIANZA"
            )
        resultados = self.evaluar()
        self.imprimir_reporte(resultados)

    def evaluar(self):
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

        df_resultados = pd.DataFrame(
            {
                "Intervalo": etiquetas_intervalos,
                "Oi (Observada)": frecuenciaob,
                "Ei (Esperada)": frecuenciaes,
                "Chi_Parcial": ((frecuenciaob - frecuenciaes) ** 2) / frecuenciaes,
            }
        )
        aprobado = chicalculada < valor_critico

        return {
            "Estadistico_Chi2": chicalculada,
            "Valor_Critico": valor_critico,
            "Grados_Libertad": grados_libertad,
            "Aprobado": aprobado,
            "Tabla": df_resultados,
        }

    def imprimir_reporte(self, resultados):
        """Muestra el Dataframe y la conclusión de la prueba en consola."""
        print("\n" + "=" * 50)
        print(" REPORTE DE PRUEBA DE CHI-CUADRADA")
        print("=" * 50)
        print(resultados["Tabla"].to_string(index=False))
        print("-" * 50)
        print(f"Suma Chi-Cuadrada Calculada : {resultados['Estadistico_Chi2']:.4f}")
        print(f"Valor Crítico (Tabla)       : {resultados['Valor_Critico']:.4f}")
        print(f"Grados de Libertad          : {resultados['Grados_Libertad']}")
        print("-" * 50)

        if resultados["Aprobado"]:
            print("CONCLUSIÓN: SE ACEPTA H0.")
            print(
                "Los números presentan una distribución uniforme estadísticamente válida."
            )
        else:
            print("CONCLUSIÓN: SE RECHAZA H0.")
            print("Los números NO presentan una distribución uniforme.")
        print("=" * 50 + "\n")
