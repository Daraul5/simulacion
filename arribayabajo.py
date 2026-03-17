from scipy.stats import norm
import numpy as np
import pandas as pd


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
                    print("Introduce una segunda semilla válida.")
                    self.semilla2 = int(input("Ingresa la nueva semilla: "))
            else:
                print("Introduce una primera semilla válida.")
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
        if not self.historial:
            print("No hay datos generados.")
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


class Arriba_Abajo:
    def __init__(self, numeros, alpha):
        self.datos = np.array(numeros)
        self.n = len(self.datos)
        self.alpha = alpha
        self.secuencia = []
        self.resultados = {}

    def ejecutar_prueba(self):
        corridas = 1
        self.secuencia = []

        # Generar secuencia de signos
        for i in range(self.n - 1):
            if self.datos[i] >= self.datos[i + 1]:
                self.secuencia.append(0)
            else:
                self.secuencia.append(1)

        # Contar corridas
        for i in range(len(self.secuencia) - 1):
            if self.secuencia[i] != self.secuencia[i + 1]:
                corridas += 1

        media_es = (2 * self.n - 1) / 3
        varianza = (16 * self.n - 29) / 90
        z_calc = (corridas - media_es) / np.sqrt(varianza)
        z_critico = norm.ppf(1 - self.alpha / 2)
        aprobado = abs(z_calc) <= z_critico

        self.resultados = {
            "Rachas (R)": corridas,
            "Media E(R)": media_es,
            "Varianza V(R)": varianza,
            "Z Calculado": z_calc,
            "Z Crítico": z_critico,
            "Alpha": self.alpha,
            "Aprobado": aprobado,
        }
        return self.resultados

    def obtener_tabla(self):
        df = pd.DataFrame(list(self.resultados.items()), columns=["Parámetro", "Valor"])
        return df

    def imprimir_reporte(self):
        if not self.resultados:
            self.ejecutar_prueba()

        tabla = self.obtener_tabla()
        aprobado = self.resultados["Aprobado"]

        print("\n" + "=" * 60)
        print(" REPORTE DE PRUEBA DE RACHAS (ARRIBA Y ABAJO)")
        print("=" * 60)

        print("SECUENCIA DE SIGNOS (0: Bajada/Empate, 1: Subida):")
        secuencia_str = "".join(map(str, self.secuencia))
        print(secuencia_str)
        print("-" * 60)

        # Imprimimos la tabla de resultados
        print(tabla.to_string(index=False))

        print("-" * 60)
        print(f"Estadístico Z Calculado      : {self.resultados['Z Calculado']:.4f}")
        print(f"Valor Crítico Z(α/2)         : {self.resultados['Z Crítico']:.4f}")
        print(f"Nivel de Significancia (α)   : {self.alpha}")
        print(f"Tamaño de la Muestra (n)     : {self.n}")
        print("-" * 60)

        if aprobado:
            print("CONCLUSIÓN: SE ACEPTA H0.")
            print("Los números presentan un comportamiento aleatorio (Independencia).")
        else:
            print("CONCLUSIÓN: SE RECHAZA H0.")
            print("Los números NO presentan un comportamiento aleatorio.")
        print("=" * 60 + "\n")


# --- Bloque de ejecución ---
try:
    seed1 = int(input("Introduce la primera semilla (par y >0): "))
    seed2 = int(input("Introduce la segunda semilla (par y misma longitud): "))
    iteraciones = int(input("Introduce las iteraciones: "))

    gen = Producto_medio(seed1, seed2, iteraciones)
    lista_ri = gen.productosmedios()
    gen.imprimir_tabla()

    prueba = Arriba_Abajo(lista_ri, 0.05)
    prueba.imprimir_reporte()
except ValueError:
    print("Error: Por favor introduce solo números enteros.")
