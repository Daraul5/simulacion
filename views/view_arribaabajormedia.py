import flet as ft
from core.uniformidad.arribayabajomedia import Arriba_Abajo_Media


class VistaArribaAbajoMedia(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.pagina = page
        self.expand = True
        self.padding = 20

        # Recuperamos la lista de la sesión
        self.lista_ri = self.pagina.session.store.get("lista_ri_actual") or []

        self.content = self.build_ui()

    def build_ui(self):
        self.bar = ft.AppBar(
            title=ft.Text(
                "Prueba de Arriba y Abajo de la Media", weight=ft.FontWeight.BOLD
            ),
            center_title=True,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.volver),
        )

        self.lbl_info = ft.Text(
            value=f"Evaluando {len(self.lista_ri)} números generados.",
            size=16,
            color=ft.Colors.BLUE,
            weight=ft.FontWeight.W_500,
        )

        self.txt_alpha = ft.TextField(
            label="Nivel de Significancia (α)", value="0.05", width=200
        )

        self.btn_calcular = ft.Button(
            "Ejecutar Prueba", on_click=self.calcular_prueba, icon=ft.Icons.CALCULATE
        )

        self.lbl_error = ft.Text(color=ft.Colors.ERROR, weight=ft.FontWeight.BOLD)

        # Campo para mostrar la secuencia de bits (1s y 0s respecto a la media)
        self.txt_secuencia = ft.TextField(
            label="Secuencia de Signos (1: ≥ Media, 0: < Media)",
            read_only=True,
            multiline=True,
            max_lines=3,
            text_size=12,
        )

        # Tabla para los estadísticos
        self.tabla_estadisticos = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Parámetro")),
                ft.DataColumn(label=ft.Text("Valor")),
            ],
            rows=[],
        )

        self.lbl_conclusion = ft.Text(
            "CONCLUSIÓN: -", size=20, weight=ft.FontWeight.BOLD
        )

        self.panel_conclusion = ft.Card(
            content=ft.Container(
                content=ft.Column([self.lbl_conclusion]),
                padding=20,
            ),
            margin=20,
        )

        return ft.Column(
            [
                self.bar,
                ft.Row([self.lbl_info], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [self.txt_alpha, self.btn_calcular],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.lbl_error,
                self.txt_secuencia,
                ft.Row(
                    [self.tabla_estadisticos], alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row([self.panel_conclusion], alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    async def volver(self, e):
        await self.pagina.push_route("/confirmaciones")

    def calcular_prueba(self, e):
        # Limpiar interfaz antes de calcular
        self.lbl_error.value = ""
        self.tabla_estadisticos.rows.clear()
        self.txt_secuencia.value = ""
        self.lbl_conclusion.value = "CONCLUSIÓN: -"
        self.lbl_conclusion.color = ft.Colors.BLACK
        self.update()

        try:
            # 1. Leer los datos más frescos de la memoria
            self.lista_ri = self.pagina.session.store.get("lista_ri_actual") or []
            if not self.lista_ri:
                raise ValueError("No hay números en memoria para evaluar.")

            # 2. Validar Alpha
            val_alpha = self.txt_alpha.value.strip()
            if not val_alpha:
                raise ValueError("El nivel de significancia (α) es requerido.")
            alpha_float = float(val_alpha)
            if not (0 < alpha_float < 1):
                raise ValueError(
                    "El nivel de significancia (α) debe estar entre 0 y 1."
                )

            # 3. Ejecutar Lógica
            prueba = Arriba_Abajo_Media(self.lista_ri, alpha_float)
            res = prueba.calcular()

            # 4. Mostrar Secuencia
            self.txt_secuencia.value = res["secuencia_str"]

            # 5. Llenar tabla de estadísticos
            for fila in res["tabla"]:
                self.tabla_estadisticos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(fila["parametro"])),
                            ft.DataCell(ft.Text(fila["valor"])),
                        ]
                    )
                )

            # 6. Mostrar Conclusión
            if res["aprobado"]:
                self.lbl_conclusion.value = (
                    "CONCLUSIÓN: SE ACEPTA H0 (Son Independientes)"
                )
                self.lbl_conclusion.color = ft.Colors.GREEN
            else:
                self.lbl_conclusion.value = (
                    "CONCLUSIÓN: SE RECHAZA H0 (No son Independientes)"
                )
                self.lbl_conclusion.color = ft.Colors.RED

        except ValueError as ve:
            self.lbl_error.value = str(ve)
        except Exception as ex:
            self.lbl_error.value = f"Error inesperado: {str(ex)}"

        self.update()
