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
