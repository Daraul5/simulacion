class Metodo_lineal:

    def __init__(self, a, semilla, c, modulo, n):
        self.a = a
        self.semilla = semilla
        self.c = c
        self.modulo = modulo
        self.longitud = len(str(self.modulo))
        self.n = n
        self.validacion()
        self.ri = []
        self.historial = []

    def validacion(self):
        while True:
            if self.a > 0 and self.semilla > 0 and self.c > 0 and self.modulo > 0:
                break
            else:
                print("introduce datos correctos")
                self.a = int(input())
                self.semilla = int(input())
                self.c = int(input())
                self.modulo = int(input())

    def metodolineal(self):
        self.ri = []
        self.historial = []
        v1 = self.semilla
        a = self.a
        c = self.c
        modulo = self.modulo
        for i in range(1, self.n + 1):
            p_norm_val = a * v1 + c
            x_sig = p_norm_val % modulo
            ri = x_sig / modulo
            self.historial.append(
                {
                    "i": i,
                    "a": a,
                    "v1": str(v1).zfill(self.longitud),
                    "c": c,
                    "modulo": modulo,
                    "normalizado": p_norm_val,
                    "x_sig": str(x_sig).zfill(self.longitud),
                    "ri": ri,
                }
            )
            self.ri.append(ri)
            if x_sig == 0:
                break
            v1 = x_sig

    def imprimir_tabla(self):
        if not self.historial:
            print("No hay datos generados. Llama primero a .metodolineal()")
            return

        # Encabezados de la tabla
        print(
            f"\n{'i':<5} | {'Xi-1':<10} | {'(a*Xi-1 + c)':<15} | {'(a*Xi-1 + c) mod m':<20} | {'Ri':<8}"
        )
        print("-" * 70)

        for fila in self.historial:
            # Extraemos los datos del diccionario de historial
            i = fila["i"]
            xi_1 = fila["v1"]
            normalizado = fila["normalizado"]
            x_sig = fila["x_sig"]
            ri = fila["ri"]

            print(
                f"{i:<5} | "
                f"{xi_1:<10} | "
                f"{normalizado:<15} | "
                f"{x_sig:<20} | "
                f"{ri:.4f}"
            )
