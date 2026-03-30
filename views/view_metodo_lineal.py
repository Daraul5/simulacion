import flet as ft
from core.metodolineal import Metodo_lineal
import math
class VistaMetodoLineal(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = 20
        self.datos_completos = []
        self.pagina_actual = 0
        self.filas_por_pagina = 100
        self.content = self.build_ui()

    def build_ui(self):
        self.bar = ft.AppBar(title=ft.Text("Generador de Números Aleatorios - Método Lineal"), center_title=True)
        self.tittle = ft.Text("Generador de Números Aleatorios - Método Lineal", size=24, weight=ft.FontWeight.BOLD)
        self.txt_a = ft.TextField(label="Multiplicador (a)", width=200)
        self.txt_semilla = ft.TextField(label="Semilla (X0)", width=200)
        self.txt_C = ft.TextField(label="Aditivo (c)", width=200)
        self.txt_modulo = ft.TextField(label="Modulo (m)", width=200)
        self.txt_n = ft.TextField(label="Iteraciones (n)", width=200)
        
        # NOTE: Event functions need an 'e' parameter
        self.btn_generar = ft.Button("Generar", on_click=self.procesar_datos)
        # En build_ui, cambia la línea del btn_clear por esto:
        self.btn_clear = ft.Button("Limpiar", on_click=self.limpiar_datos)
        self.lbl_error = ft.Text(color=ft.Colors.ERROR, size=14, weight=ft.FontWeight.BOLD)

        self.btn_prev = ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.pagina_anterior, disabled=True)
        self.btn_next = ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=self.pagina_siguiente, disabled=True)
        self.lbl_paginacion = ft.Text("Página 0 de 0")

        self.tabla_datos = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("i")),
                ft.DataColumn(label=ft.Text("a")),
                ft.DataColumn(label=ft.Text("v1")), # o X_i
                ft.DataColumn(label=ft.Text("c")),
                ft.DataColumn(label=ft.Text("modulo")),
                ft.DataColumn(label=ft.Text("normalizado")),
                ft.DataColumn(label=ft.Text("x_sig")),
                ft.DataColumn(label=ft.Text("ri")),
            ]
        )

        return ft.Column(
            controls=[
                # Updated Title
                self.bar,
                ft.Row([self.tittle], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.txt_a, self.txt_semilla, self.txt_C, self.txt_modulo, self.txt_n, self.btn_generar, self.btn_clear]),
                self.lbl_error,
                ft.Row([self.btn_prev, self.lbl_paginacion, self.btn_next], alignment=ft.MainAxisAlignment.CENTER),
                ft.ListView(
                    controls=[self.tabla_datos],
                    expand=True,
                    spacing=10,
                    padding=20,
                )
            ],
            expand=True
        )
    
    def limpiar_datos(self, e):
        self.tabla_datos.rows.clear()
        self.datos_completos = []
        self.lbl_paginacion.value = "Página 0 de 0"
        self.txt_a.value = ""
        self.txt_semilla.value = ""
        self.txt_C.value = ""
        self.txt_modulo.value = ""
        self.txt_n.value = ""
        self.update()

    def actualizar_tabla(self):
        self.tabla_datos.rows.clear()
        inicio = self.pagina_actual * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina
        segmento = self.datos_completos[inicio:fin]

        # Calculamos la cantidad de decimales basados en la longitud del string del módulo.
        # Lo leemos directamente del TextField para asegurarnos.
        try:
            modulo_str = self.txt_modulo.value.strip()
            num_decimales = len(modulo_str) if modulo_str else 4 # 4 por defecto si algo falla
        except:
            num_decimales = 4

        for fila in segmento:
            # Aplicamos el formato dinámico al valor ri
            ri_formateado = f"{float(fila['ri']):.{num_decimales}f}"

            self.tabla_datos.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(fila["i"]))),
                    ft.DataCell(ft.Text(str(fila["a"]))),
                    ft.DataCell(ft.Text(str(fila["v1"]))),
                    ft.DataCell(ft.Text(str(fila["c"]))),
                    ft.DataCell(ft.Text(str(fila["modulo"]))),
                    ft.DataCell(ft.Text(str(fila["normalizado"]))),
                    ft.DataCell(ft.Text(str(fila["x_sig"]))),
                    # Usamos el string formateado aquí
                    ft.DataCell(ft.Text(ri_formateado)), 
                ])
            )
            
        total_pags = (len(self.datos_completos)-1)//self.filas_por_pagina + 1 if self.datos_completos else 0
        self.lbl_paginacion.value = f"Página {self.pagina_actual + 1} de {total_pags}"
        self.btn_prev.disabled = self.pagina_actual <= 0
        self.btn_next.disabled = fin >= len(self.datos_completos)
        self.update()

    def procesar_datos(self, e): # Added 'e'
        self.lbl_error.value = '' # Fixed assignment to .value
        self.datos_completos = []
        self.tabla_datos.rows.clear()

        try:
            val_a = self.txt_a.value.strip()
            val_s = self.txt_semilla.value.strip()
            val_c = self.txt_C.value.strip()
            val_modulo = self.txt_modulo.value.strip()
            val_n = self.txt_n.value.strip()

            # --- 1. Validaciones para el Multiplicador (a) ---
            if not val_a:
                raise ValueError("El campo del multiplicador (a) no puede estar vacío.")
            try:
                val_a = int(val_a)
            except ValueError:
                raise ValueError("El multiplicador (a) debe ser un número entero (sin letras ni signos raros).")
            if val_a <= 0:
                raise ValueError("El multiplicador (a) no puede ser cero ni negativo.")

            # --- 2. Validaciones para la Semilla (X0) ---
            if not val_s:
                raise ValueError("El campo de la semilla (X0) no puede estar vacío.")
            try:
                val_s = int(val_s)
            except ValueError:
                raise ValueError("La semilla (X0) debe ser un número entero válido.")
            if val_s <= 0:
                raise ValueError("La semilla (X0) no puede ser cero ni negativa.")

            # --- 3. Validaciones para el Aditivo (c) ---
            if not val_c:
                raise ValueError("El campo del aditivo (c) no puede estar vacío.")
            try:
                val_c = int(val_c)
            except ValueError:
                raise ValueError("El aditivo (c) debe ser un número entero.")
            if val_c < 0:
                raise ValueError("El aditivo (c) no puede ser negativo (puede ser 0 o mayor).")

            # --- 4. Validaciones para el Módulo (m) ---
            if not val_modulo:
                raise ValueError("El campo del módulo (m) no puede estar vacío.")
            try:
                val_modulo = int(val_modulo)
            except ValueError:
                raise ValueError("El módulo (m) debe ser un número entero.")
            if val_modulo <= 0:
                raise ValueError("El módulo (m) no puede ser cero ni negativo.")

            # --- 5. Validaciones para Iteraciones (n) ---
            if not val_n:
                raise ValueError("El campo de iteraciones (n) no puede estar vacío.")
            try:
                val_n = int(val_n)
            except ValueError:
                raise ValueError("Las iteraciones (n) deben ser un número entero.")
            if val_n <= 0:
                raise ValueError("Debes ingresar por lo menos 1 iteración.")
                
            # --- 6. AUTO-CORRECCIÓN Matemáticas del LCG (Hull-Dobell) ---
            # Regla 1: El módulo (m) siempre debe ser mayor que a, X0 y c.
            # Regla 2: Para máxima eficiencia, 'c' y 'm' deben ser PRIMOS RELATIVOS (su Máximo Común Divisor debe ser 1).
            
            valor_maximo = max(val_a, val_s, val_c)
            necesita_ajuste = False
            
            # Verificamos si es muy pequeño O si NO son primos relativos
            if val_modulo <= valor_maximo or math.gcd(val_c, val_modulo) != 1:
                necesita_ajuste = True
                
                # Primero aseguramos que sea más grande que el máximo
                val_modulo = max(val_modulo, valor_maximo + 1)
                
                # Luego, iteramos hasta encontrar el primer número que sea primo relativo de c
                while math.gcd(val_c, val_modulo) != 1:
                    val_modulo += 1

            if necesita_ajuste:
                # ¡Magia! Actualizamos el campo de texto en la interfaz
                self.txt_modulo.value = str(val_modulo)
                
                # Le avisamos qué reglas aplicamos
                self.lbl_error.value = f"Aviso: Módulo ajustado a {val_modulo} para cumplir tamaño y ser primo relativo de 'c'."
                self.lbl_error.color = ft.Colors.ORANGE
            else:
                # Si todo está bien, limpiamos
                self.lbl_error.value = ""
                self.lbl_error.color = ft.Colors.ERROR
            # 7. Ejecución de la lógica (¡Ya son enteros, no necesitas el int() aquí!)
            generador = Metodo_lineal(
                a=val_a, 
                semilla=val_s, 
                c=val_c, 
                modulo=val_modulo, 
                n=val_n
            )
            self.datos_completos = generador.metodolineal()
            
            # Reset de página y renderizado
            self.pagina_actual = 0
            self.actualizar_tabla()

        except ValueError as ex:
            self.lbl_error.value = str(ex)
            self.update()
        except Exception as ex:
            self.lbl_error.value = f"Error inesperado: {type(ex).__name__}"
            self.update()

    def pagina_siguiente(self, e):
        self.pagina_actual += 1
        self.actualizar_tabla()

    def pagina_anterior(self, e):
        self.pagina_actual -= 1
        self.actualizar_tabla()
