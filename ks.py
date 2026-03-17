import numpy as np
import pandas as pd
from scipy.stats import ksone


class KS_metodo:
    def __init__(self, numeros, alpha):
        self.datos = sorted(np.array(numeros))
        self.n = len(self.datos)
        self.alpha = alpha
        self.d_plus = []
        self.d_minus = []
        self.d_estadistico = 0
        self.validacion()

    def validacion(self):
        try:
            if self.n > 40:
                raise ValueError("demasiados numeros")
            self.evaluar()
            self.imprimir_reporte_ks()
        except ValueError as e:
            print(f"\nError: {e}")

    def evaluar(self):
        for i in range(1, self.n + 1):
            ri = self.datos[i - 1]
            self.d_plus.append((i / self.n) - ri)
            self.d_minus.append(ri - ((i - 1) / self.n))

        max_d_plus = max(self.d_plus)
        max_d_minus = max(self.d_minus)
        self.d_estadistico = max(max_d_plus, max_d_minus)
        return self.d_estadistico

    def obtener_tabla(self):
        df = pd.DataFrame(
            {
                "i": range(1, self.n + 1),
                "ri": self.datos,
                "DMAS": self.d_plus,
                "DMENOS": self.d_minus,
            }
        )
        return df

    def obtener_valor_critico(self):
        return ksone.ppf(1 - self.alpha / 2, self.n)

    def imprimir_reporte_ks(self):
        """Muestra el Dataframe y la conclusión de la prueba KS en consola."""
        tabla = self.obtener_tabla()
        valor_critico = self.obtener_valor_critico()
        aprobado = self.d_estadistico < valor_critico

        print("\n" + "=" * 60)
        print(" REPORTE DE PRUEBA DE KOLMOGOROV-SMIRNOV (K-S)")
        print("=" * 60)

        # Imprimimos la tabla de pandas con formato limpio
        print(tabla.to_string(index=False))

        print("-" * 60)
        print(f"Estadístico D Calculado      : {self.d_estadistico:.4f}")
        print(f"Valor Crítico (Tabla)        : {valor_critico:.4f}")
        print(f"Nivel de Significancia (α)   : {self.alpha}")
        print(f"Tamaño de la Muestra (n)     : {self.n}")
        print("-" * 60)

        if aprobado:
            print("CONCLUSIÓN: SE ACEPTA H0.")
            print(
                "Los números presentan una distribución uniforme estadísticamente válida."
            )
        else:
            print("CONCLUSIÓN: SE RECHAZA H0.")
            print("Los números NO presentan una distribución uniforme.")
        print("=" * 60 + "\n")
