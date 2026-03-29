class Multiplicador_constante:
    def __init__(self, a, semilla, n):
        self.a = a
        self.semilla = semilla
        self.n = n
        self.longitud = len(str(self.semilla))

    def validacion(self):
        if self.a < 0:
            raise ValueError("la constante multiplicativa debe ser positiva")
        if not isinstance(self.a, int):
            raise ValueError("la constante multiplicativa debe ser un numero entero")
        if self.semilla < 0:
            raise ValueError("la semilla debe ser positiva")
        if not isinstance(self.semilla, int):
            raise ValueError("la semilla debe ser un numero entero")
        if self.n < 0:
            raise ValueError("el numero de iteraciones debe ser positivo")
        if not isinstance(self.n, int):
            raise ValueError("el numero de iteraciones debe ser un numero entero")
        if self.longitud % 2 != 0:
            raise ValueError("la semilla debe tener un numero par de digitos")

    def centro(self, cte, actual):
        producto = cte * actual
        prod_norm = str(producto).zfill(2 * self.longitud)
        inicio = (len(prod_norm) - self.longitud) // 2
        fin = inicio + self.longitud
        centro = prod_norm[inicio:fin]
        return prod_norm, int(centro)
    
    def multiplicadorconstante(self):
        self.ri = []
        self.historial = []
        a = self.a
        xn = self.semilla
        for i in range(1, self.n + 1):
            p_norm, x_siguiente = self.centro(a, xn)
            valor_ri = x_siguiente / (10**self.longitud)
            self.historial.append(
                {
                    "i": i,
                    "a": a,
                    "xn": str(xn).zfill(self.longitud),
                    "producto": p_norm,
                    "x_sig": str(x_siguiente).zfill(self.longitud),
                    "ri": valor_ri,
                }
            )
            self.ri.append(valor_ri)
            xn = x_siguiente
            if xn == 0:
                break
        return self.historial
