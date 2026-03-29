import flet as ft
from core.productosmedios import Producto_medio

class VistaProductosMedios(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = 20
        self.datos_completos = []
        self.pagina_actual = 0
        self.filas_por_pagina = 100
        self.content = self.build_ui()

    def build_ui(self):
        self.txt_semilla1 = ft.TextField(label="Semilla 1", width=200)
        self.txt_semilla2 = ft.TextField(label="Semilla 2", width=200)
        self.txt_n = ft.TextField(label="Iteraciones (n)", width=150)
        self.btn_generar = ft.Button("Generar", on_click=self.procesar_datos)
        self.btn_clear = ft.Button("Limpiar", on_click=self.limpiar_datos)
        self.lbl_error = ft.Text(color=ft.Colors.ERROR, size=14, weight=ft.FontWeight.BOLD)
        
        self.btn_prev = ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.pagina_anterior, disabled=True)
        self.btn_next = ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=self.pagina_siguiente, disabled=True)
        self.lbl_paginacion = ft.Text("Página 0 de 0")
        
        self.tabla_datos = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("i")),
                ft.DataColumn(label=ft.Text("X1-1")),
                ft.DataColumn(label=ft.Text("X2")),
                ft.DataColumn(label=ft.Text("Cuadrado")),
                ft.DataColumn(label=ft.Text("Centro")),
                ft.DataColumn(label=ft.Text("Ri")),
            ],
            rows=[]
        )

        return ft.Column(
            controls=[
                ft.Text(value="Generador: Productos Medios", size=32, weight=ft.FontWeight.BOLD),
                ft.Row([self.txt_semilla1, self.txt_semilla2, self.txt_n, self.btn_generar]),
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
                    ft.DataCell(ft.Text(fila["v1"])),
                    ft.DataCell(ft.Text(fila["v2"])),
                    ft.DataCell(ft.Text(fila["producto"])),
                    ft.DataCell(ft.Text(fila["x_sig"])),
                    ft.DataCell(ft.Text(f"{fila['ri']:.4f}")),
                ])
            )
        
        total_pags = (len(self.datos_completos) - 1) // self.filas_por_pagina + 1 if self.datos_completos else 0
        self.lbl_paginacion.value = f"Página {self.pagina_actual + 1} de {total_pags}"
        self.btn_prev.disabled = self.pagina_actual <= 0
        self.btn_next.disabled = fin >= len(self.datos_completos)
        self.update()
        
    def limpiar_datos(self, e):
        self.tabla_datos.rows.clear()
        self.datos_completos = []
        self.lbl_paginacion.value = "Página 0 de 0"
        self.btn_prev.disabled = True
        self.btn_next.disabled = True
        self.update()

    def procesar_datos(self, e):
        self.lbl_error.value = ""
        
        self.tabla_datos.rows.clear()
        self.update() 
        
        try:
            val_s1 = self.txt_semilla1.value.strip()
            val_s2 = self.txt_semilla2.value.strip()
            val_n = self.txt_n.value.strip()

            # 1. Validaciones Semilla 1
            if not val_s1:
                raise ValueError("La semilla 1 es obligatoria.")
            if not val_s1.isdigit():
                raise ValueError(f"Semilla 1 '{val_s1}' no válida. Use solo números.")
            if len(val_s1) % 2 != 0:
                raise ValueError(f"Semilla 1 tiene {len(val_s1)} dígitos. Debe ser par.")

            # 2. Validaciones Semilla 2
            if not val_s2:
                raise ValueError("La semilla 2 es obligatoria.")
            if not val_s2.isdigit():
                raise ValueError(f"Semilla 2 '{val_s2}' no válida. Use solo números.")
            if len(val_s2) % 2 != 0:
                raise ValueError(f"Semilla 2 tiene {len(val_s2)} dígitos. Debe ser par.")
            
            # Validación de longitud igual (opcional, dependiendo de tu core)
            if len(val_s1) != len(val_s2):
                raise ValueError("Ambas semillas deben tener la misma cantidad de dígitos.")

            # 3. Validación Iteraciones
            if not val_n:
                raise ValueError("El número de iteraciones (n) es obligatorio.")
            if not val_n.isdigit() or int(val_n) <= 0:
                raise ValueError("Las iteraciones deben ser un número entero mayor a 0.")

            # Ejecución
            generador = Producto_medio(semilla1=val_s1, semilla2=val_s2, n=int(val_n))
            self.datos_completos = generador.productosmedios()
            
            self.pagina_actual = 0
            self.actualizar_tabla()

        except ValueError as ex:
            self.lbl_error.value = str(ex)
            self.update()
        except Exception as ex:
            self.lbl_error.value = f"Error crítico: {type(ex).__name__}"
            self.update()

    def pagina_siguiente(self, e):
        self.pagina_actual += 1
        self.actualizar_tabla()

    def pagina_anterior(self, e):
        self.pagina_actual -= 1
        self.actualizar_tabla()

