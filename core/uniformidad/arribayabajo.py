import numpy as np
from scipy.stats import norm


class Arriba_Abajo:
    def __init__(self, numeros, alpha):
        self.datos = np.array(numeros)
        self.n = len(self.datos)
        self.alpha = float(alpha)

        # Validación básica para que la fórmula de varianza no falle
        if self.n < 3:
            raise ValueError(
                "Se requieren al menos 3 números para realizar la prueba de Arriba y Abajo."
            )

    def calcular(self):
        """
        Ejecuta la prueba de rachas (Arriba y Abajo) y devuelve un diccionario
        con los estadísticos y la tabla estructurada para Flet.
        """
        # Generar secuencia de signos (0: Bajada/Empate, 1: Subida)
        secuencia = []
        for i in range(self.n - 1):
            if self.datos[i] >= self.datos[i + 1]:
                secuencia.append(0)
            else:
                secuencia.append(1)

        # Contar rachas (corridas)
        corridas = 1
        for i in range(len(secuencia) - 1):
            if secuencia[i] != secuencia[i + 1]:
                corridas += 1

        # Fórmulas de Media y Varianza para la prueba
        media_es = (2 * self.n - 1) / 3
        varianza = (16 * self.n - 29) / 90

        # Cálculo del estadístico Z y el valor crítico
        z_calc = (corridas - media_es) / np.sqrt(varianza)
        z_critico = norm.ppf(1 - self.alpha / 2)

        # Criterio de aceptación: |Z calculado| <= Z crítico
        aprobado = bool(abs(z_calc) <= z_critico)

        # Construimos la tabla directamente como lista de diccionarios para Flet
        # sin necesidad de usar Pandas
        tabla_resultados = [
            {"parametro": "Rachas (R)", "valor": f"{corridas}"},
            {"parametro": "Media E(R)", "valor": f"{media_es:.4f}"},
            {"parametro": "Varianza V(R)", "valor": f"{varianza:.4f}"},
            {"parametro": "Z Calculado", "valor": f"{z_calc:.4f}"},
            {"parametro": "Z Crítico", "valor": f"{z_critico:.4f}"},
            {"parametro": "Nivel de Significancia (α)", "valor": f"{self.alpha}"},
        ]

        return {
            "n": self.n,
            "secuencia_str": "".join(
                map(str, secuencia)
            ),  # String "010110..." listo para mostrar
            "rachas": corridas,
            "estadistico_z": float(z_calc),
            "valor_critico": float(z_critico),
            "aprobado": aprobado,
            "tabla": tabla_resultados,
        }
