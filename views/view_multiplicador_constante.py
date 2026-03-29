import flet as ft
from core.multplicadorconstante import Multiplicador_constante

class VistaMultiplicadorConstante(ft.Container):
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
        self.txt_n = ft.TextField(label="Iteraciones (n)", width=200)
        
        self.btn_generar = ft.Button("Generar", on_click=self.procesar_datos)
        self.btn_clear = ft.Button("Limpiar", on_click=self.limpiar_datos)
        self.lbl_error = ft.Text(color=ft.Colors.ERROR, weight=ft.FontWeight.BOLD)

        self.btn_prev = ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.pagina_anterior, disabled=True)
        self.btn_next = ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=self.pagina_siguiente, disabled=True)
        self.lbl_paginacion = ft.Text("Página 0 de 0")

        self.tabla_datos = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("i")),
                ft.DataColumn(label=ft.Text("a")),
                ft.DataColumn(label=ft.Text("Xn")),
                ft.DataColumn(label=ft.Text("Producto (Norm)")),
                ft.DataColumn(label=ft.Text("Xn+1")),
                ft.DataColumn(label=ft.Text("Ri")),
            ],
            rows=[]
        )

        return ft.Column(
            controls=[
                ft.Text(value="Generador: Multiplicador Constante", size=32, weight=ft.FontWeight.BOLD),
                ft.Row([self.txt_a, self.txt_semilla, self.txt_n, self.btn_generar, self.btn_clear]),
                self.lbl_error,
                ft.Row([self.btn_prev, self.lbl_paginacion, self.btn_next], alignment=ft.MainAxisAlignment.CENTER),
                ft.ListView(
                    controls=[self.tabla_datos],
                    expand=True,
                    spacing=10,
                    padding=20,
                )
            ],)
    
    def actualizar_tabla(self):
        self.tabla_datos.rows.clear()
        inicio = self.pagina_actual * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina
        segmento = self.datos_completos[inicio:fin]

        for fila in segmento:
            self.tabla_datos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(fila["i"]))),
                        ft.DataCell(ft.Text(str(fila["a"]))),
                        ft.DataCell(ft.Text(str(fila["xn"]))),
                        ft.DataCell(ft.Text(str(fila["producto"]))),
                        ft.DataCell(ft.Text(str(fila["x_sig"]))),
                        ft.DataCell(ft.Text(str(fila["ri"]))),
                    ]
                )
            )
        total_paginas = (len(self.datos_completos) - 1) // self.filas_por_pagina + 1 if self.datos_completos else 0
        self.lbl_paginacion.value = f"Página {self.pagina_actual + 1} de {total_paginas}"
        self.btn_prev.disabled = self.pagina_actual <= 0
        self.btn_next.disabled = fin >= len(self.datos_completos)
        self.update()

    def limpiar_datos(self, e):
        self.txt_a.value = ""
        self.txt_semilla.value = ""
        self.txt_n.value = ""
        self.lbl_error.value = ""
        self.tabla_datos.rows.clear()
        self.datos_completos = []
        self.pagina_actual = 0
        self.update()

    def procesar_datos(self, e):
        self.lbl_error.value = ""
        self.tabla_datos.rows.clear()
        self.update()
        try:
            a = self.txt_a.value.strip()
            semilla = self.txt_semilla.value.strip()
            n = self.txt_n.value.strip()

            if not a:
                raise ValueError("El multiplicador (a) es requerido")
            if not a.isdigit():
                raise ValueError(f"El multiplicador {a} debe ser un número entero")
            if int(a) < 0:
                raise ValueError("El multiplicador (a) debe ser positivo")

            if not semilla:
                raise ValueError("La semilla (X0) es requerida")
            if not semilla.isdigit():
                raise ValueError(f"La semilla {semilla} debe ser un número entero")
            if len(semilla) % 2 != 0:
                raise ValueError("La semilla debe tener un número par de dígitos")
            if int(semilla) < 0:
                raise ValueError("La semilla (X0) debe ser positiva")

            if not n:
                raise ValueError("El número de iteraciones (n) es requerido")
            if not n.isdigit():
                raise ValueError(f"El número de iteraciones {n} debe ser un número entero")
            if int(n) < 0:
                raise ValueError("El número de iteraciones (n) debe ser positivo")


            generador = Multiplicador_constante(a=int(a), semilla=int(semilla), n=int(n))
            self.datos_completos = generador.multiplicadorconstante()
            self.pagina_actual = 0
            self.actualizar_tabla()
            
        except ValueError as ve:
            self.lbl_error.value = str(ve)
        except Exception as ex:
            self.lbl_error.value = f"Error inesperado: {str(ex)}"
        self.update()
        

    def pagina_siguiente(self, e):
        self.pagina_actual += 1
        self.actualizar_tabla()

    def pagina_anterior(self, e):
        self.pagina_actual -= 1
        self.actualizar_tabla()
