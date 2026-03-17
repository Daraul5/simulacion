import flet as ft
from views.view_producto_medio import VistaProductosMedios

def main(page: ft.Page):
    page.title = "Prueba Unitaria - Interfaz"
    page.theme_mode = ft.ThemeMode.DARK # Un entorno oscuro cómodo
    page.padding = 30

    # Instanciamos nuestra vista encapsulada y la agregamos a la página
    vista = VistaProductosMedios()
    page.add(vista)

if __name__ == "__main__":
    try:
        ft.run(main)
    except Exception:
        pass # Ignora errores al cerrar la ventana