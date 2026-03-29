import flet as ft
from core.multplicadorconstante import Multiplicador_constante

class VistaMultiplicadorCOnstante(ft.Container):
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
        
        self.btn_generar = ft.Button("Generar")
        self.btn_clear = ft.Button("Limpiar")
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
        pass
        

    def pagina_anterior(self):
        pass
    def pagina_siguiente(self):
        pass