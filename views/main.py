import flet as ft


class VistaMenu(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.pagina = page  # Guardamos la referencia a la página principal
        self.expand = True
        self.padding = 40
        self.content = self.build_ui()

    def build_ui(self):
        return ft.Column(
            controls=[
                ft.Text("Menú de Generadores", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Selecciona el método de simulación que deseas utilizar:", size=16
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),  # Espacio en blanco
                # Botones de navegación
                ft.Button(
                    content=ft.Text("Generador: Productos Medios"),
                    icon=ft.Icons.CALCULATE,
                    width=300,
                    height=50,
                    on_click=self.ir_a_productos_medios,
                ),
                ft.Button(
                    content=ft.Text("Generador: Cuadrados Medios"),
                    icon=ft.Icons.CALCULATE,
                    width=300,
                    height=50,
                    on_click=self.ir_a_cuadrados_medios,
                ),
                ft.Button(
                    content=ft.Text("Generador: Multiplicador Constante"),
                    icon=ft.Icons.CALCULATE,
                    width=300,
                    height=50,
                    on_click=self.ir_a_multiplicador_constante,
                ),
                ft.Button(
                    content=ft.Text("Generador: Algoritmo lineal"),
                    icon=ft.Icons.CALCULATE,
                    width=300,
                    height=50,
                    on_click=self.ir_a_algoritmo_lineal,
                ),
                # Aquí puedes ir agregando más botones en el futuro
                # ft.ElevatedButton("Generador: Cuadrados Medios", ...)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar los elementos
        )

    # Funciones de navegación asíncronas
    async def ir_a_productos_medios(self, e):
        await self.pagina.push_route("/productos_medios")

    async def ir_a_cuadrados_medios(self, e):
        await self.pagina.push_route("/cuadrados_medios")

    async def ir_a_multiplicador_constante(self, e):
        await self.pagina.push_route("/multiplicador_constante")

    async def ir_a_algoritmo_lineal(self, e):
        await self.pagina.push_route("/algoritmo_lineal")
