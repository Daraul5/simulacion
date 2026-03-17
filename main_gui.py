import flet as ft
from views.view_cuadrado_medio import VistaCuadradosMedios

def main(page: ft.Page):
    page.title = "Prueba Unitaria - Interfaz"
    page.theme_mode = ft.ThemeMode.DARK # Un entorno oscuro cómodo
    page.padding = 30

    # Instanciamos nuestra vista encapsulada y la agregamos a la página
    vista = VistaCuadradosMedios()
    page.add(vista)

if __name__ == "__main__":
    ft.app(target=main)