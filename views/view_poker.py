import flet as ft
from core.independencia.poker import Prueba_Poker


class VistaPoker(ft.Container):
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
            title=ft.Text("Prueba de Póker", weight=ft.FontWeight.BOLD),
            center_title=True,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.volver),
        )

        self.lbl_info = ft.Text(
            value=f"Evaluando {len(self.lista_ri)} números generados.",
            size=16,
            color=ft.Colors.BLUE,
            weight=ft.FontWeight.W_500,
        )

        # Información sobre la normalización de decimales
        self.lbl_decimales = ft.Text(
            value="Decimales detectados: -",
            size=14,
            color=ft.Colors.ORANGE_900,
            weight=ft.FontWeight.BOLD,
        )

        self.txt_alpha = ft.TextField(
            label="Nivel de Significancia (α)", value="0.05", width=200
        )

        self.btn_calcular = ft.Button(
            "Ejecutar Prueba", on_click=self.calcular_prueba, icon=ft.Icons.CALCULATE
        )

        self.lbl_error = ft.Text(color=ft.Colors.ERROR, weight=ft.FontWeight.BOLD)

        # Tabla de resultados (Categoría de la mano, Oi, Ei, Chi Parcial)
        self.tabla_datos = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Mano (Categoría)")),
                ft.DataColumn(label=ft.Text("Oi (Observada)")),
                ft.DataColumn(label=ft.Text("Ei (Esperada)")),
                ft.DataColumn(label=ft.Text("Chi Parcial")),
            ],
            rows=[],
        )

        # Etiquetas para la conclusión
        self.lbl_chi_calc = ft.Text("Chi-Cuadrada Calculada: -", size=16)
        self.lbl_chi_crit = ft.Text("Valor Crítico (Tabla): -", size=16)
        self.lbl_grados = ft.Text("Grados de Libertad: -", size=16)
        self.lbl_conclusion = ft.Text(
            "CONCLUSIÓN: -", size=20, weight=ft.FontWeight.BOLD
        )

        self.panel_conclusion = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        self.lbl_chi_calc,
                        self.lbl_chi_crit,
                        self.lbl_grados,
                        ft.Divider(),
                        self.lbl_conclusion,
                    ]
                ),
                padding=20,
            ),
            width=500,
            margin=20,
        )

        return ft.Column(
            controls=[
                self.bar,
                ft.Row([self.lbl_info], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.lbl_decimales], alignment=ft.MainAxisAlignment.CENTER),
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
        self.lbl_decimales.value = "Decimales detectados: -"
        self.lbl_conclusion.value = "CONCLUSIÓN: -"
        self.lbl_conclusion.color = ft.Colors.BLACK
        self.update()

        try:
            # 1. Leer los datos más frescos de la memoria
            self.lista_ri = self.pagina.session.store.get("lista_ri_actual") or []
            if not self.lista_ri:
                raise ValueError("No hay números generados en memoria para evaluar.")

            # 2. Validar Alpha
            val_alpha = self.txt_alpha.value.strip()
            if not val_alpha:
                raise ValueError("El valor de alfa (α) es requerido.")

            alpha_float = float(val_alpha)
            if not (0 < alpha_float < 1):
                raise ValueError(
                    "El nivel de significancia (α) debe estar entre 0 y 1 (ej. 0.05)."
                )

            # 3. Instanciar la clase y calcular
            prueba = Prueba_Poker(numeros=self.lista_ri, alpha=alpha_float)
            resultados = prueba.calcular()

            # 4. Actualizar el indicador de decimales evaluados
            self.lbl_decimales.value = (
                f"Normalizado a: {resultados['decimales_evaluados']} decimales"
            )

            # 5. Llenar la tabla
            for fila in resultados["tabla"]:
                self.tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(fila["categoria"])),
                            ft.DataCell(ft.Text(str(fila["oi"]))),
                            ft.DataCell(ft.Text(fila["ei"])),
                            ft.DataCell(ft.Text(fila["chi_parcial"])),
                        ]
                    )
                )

            # 6. Actualizar el panel de conclusión
            self.lbl_chi_calc.value = (
                f"Chi-Cuadrada Calculada: {resultados['estadistico_chi2']:.4f}"
            )
            self.lbl_chi_crit.value = (
                f"Valor Crítico (Tabla): {resultados['valor_critico']:.4f}"
            )
            self.lbl_grados.value = (
                f"Grados de Libertad: {resultados['grados_libertad']}"
            )

            if resultados["aprobado"]:
                self.lbl_conclusion.value = (
                    "CONCLUSIÓN: SE ACEPTA H0 (Son Independientes)"
                )
                self.lbl_conclusion.color = ft.Colors.GREEN
            else:
                self.lbl_conclusion.value = (
                    "CONCLUSIÓN: SE RECHAZA H0 (No son Independientes)"
                )
                self.lbl_conclusion.color = ft.Colors.RED

        except ValueError as ex:
            self.lbl_error.value = str(ex)
        except Exception as ex:
            self.lbl_error.value = f"Error al calcular: {str(ex)}"

        self.update()
