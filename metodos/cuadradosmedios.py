class Cuadrado_medio:

    def __init__(self, semilla, n):
        self.semilla = semilla
        self.n = n
        self.longitud = len(str(self.semilla))
        self.validacion()
        self.ri = []
        self.historial = []

    def validacion(self):
        while True:
            if self.semilla > 0 and self.longitud % 2 == 0:
                break
            else:
                print(
                    "Error: La semilla debe ser positiva y tener un número par de dígitos."
                )
                self.semilla = int(input("Ingresa una nueva semilla: "))
                self.longitud = len(str(self.semilla))

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
        return self.ri

    def imprimir_tabla(self):
        if not self.historial:
            print("No hay datos generados. Llama primero a .generar()")
            return
        print(
            f"\n{'i':<5} | {'Xi-1':<10} | {'Cuadrado':<15} | {'Centro':<15} | {'Ri':<8}"
        )
        print("-" * 75)
        for fila in self.historial:
            print(
                f"{fila['i']:<5} | {fila['v1']:<10} | "
                f"{fila['cuadrado']:<15} | {fila['x_sig']:<15} | {fila['ri']:.4f}"
            )
