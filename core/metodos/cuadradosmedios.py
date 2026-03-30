class Cuadrado_medio:
    def __init__(self, semilla, n):
        self.semilla = int(semilla)
        self.n = n
        self.longitud = len(str(self.semilla))
        self.validacion()
        self.ri = []
        self.historial = []

    def validacion(self):
        if self.semilla < 0 or self.longitud % 2 != 0:
            raise ValueError("La semilla debe ser positiva y de longitud par.")

    def centro(self, v1):
        cuadrado = v1**2
        s_cuadrado = str(cuadrado).zfill(2 * self.longitud)
        inicio = (len(s_cuadrado) - self.longitud) // 2
        fin = inicio + self.longitud
        centro = s_cuadrado[inicio:fin]
        return int(centro), s_cuadrado

    def cuadradosmedios(self):
        self.ri = []
        self.historial = []
        v1 = self.semilla
        for i in range(1, self.n + 1):
            x_sig, s_cuad = self.centro(v1)
            valor_ri = x_sig / (10**self.longitud)
            self.historial.append(
                {
                    "i": i,
                    "v1": str(v1).zfill(self.longitud),
                    "cuadrado": s_cuad,
                    "x_sig": str(x_sig).zfill(self.longitud),
                    "ri": valor_ri,
                }
            )
            self.ri.append(valor_ri)
            if x_sig == 0:
                break
            v1 = x_sig
        return self.historial  # IMPORTANTE: Devolver el historial para la tabla
