import numpy as np
import pandas as pd
from scipy.stats import chi2


class Producto_medio:

    def __init__(self, semilla1, semilla2, n):
        self.semilla1 = int(semilla1)
        self.semilla2 = int(semilla2)
        self.n = n
        self.longitud = len(str(self.semilla1))
        self.validacion()
        self.ri = []
        self.historial = []

    def centro(self, valor_actual1, valor_actual2):
        cuadrado = valor_actual1 * valor_actual2
        s_producto = str(cuadrado).zfill(2 * self.longitud)
        inicio = (len(s_producto) - self.longitud) // 2
        fin = inicio + self.longitud
        centro = s_producto[inicio:fin]
        return int(centro), s_producto

    def validacion(self):
        while True:
            if self.semilla1 > 0 and self.longitud % 2 == 0:
                if (
                    self.semilla2 > 0
                    and len(str(self.semilla2)) % 2 == 0
                    and self.longitud == len(str(self.semilla2))
                ):
                    break
                else:
                    print("introduce una segunda semilla valida ")
                    self.semilla2 = int(input("Ingresa la nueva semilla: "))
            else:
                print("Introduce una primera semilla valida ")
                self.semilla1 = int(input("Ingresa la nueva semilla: "))
                self.longitud = len(str(self.semilla1))

    def productosmedios(self):
        self.ri = []
        self.historial = []
        v1, v2 = self.semilla1, self.semilla2
        for i in range(1, self.n + 1):
            x_sig, s_prod = self.centro(v1, v2)
            valor_ri = x_sig / (10**self.longitud)
            self.historial.append(
                {
                    "i": i,
                    "v1": str(v1).zfill(self.longitud),
                    "v2": str(v2).zfill(self.longitud),
                    "producto": s_prod,
                    "x_sig": str(x_sig).zfill(self.longitud),
                    "ri": valor_ri,
                }
            )
            self.ri.append(valor_ri)
            if x_sig == 0:
                break
            v1, v2 = v2, x_sig
        return self.ri

    def imprimir_tabla(self):
        """Muestra los datos generados previamente."""
        if not self.historial:
            print("No hay datos generados. Llama primero a .generar()")
            return
        print(
            f"\n{'i':<5} | {'Xi-1':<10} | {'Xi':<10} | {'Producto':<15} | {'Centro':<15} | {'Ri':<8}"
        )
        print("-" * 75)
        for fila in self.historial:
            print(
                f"{fila['i']:<5} | {fila['v1']:<10} | {fila['v2']:<10} | "
                f"{fila['producto']:<15} | {fila['x_sig']:<15} | {fila['ri']:.4f}"
            )


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


gen = Producto_medio(2500, 2500, 4)
lista_ri = gen.productosmedios()
gen.imprimir_tabla()
chi_cuadrada = Prueba_chi2(lista_ri, 0.05)
resultados = chi_cuadrada.evaluar()
chi_cuadrada.imprimir_reporte(resultados)
