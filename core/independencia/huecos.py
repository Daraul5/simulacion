import numpy as np
from scipy.stats import chi2


class Prueba_Huecos:
    def __init__(self, numeros, alpha, limite_inf=0.1, limite_sup=0.5, max_gap=5):
        self.datos = np.array(numeros)
        self.n = len(self.datos)
        self.alpha = float(alpha)
        self.lim_inf = float(limite_inf)
        self.lim_sup = float(limite_sup)
        self.max_gap = int(max_gap)

        if self.n < 10:
            raise ValueError(
                "Se requieren más datos para realizar la prueba de Huecos."
            )
        if self.lim_inf >= self.lim_sup:
            raise ValueError(
                "El límite inferior debe ser estrictamente menor al límite superior."
            )
        if not (0 <= self.lim_inf <= 1) or not (0 <= self.lim_sup <= 1):
            raise ValueError("Los límites del intervalo deben estar entre 0 y 1.")

    def calcular(self):
        """
        Ejecuta la prueba de Huecos, calcula las frecuencias y aplica Chi-Cuadrada.
        Devuelve un diccionario listo para la interfaz gráfica.
        """
        # 1. Identificar si cada número cae dentro del intervalo (1) o fuera (0)
        en_intervalo = [(self.lim_inf <= x <= self.lim_sup) for x in self.datos]

        huecos = []
        contador_hueco = 0
        contando = False

        # 2. Contar la longitud de los huecos
        for estado in en_intervalo:
            if estado:
                if contando:
                    huecos.append(contador_hueco)
                contador_hueco = 0
                contando = True
            else:
                if contando:
                    contador_hueco += 1

        total_huecos = len(huecos)
        if total_huecos == 0:
            raise ValueError(
                "Ningún número cayó dentro del intervalo. No hay huecos para evaluar."
            )

        # 3. Calcular Frecuencias Observadas (Oi)
        frecuencias_obs = {i: 0 for i in range(self.max_gap + 1)}
        for h in huecos:
            if h >= self.max_gap:
                frecuencias_obs[self.max_gap] += 1
            else:
                frecuencias_obs[h] += 1

        # 4. Calcular Frecuencias Esperadas (Ei)
        # Probabilidad de caer en el intervalo (p) y de no caer (q)
        p = self.lim_sup - self.lim_inf
        q = 1 - p

        frecuencias_esp = {}
        for i in range(self.max_gap):
            # E_i = Total de huecos * p * q^i
            frecuencias_esp[i] = total_huecos * p * (q**i)

        # Para la categoría acumulada (>= max_gap)
        frecuencias_esp[self.max_gap] = total_huecos * (q**self.max_gap)

        # 5. Calcular Chi-Cuadrada
        chi_calculada = 0
        tabla_resultados = []

        for i in range(self.max_gap + 1):
            oi = frecuencias_obs[i]
            ei = frecuencias_esp[i]

            # Evitar división por cero en chi parcial
            chi_parcial = ((oi - ei) ** 2) / ei if ei > 0 else 0
            chi_calculada += chi_parcial

            categoria = f"{i}" if i < self.max_gap else f"≥ {self.max_gap}"
            tabla_resultados.append(
                {
                    "tamaño_hueco": categoria,
                    "oi": oi,
                    "ei": f"{ei:.4f}",
                    "chi_parcial": f"{chi_parcial:.4f}",
                }
            )

        # Grados de libertad = Categorías (max_gap + 1) - 1
        grados_libertad = self.max_gap
        valor_critico = chi2.ppf(1 - self.alpha, grados_libertad)
        aprobado = bool(chi_calculada <= valor_critico)

        return {
            "n": self.n,
            "intervalo_str": f"[{self.lim_inf}, {self.lim_sup}]",
            "total_huecos": total_huecos,
            "grados_libertad": grados_libertad,
            "estadistico_chi2": float(chi_calculada),
            "valor_critico": float(valor_critico),
            "aprobado": aprobado,
            "tabla": tabla_resultados,
        }
