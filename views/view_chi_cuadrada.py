import flet as ft
from core.aleatoriedad.chicuadrada import Prueba_chi2


class VistaChiCuadrada(ft.Container):
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
            title=ft.Text("Prueba de Chi-Cuadrada", weight=ft.FontWeight.BOLD),
            center_title=True,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.volver),
        )

        self.lbl_info = ft.Text(
            value=f"Evaluando {len(self.lista_ri)} números generados.",
            size=16,
            color=ft.Colors.BLUE,
            weight=ft.FontWeight.W_500,
        )

        # Campo para el nivel de significancia (con valor por defecto común)
        self.txt_alpha = ft.TextField(
            label="Nivel de Significancia (α)", value="0.05", width=200
        )
        self.btn_calcular = ft.Button(
            "Ejecutar Prueba", on_click=self.calcular_prueba, icon=ft.Icons.CALCULATE
        )
        self.lbl_error = ft.Text(color=ft.Colors.ERROR, weight=ft.FontWeight.BOLD)

        # Tabla de resultados
        self.tabla_datos = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Intervalo")),
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

        # Panel de conclusión visual
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
        # Regresamos al menú de selección de pruebas para poder aplicar otra prueba
        # a la misma lista de números sin tener que volver a generarlos.
        await self.pagina.push_route("/confirmaciones")

    def calcular_prueba(self, e):
        # Limpiar resultados anteriores
        self.lbl_error.value = ""
        self.tabla_datos.rows.clear()
        self.lbl_conclusion.value = "CONCLUSIÓN: -"
        self.lbl_conclusion.color = ft.Colors.BLACK
        self.update()

        try:
            # 1. Validaciones iniciales
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

            # 2. Instanciar nuestra clase refactorizada
            prueba = Prueba_chi2(numeros=self.lista_ri, alpha=alpha_float)
            resultados = prueba.calcular()

            # 3. Llenar la tabla con el diccionario devuelto
            for fila in resultados["tabla"]:
                self.tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(fila["intervalo"])),
                            ft.DataCell(ft.Text(str(fila["oi"]))),
                            ft.DataCell(ft.Text(f"{fila['ei']:.4f}")),
                            ft.DataCell(ft.Text(f"{fila['chi_parcial']:.4f}")),
                        ]
                    )
                )

            # 4. Actualizar el panel de conclusión
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
                    "CONCLUSIÓN: SE ACEPTA H0 (Distribución Uniforme)"
                )
                self.lbl_conclusion.color = ft.Colors.GREEN
            else:
                self.lbl_conclusion.value = (
                    "CONCLUSIÓN: SE RECHAZA H0 (No son uniformes)"
                )
                self.lbl_conclusion.color = ft.Colors.RED

        except ValueError as ex:
            self.lbl_error.value = str(ex)
        except Exception as ex:
            self.lbl_error.value = f"Error al calcular: {str(ex)}"

        self.update()
