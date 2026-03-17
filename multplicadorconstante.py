class Multiplicador_constante:
    def __init__(self, a, semilla, n):
        self.a = a
        self.semilla = semilla
        self.n = n
        self.longitud = len(str(self.semilla))

    def validacion(self):
        while True:
            if self.semilla > 0 and self.longitud % 2 == 0:
                if self.a > 0 and len(str(self.a)) == self.longitud:
                    break
                else:
                    print("introduzca un multiplicador valido")
                    self.a = int(input("introduce el nuevo multiplicador "))
            else:
                print("introduce una semilla valida")
                self.semilla = int(input("itroduzca la nueva semilla: "))
                self.longitud = len(str(self.semilla))

    def mmultiplicadorconstante(self, cte, actual):
        producto = cte * actual
        prod_norm = str(producto).zfill(2 * self.longitud)
        inicio = (len(prod_norm) - self.longitud) // 2
        fin = inicio + self.longitud
        centro = prod_norm[inicio:fin]
        return prod_norm, int(centro)

    def imprimir(self):
        print(
            f"\n{'Iter (i)':<8} | {'Constante (a)':<13} | {'Xn':<8} | {'Producto (Norm)':<15} | {'Xn+1':<8} | {'Ri':<8}"
        )
        print("-" * 85)
        a = self.a
        xn = self.semilla
        for i in range(1, self.n + 1):
            p_norm, x_siguiente = self.mmultiplicadorconstante(a, xn)
            ri = x_siguiente / (10**self.longitud)
            print(
                f"{i:<8} | {a:<13} | {str(xn).zfill(self.longitud):<8} | {p_norm:<15} | {x_siguiente:0{self.longitud}d} | {ri:.4f}"
            )
            xn = x_siguiente
            if xn == 0:
                break
