import flet as ft
from views.view_metodo_lineal import VistaMetodoLineal

def main(page: ft.Page):
    page.title = "Prueba Unitaria - Interfaz"
    page.theme_mode = ft.ThemeMode.DARK 
    page.padding = 30
    vista = VistaMetodoLineal()
    page.add(vista)

if __name__ == "__main__":
    try:
        ft.run(main)
    except Exception:
        pass 