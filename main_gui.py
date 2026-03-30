import flet as ft
from views.view_confirmaciones import VistaConfirmaciones
from views.view_cuadrado_medio import VistaCuadradosMedios
from views.view_producto_medio import VistaProductosMedios
from views.view_metodo_lineal import VistaMetodoLineal
from views.view_multiplicador_constante import VistaMultiplicadorConstante
from views.main import VistaMenu

# IMPORTANTE: Asegúrate de importar tus vistas de pruebas
from views.view_chi_cuadrada import VistaChiCuadrada


def main(page: ft.Page):
    page.title = "Mis Generadores"

    # EL TRUCO: Instanciar todas las vistas UNA SOLA VEZ aquí afuera.
    # Esto evita que se borren tus números generados (las tablas y los inputs)
    # cuando cambies de pantalla y regreses.
    vistas = {
        "/": VistaMenu(page),
        "/productos_medios": VistaProductosMedios(page),
        "/cuadrados_medios": VistaCuadradosMedios(page),
        "/multiplicador_constante": VistaMultiplicadorConstante(),
        "/algoritmo_lineal": VistaMetodoLineal(),
        "/confirmaciones": VistaConfirmaciones(page),
        "/prueba_chi2": VistaChiCuadrada(page),
        # Aquí irán las otras 5 pruebas...
    }

    def route_change(e=None):
        page.views.clear()

        # NIVEL 0: Siempre apilamos el menú principal en el fondo
        page.views.append(ft.View(route="/", controls=[vistas["/"]]))

        # Recuperamos de qué generador venimos (nuestra migaja de pan)
        ruta_origen = page.session.store.get("ruta_origen")

        # NIVEL 1: Vistas Generadoras
        if page.route in [
            "/productos_medios",
            "/cuadrados_medios",
            "/multiplicador_constante",
            "/algoritmo_lineal",
        ]:
            page.views.append(ft.View(route=page.route, controls=[vistas[page.route]]))

        elif page.route == "/confirmaciones" or page.route.startswith("/prueba_"):
            # Si avanzamos a validaciones, dejamos el generador apilado DEBAJO
            if ruta_origen and ruta_origen in vistas:
                page.views.append(
                    ft.View(route=ruta_origen, controls=[vistas[ruta_origen]])
                )

        # NIVEL 2: Menú de Confirmaciones
        if page.route == "/confirmaciones":
            # Actualizamos el texto para que lea la memoria más reciente
            lista_actual = page.session.store.get("lista_ri_actual") or []
            vistas["/confirmaciones"].lbl_info.value = (
                f"Se evaluarán {len(lista_actual)} números generados."
            )

            page.views.append(
                ft.View(route="/confirmaciones", controls=[vistas["/confirmaciones"]])
            )

        elif page.route.startswith("/prueba_"):
            # Si estamos en una prueba, dejamos las validaciones apiladas DEBAJO
            page.views.append(
                ft.View(route="/confirmaciones", controls=[vistas["/confirmaciones"]])
            )

            # NIVEL 3: La Prueba Específica (Chi-Cuadrada, KS, etc.)
            if page.route in vistas:
                page.views.append(
                    ft.View(route=page.route, controls=[vistas[page.route]])
                )

        page.update()

    async def view_pop(e):
        # Cuando le dan a la flecha atrás, Flet saca la última vista y regresa a la que quedó arriba
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


if __name__ == "__main__":
    ft.run(main)
