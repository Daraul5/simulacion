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
        # 1. Errores críticos que la matemática no puede perdonar
        if self.modulo <= 0:
            raise ValueError("El módulo (m) no puede ser cero ni negativo.")
        if self.a < 0 or self.semilla < 0 or self.c < 0:
            raise ValueError("Los parámetros a, semilla y c no pueden ser negativos.")

        # 2. AUTO-CORRECCIÓN: Reglas del Generador Lineal
        # El módulo siempre debe ser estrictamente mayor que a, X0 y c.
        valor_maximo = max(self.a, self.semilla, self.c)

        if self.modulo <= valor_maximo:
            # Ajustamos el módulo automáticamente para que sea válido
            self.modulo = valor_maximo + 1

            # Actualizamos la longitud por si el nuevo módulo tiene más dígitos
            self.longitud = len(str(self.modulo))

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
        return self.historial
