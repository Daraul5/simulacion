import flet as ft


class VistaConfirmaciones(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.pagina = page
        self.expand = True
        self.padding = 40

        # Recuperamos la lista de la sesión (si no hay, usamos una lista vacía)
        self.lista_ri = self.pagina.session.store.get("lista_ri_actual") or []

        self.content = self.build_ui()

    def build_ui(self):
        # Encabezado con botón de volver
        self.bar = ft.AppBar(
            title=ft.Text("Pruebas de Aleatoriedad", weight=ft.FontWeight.BOLD),
            center_title=True,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.volver),
        )

        self.tittle = ft.Text(
            "Seleccione la prueba a realizar", size=28, weight=ft.FontWeight.BOLD
        )

        self.lbl_info = ft.Text(
            value=f"Se evaluarán {len(self.lista_ri)} números generados.",
            color=ft.Colors.BLUE,
            size=16,
        )

        # Botones de las pruebas
        return ft.Column(
            controls=[
                self.bar,
                self.tittle,
                self.lbl_info,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Button(
                    content=ft.Text("Prueba de Chi-Cuadrada"),
                    icon=ft.Icons.FACT_CHECK,
                    width=300,
                    height=50,
                    on_click=self.ir_a_chi2,
                ),
                ft.Button(
                    content=ft.Text("Prueba Kolmogorov-Smirnov"),
                    icon=ft.Icons.FACT_CHECK,
                    width=300,
                    height=50,
                    on_click=self.ir_a_ks,
                ),
                ft.Button(
                    content=ft.Text("Prueba Arriba y Abajo"),
                    icon=ft.Icons.FACT_CHECK,
                    width=300,
                    height=50,
                    on_click=self.ir_a_arriba_abajo,
                ),
                ft.Button(
                    content=ft.Text("Prueba Arriba y Abajo de la Media"),
                    icon=ft.Icons.FACT_CHECK,
                    width=300,
                    height=50,
                    on_click=self.ir_a_arriba_abajo_media,
                ),
                ft.Button(
                    content=ft.Text("Prueba de Póker"),
                    icon=ft.Icons.FACT_CHECK,
                    width=300,
                    height=50,
                    on_click=self.ir_a_poker,
                ),
                ft.Button(
                    content=ft.Text("Prueba de Huecos"),
                    icon=ft.Icons.FACT_CHECK,
                    width=300,
                    height=50,
                    on_click=self.ir_a_huecos,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    async def volver(self, e):
        # Recuperamos la ruta de donde veníamos para regresar al generador correcto
        ruta_origen = self.pagina.session.store.get("ruta_origen") or "/"

        # Solo limpiamos la memoria al retroceder, porque ya no vamos a evaluar nada
        self.pagina.session.store.remove("lista_ri_actual")
        self.pagina.session.store.remove("ruta_origen")

        # Navegamos de vuelta al generador
        await self.pagina.push_route(ruta_origen)

    # Funciones asíncronas de navegación para cada prueba
    async def ir_a_chi2(self, e):
        await self.pagina.push_route("/prueba_chi2")

    async def ir_a_ks(self, e):
        await self.pagina.push_route("/prueba_ks")

    async def ir_a_arriba_abajo(self, e):
        await self.pagina.push_route("/prueba_arriba_abajo")

    async def ir_a_arriba_abajo_media(self, e):
        await self.pagina.push_route("/prueba_arriba_abajo_media")

    async def ir_a_poker(self, e):
        await self.pagina.push_route("/prueba_poker")

    async def ir_a_huecos(self, e):
        await self.pagina.push_route("/prueba_huecos")
