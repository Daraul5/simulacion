import flet as ft
from core.cuadradosmedios import Cuadrado_medio

class VistaCuadradosMedios(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = 20
        self.datos_completos = []
        self.pagina_actual = 0
        self.filas_por_pagina = 100
        self.content = self.build_ui()

    def build_ui(self):
        self.bar = ft.AppBar(title=ft.Text("Generador de Números Aleatorios - Cuadrados Medios"), center_title=True)
        self.tittle = ft.Text("Generador de Números Aleatorios - Cuadrados Medios", size=24, weight=ft.FontWeight.BOLD)
        self.txt_semilla = ft.TextField(label="Semilla", width=200)
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
                ft.DataColumn(label=ft.Text("Xi-1")),
                ft.DataColumn(label=ft.Text("Cuadrado")),
                ft.DataColumn(label=ft.Text("Centro")),
                ft.DataColumn(label=ft.Text("Ri")),
            ],
            rows=[]
        )
        return ft.Column(
            controls=[
                self.bar,
                ft.Row([self.tittle], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.txt_semilla, self.txt_n, self.btn_generar]),
                self.lbl_error,
                ft.Row([self.btn_prev, self.lbl_paginacion, self.btn_next], alignment=ft.MainAxisAlignment.CENTER),
                ft.ListView(
                    controls=[self.tabla_datos], 
                    expand=True, 
                    padding=20)
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
                    ft.DataCell(ft.Text(fila["cuadrado"])),
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
        self.txt_semilla.value = ""
        self.txt_n.value = ""
        self.lbl_error.value = ""
        self.datos_completos = []
        self.pagina_actual = 0
        self.tabla_datos.rows.clear()
        self.btn_prev.disabled = True
        self.btn_next.disabled = True
        self.lbl_paginacion.value = "Página 0 de 0"
        self.update()


    def procesar_datos(self, e):
        self.lbl_error.value = ""
        self.datos_completos = []
        self.tabla_datos.rows.clear()
        
        try:
            val_s = self.txt_semilla.value.strip()
            val_n = self.txt_n.value.strip()

            # 1. Validaciones específicas para Semilla
            if not val_s:
                raise ValueError("La semilla es obligatoria.")
            if not val_s.isdigit():
                raise ValueError(f"La semilla '{val_s}' no es válida. Debe contener solo números.")
            if len(val_s) % 2 != 0:
                raise ValueError(f"La semilla tiene {len(val_s)} dígitos. Debe tener un número par (ej. 4, 6 dígitos).")

            # 2. Validaciones específicas para n (Iteraciones)
            if not val_n:
                raise ValueError("El número de iteraciones (n) es obligatorio.")
            if not val_n.isdigit():
                raise ValueError(f"El valor '{val_n}' no es válido. Las iteraciones deben ser un número entero.")
            if int(val_n) <= 0:
                raise ValueError("El número de iteraciones debe ser mayor a 0.")

            # 3. Ejecución de la lógica
            generador = Cuadrado_medio(semilla=val_s, n=int(val_n))
            self.datos_completos = generador.cuadradosmedios()
            
            # Reset de página y renderizado
            self.pagina_actual = 0
            self.actualizar_tabla()

        except ValueError as ex:
            # Captura tanto tus raise manuales como los raise de la clase Cuadrado_medio
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

