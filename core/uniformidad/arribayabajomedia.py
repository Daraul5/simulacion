import numpy as np
from scipy.stats import norm


class Arriba_Abajo_Media:
    def __init__(self, numeros, alpha):
        self.datos = np.array(numeros)
        self.n = len(self.datos)
        self.alpha = float(alpha)

        if self.n < 2:
            raise ValueError("Se requieren al menos 2 números para realizar la prueba.")

    def calcular(self):
        """
        Ejecuta la prueba de rachas respecto a la media y devuelve un diccionario
        con los estadísticos y la tabla estructurada para Flet.
        """
        # 1. Calcular la media de la muestra
        media_muestra = np.mean(self.datos)

        # 2. Generar secuencia de signos (1: Arriba/Igual a la media, 0: Abajo de la media)
        secuencia = []
        n1 = 0  # Contador de números por encima o iguales a la media
        n2 = 0  # Contador de números por debajo de la media

        for num in self.datos:
            if num >= media_muestra:
                secuencia.append(1)
                n1 += 1
            else:
                secuencia.append(0)
                n2 += 1

        # Validación de seguridad matemática
        if n1 == 0 or n2 == 0:
            raise ValueError(
                "Todos los números están del mismo lado de la media. No se puede calcular la varianza."
            )

        # 3. Contar rachas (corridas)
        corridas = 1
        for i in range(len(secuencia) - 1):
            if secuencia[i] != secuencia[i + 1]:
                corridas += 1

        # 4. Fórmulas de Media y Varianza para la prueba respecto a la media
        # n = n1 + n2 (Total de datos)
        media_es = ((2 * n1 * n2) / self.n) + 1
        varianza = (2 * n1 * n2 * (2 * n1 * n2 - self.n)) / ((self.n**2) * (self.n - 1))

        # 5. Cálculo del estadístico Z y el valor crítico
        z_calc = (corridas - media_es) / np.sqrt(varianza)
        z_critico = norm.ppf(1 - self.alpha / 2)

        # 6. Criterio de aceptación: |Z calculado| <= Z crítico
        aprobado = bool(abs(z_calc) <= z_critico)

        # Construimos la tabla directamente como lista de diccionarios para Flet
        tabla_resultados = [
            {"parametro": "Media de la muestra", "valor": f"{media_muestra:.4f}"},
            {"parametro": "Datos ≥ Media (n1)", "valor": f"{n1}"},
            {"parametro": "Datos < Media (n2)", "valor": f"{n2}"},
            {"parametro": "Rachas (R)", "valor": f"{corridas}"},
            {"parametro": "Media E(R)", "valor": f"{media_es:.4f}"},
            {"parametro": "Varianza V(R)", "valor": f"{varianza:.4f}"},
            {"parametro": "Z Calculado", "valor": f"{z_calc:.4f}"},
            {"parametro": "Z Crítico", "valor": f"{z_critico:.4f}"},
            {"parametro": "Nivel de Significancia (α)", "valor": f"{self.alpha}"},
        ]

        return {
            "n": self.n,
            "secuencia_str": "".join(map(str, secuencia)),
            "media_muestra": float(media_muestra),
            "n1": n1,
            "n2": n2,
            "rachas": corridas,
            "estadistico_z": float(z_calc),
            "valor_critico": float(z_critico),
            "aprobado": aprobado,
            "tabla": tabla_resultados,
        }
