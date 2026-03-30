import numpy as np
from collections import Counter
from scipy.stats import chi2


class Prueba_Poker:
    def __init__(self, numeros, alpha):
        self.datos = numeros
        self.n = len(self.datos)
        self.alpha = float(alpha)

        if self.n < 5:
            raise ValueError("Se requieren al menos 5 números para la prueba de Poker.")

        # Definimos las probabilidades esperadas según la cantidad de decimales
        self.probabilidades = {
            5: {
                "Todos Diferentes (TD)": 0.3024,
                "Un Par (1P)": 0.5040,
                "Dos Pares (2P)": 0.1080,
                "Tercia (T)": 0.0720,
                "Full House (FH)": 0.0090,
                "Poker (P)": 0.0045,
                "Quintilla (Q)": 0.0001,
            },
            4: {
                "Todos Diferentes (TD)": 0.5040,
                "Un Par (1P)": 0.4320,
                "Dos Pares (2P)": 0.0270,
                "Tercia (T)": 0.0360,
                "Poker (P)": 0.0010,
            },
            3: {
                "Todos Diferentes (TD)": 0.720,
                "Un Par (1P)": 0.270,
                "Tercia (T)": 0.010,
            },
        }

    def _determinar_longitud_y_normalizar(self):
        """Detecta la cantidad de decimales dominante y normaliza el arreglo."""
        longitudes = []
        for num in self.datos:
            # Evitamos notación científica y sacamos la parte decimal
            s_num = f"{float(num):.10f}".rstrip("0").split(".")[-1]
            longitudes.append(len(s_num) if s_num else 1)

        # Obtenemos la longitud más común (la moda)
        moda_longitud = Counter(longitudes).most_common(1)[0][0]

        # Acotamos estrictamente a 3, 4 o 5
        decimales_objetivo = max(3, min(moda_longitud, 5))

        # Normalizamos todos los números a esa cantidad exacta de decimales
        datos_normalizados = []
        for num in self.datos:
            # Forzamos el formato a N decimales, esto trunca y pule automáticamente
            str_formateado = f"{float(num):.{decimales_objetivo}f}"
            parte_decimal = str_formateado.split(".")[-1]
            datos_normalizados.append(parte_decimal)

        return decimales_objetivo, datos_normalizados

    def _clasificar_mano(self, decimales_str, longitud):
        """Identifica la 'mano' de poker contando la frecuencia de los dígitos."""
        frecuencias = sorted(list(Counter(decimales_str).values()), reverse=True)

        if longitud == 5:
            if frecuencias == [1, 1, 1, 1, 1]:
                return "Todos Diferentes (TD)"
            if frecuencias == [2, 1, 1, 1]:
                return "Un Par (1P)"
            if frecuencias == [2, 2, 1]:
                return "Dos Pares (2P)"
            if frecuencias == [3, 1, 1]:
                return "Tercia (T)"
            if frecuencias == [3, 2]:
                return "Full House (FH)"
            if frecuencias == [4, 1]:
                return "Poker (P)"
            if frecuencias == [5]:
                return "Quintilla (Q)"

        elif longitud == 4:
            if frecuencias == [1, 1, 1, 1]:
                return "Todos Diferentes (TD)"
            if frecuencias == [2, 1, 1]:
                return "Un Par (1P)"
            if frecuencias == [2, 2]:
                return "Dos Pares (2P)"
            if frecuencias == [3, 1]:
                return "Tercia (T)"
            if frecuencias == [4]:
                return "Poker (P)"

        elif longitud == 3:
            if frecuencias == [1, 1, 1]:
                return "Todos Diferentes (TD)"
            if frecuencias == [2, 1]:
                return "Un Par (1P)"
            if frecuencias == [3]:
                return "Tercia (T)"

        raise ValueError(f"Frecuencia no reconocida para {decimales_str}")

    def calcular(self):
        """Calcula las frecuencias, aplica Chi-Cuadrada y devuelve el diccionario UI."""
        decimales_obj, datos_norm = self._determinar_longitud_y_normalizar()
        prob_actuales = self.probabilidades[decimales_obj]

        # Inicializamos el conteo en 0 para todas las categorías posibles
        conteos = {categoria: 0 for categoria in prob_actuales.keys()}

        # Clasificamos cada número normalizado
        for d_str in datos_norm:
            categoria = self._clasificar_mano(d_str, decimales_obj)
            conteos[categoria] += 1

        # Realizamos la prueba Chi-Cuadrada
        chi_calculada = 0
        tabla_resultados = []

        for categoria, oi in conteos.items():
            probabilidad = prob_actuales[categoria]
            ei = self.n * probabilidad

            # Cálculo de Chi parcial protegiendo divisiones por cero
            chi_parcial = ((oi - ei) ** 2) / ei if ei > 0 else 0
            chi_calculada += chi_parcial

            tabla_resultados.append(
                {
                    "categoria": categoria,
                    "oi": oi,
                    "ei": f"{ei:.4f}",
                    "chi_parcial": f"{chi_parcial:.4f}",
                }
            )

        # Grados de libertad = (Número de categorías) - 1
        grados_libertad = len(prob_actuales) - 1
        valor_critico = chi2.ppf(1 - self.alpha, grados_libertad)
        aprobado = bool(chi_calculada <= valor_critico)

        return {
            "n": self.n,
            "decimales_evaluados": decimales_obj,
            "grados_libertad": grados_libertad,
            "estadistico_chi2": float(chi_calculada),
            "valor_critico": float(valor_critico),
            "aprobado": aprobado,
            "tabla": tabla_resultados,
        }
