import flet as ft
from core.metodolineal import Metodo_lineal

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
        self.txt_a = ft.TextField(label="Multiplicador (a)", width=200)
        self.txt_semilla = ft.TextField(label="Semilla (X0)", width=200)
        self.txt_C = ft.TextField(label="Aditivo (c)", width=200)
        self.txt_modulo = ft.TextField(label="Modulo (m)", width=200)
        self.txt_n = ft.TextField(label="Iteraciones (n)")
        
        # NOTE: Event functions need an 'e' parameter
        self.btn_generar = ft.ElevatedButton("Generar", on_click=self.procesar_datos)
        self.lbl_error = ft.Text("", color=ft.Colors.ERROR, size=14, weight=ft.FontWeight.BOLD)

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
                ft.Text(value="Generador: Método Lineal Congruencial", size=32, weight=ft.FontWeight.BOLD),
                ft.Row([self.txt_a, self.txt_semilla, self.txt_C, self.txt_modulo, self.txt_n, self.btn_generar]),
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

    def actualizar_tabla(self):
        self.tabla_datos.rows.clear()
        inicio = self.pagina_actual * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina
        segmento = self.datos_completos[inicio:fin]

        for fila in segmento:
            self.tabla_datos.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(fila["i"]))),
                    ft.DataCell(ft.Text(str(fila["a"]))),
                    ft.DataCell(ft.Text(str(fila["vi"]))),
                    ft.DataCell(ft.Text(str(fila["c"]))),
                    ft.DataCell(ft.Text(str(fila["modulo"]))),
                    ft.DataCell(ft.Text(str(fila["normalizado"]))),
                    ft.DataCell(ft.Text(str(fila["x_sig"]))),
                    ft.DataCell(ft.Text(str(fila["ri"]))),
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

            # 1. Validaciones para el multiplicador
            if not val_a or not val_a.isdigit() or int(val_a) <= 0:
                raise ValueError("El multiplicador debe ser un número entero positivo.")
            
            # 2. Validaciones para Semilla
            if not val_s or not val_s.isdigit() or int(val_s) <= 0:
                raise ValueError("La semilla debe ser un número entero positivo.")
            
            # (Opcional) Removida la validación de dígitos pares, ya que no aplica al método lineal
            
            # 3. Validaciones para C y Modulo (Recomendado agregarlas)
            if not val_c or not val_c.isdigit() or int(val_c) < 0:
                 raise ValueError("El aditivo (c) debe ser un número entero positivo o cero.")
            
            if not val_modulo or not val_modulo.isdigit() or int(val_modulo) <= 0:
                 raise ValueError("El módulo debe ser un número entero positivo.")

            # 4. Validaciones para n (Iteraciones)
            if not val_n or not val_n.isdigit() or int(val_n) <= 0:
                raise ValueError("El número de iteraciones debe ser un entero mayor a 0.")

            # 5. Ejecución de la lógica
            # Asegúrate de pasar enteros si tu backend así lo requiere
            generador = Metodo_lineal(
                a=int(val_a), 
                semilla=int(val_s), 
                c=int(val_c), 
                modulo=int(val_modulo), 
                n=int(val_n)
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
