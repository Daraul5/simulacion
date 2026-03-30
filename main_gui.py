import flet as ft
from views.view_cuadrado_medio import VistaCuadradosMedios
from views.view_producto_medio import VistaProductosMedios
from views.view_metodo_lineal import VistaMetodoLineal
from views.view_multiplicador_constante import VistaMultiplicadorConstante
from views.main import VistaMenu 

def main(page: ft.Page):
    page.title = "Mis Generadores"

    # Manejador de rutas
    def route_change(e=None):
        page.views.clear()
        
        # 1. Instanciamos la clase ANTES de crear el ft.View
        mi_vista_menu = VistaMenu(page) 
        
        # Siempre apilamos el menú principal abajo
        page.views.append(
            ft.View(
                route="/",
                controls=[mi_vista_menu] # 2. Pasamos la instancia a los controles
            )
        )

        # Si la ruta coincide, apilamos la vista de productos
        if page.route == "/productos_medios":
            mi_vista_productos = VistaProductosMedios()
            page.views.append(
                ft.View(
                    route="/productos_medios",
                    controls=[mi_vista_productos]
                )
            )
        if page.route == "/cuadrados_medios":
            mi_vista_cuadrados = VistaCuadradosMedios()
            page.views.append(
                ft.View(
                    route="/cuadrados_medios",
                    controls=[mi_vista_cuadrados]
                )
            )
        if page.route == "/multiplicador_constante":
            mi_vista_multiplicador = VistaMultiplicadorConstante()
            page.views.append(
                ft.View(
                    route="/multiplicador_constante",
                    controls=[mi_vista_multiplicador]
                )
            )
        if page.route == "/algoritmo_lineal":
            mi_vista_lineal = VistaMetodoLineal()
            page.views.append(
                ft.View(
                    route="/algoritmo_lineal",
                    controls=[mi_vista_lineal]
                )
            )
        page.update()

    # Manejador de volver atrás
    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    # Asignamos los eventos
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Pintar la primera pantalla directamente
    route_change()

if __name__ == "__main__":
    ft.run(main)