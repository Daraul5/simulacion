import flet as ft
from core.aleatoriedad.ks import KS_metodo


class VistaKS(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.pagina = page
        self.expand = True
        self.padding = 20

        # 1. Recuperamos los números sin importar de qué generador vienen
        self.lista_ri = self.pagina.session.store.get("lista_ri_actual") or []

        self.content = self.build_ui()

    def build_ui(self):
        self.bar = ft.AppBar(
            title=ft.Text("Prueba de Kolmogorov-Smirnov", weight=ft.FontWeight.BOLD),
            center_title=True,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.volver),
        )
        self.lbl_info = ft.Text(
            value=f"Evaluando {len(self.lista_ri)} números generados (Maximo 40 permitidos).",
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

        self.tabla_datos = ft.DataTable(
            [
                ft.DataColumn(label=ft.Text("Indice")),
                ft.DataColumn(label=ft.Text("Valor Ri")),
                ft.DataColumn(label=ft.Text("DMAS")),
                ft.DataColumn(label=ft.Text("DMENOS")),
            ],
            rows=[],
        )
        self.lbl_ks_calc = ft.Text("Estadístico KS Calculado: -", size=16)
        self.lbl_ks_crit = ft.Text("Valor Crítico (Tabla): -", size=16)
        self.lbl_conclusion = ft.Text(
            "CONCLUSIÓN: -", size=20, weight=ft.FontWeight.BOLD
        )

        self.panel_conclusion = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        self.lbl_ks_calc,
                        self.lbl_ks_crit,
                        ft.Divider(),
                        self.lbl_conclusion,
                    ],
                ),
                padding=20,
            ),
            width=500,
        )
        return ft.Column(
            controls=[
                self.bar,
                ft.Row([self.lbl_info], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [self.txt_alpha, self.btn_calcular],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.lbl_error,
                ft.Row([self.panel_conclusion], alignment=ft.MainAxisAlignment.CENTER),
                ft.ListView(
                    controls=[self.tabla_datos],
                    expand=True,
                    padding=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    async def volver(self, e):
        await self.pagina.push_route("/confirmaciones")

    def calcular_prueba(self, e):
        self.lbl_error.value = ""
        self.tabla_datos.rows.clear()
        self.lbl_conclusion.value = "CONCLUSIÓN: -"
        self.lbl_conclusion.color = ft.Colors.BLACK
        self.update()
        try:
            self.lista_ri = self.pagina.session.store.get("lista_ri_actual") or []
            if not self.lista_ri:
                raise ValueError("No hay números generados en memoria para evaluar.")

            val_alpha = self.txt_alpha.value.strip()
            if not val_alpha:
                raise ValueError("El valor de alfa (α) es requerido.")

            alpha_float = float(val_alpha)
            if not (0 < alpha_float < 1):
                raise ValueError(
                    "El nivel de significancia (α) debe estar entre 0 y 1 (ej. 0.05)."
                )
            # Ejecutamos la prueba KS
            prueba_ks = KS_metodo(self.lista_ri, alpha_float)
            resultado = prueba_ks.calcular()

            for fila in resultado["tabla"]:
                self.tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila["i"]))),
                            ft.DataCell(ft.Text(f"{fila['ri']:.6f}")),
                            ft.DataCell(ft.Text(f"{fila['d_mas']:.6f}")),
                            ft.DataCell(ft.Text(f"{fila['d_menos']:.6f}")),
                        ]
                    )
                )
            self.lbl_ks_calc.value = (
                f"Estadístico KS Calculado: {resultado['estadistico_ks']:.6f}"
            )
            self.lbl_ks_crit.value = (
                f"Valor Crítico (Tabla): {resultado['valor_critico']:.6f}"
            )
            if resultado["aprobado"]:
                self.lbl_conclusion.value = (
                    "CONCLUSIÓN: Se acepta la hipótesis de uniformidad."
                )
                self.lbl_conclusion.color = ft.Colors.GREEN
            else:
                self.lbl_conclusion.value = (
                    "CONCLUSIÓN: Se rechaza la hipótesis de uniformidad."
                )
                self.lbl_conclusion.color = ft.Colors.RED

        except ValueError as ex:
            self.lbl_error.value = str(ex)
        except Exception as ex:
            self.lbl_error.value = f"Error inesperado: {str(ex)}"

        self.update()
