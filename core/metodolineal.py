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
        if self.a < 0:
            raise ValueError("el multiplicador debe de ser positivo")
        if self.semilla < 0:
            raise ValueError("la semilla debe de ser positiva")
        if self.c < 0:
            raise ValueError("el elemento aditivo debe de ser positivo")
        if self.modulo < 0:
            raise ValueError("el modulo debe de ser positivo") 
        
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
    