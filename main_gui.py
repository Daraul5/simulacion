import flet as ft
from views.view_arribaabajo import VistaArribaAbajo
from views.view_confirmaciones import VistaConfirmaciones
from views.view_cuadrado_medio import VistaCuadradosMedios
from views.view_producto_medio import VistaProductosMedios
from views.view_metodo_lineal import VistaMetodoLineal
from views.view_multiplicador_constante import VistaMultiplicadorConstante
from views.main import VistaMenu
from views.view_chi_cuadrada import VistaChiCuadrada
from views.view_kS import VistaKS

# ... importar las demás pruebas ...


def main(page: ft.Page):
    page.adaptive = True
    page.title = "Mis Generadores"
    page.theme_mode = ft.ThemeMode.DARK
    # 1. DICCIONARIO PERSISTENTE: Solo metemos los menús y los generadores.
    # Quitamos VistaChiCuadrada de aquí.
    vistas = {
        "/": VistaMenu(page),
        "/productos_medios": VistaProductosMedios(page),
        "/cuadrados_medios": VistaCuadradosMedios(page),
        "/multiplicador_constante": VistaMultiplicadorConstante(),
        "/algoritmo_lineal": VistaMetodoLineal(),
        "/confirmaciones": VistaConfirmaciones(page),
    }

    def route_change(e=None):
        page.views.clear()

        # Apilamos el menú principal
        page.views.append(ft.View(route="/", controls=[vistas["/"]]))
        ruta_origen = page.session.store.get("ruta_origen")

        # Apilamos el generador si estamos en uno
        if page.route in [
            "/productos_medios",
            "/cuadrados_medios",
            "/multiplicador_constante",
            "/algoritmo_lineal",
        ]:
            page.views.append(ft.View(route=page.route, controls=[vistas[page.route]]))

        # Apilamos el generador debajo si estamos en validaciones o en una prueba
        elif page.route == "/confirmaciones" or page.route.startswith("/prueba_"):
            if ruta_origen and ruta_origen in vistas:
                page.views.append(
                    ft.View(route=ruta_origen, controls=[vistas[ruta_origen]])
                )

        # Lógica para Confirmaciones
        if page.route == "/confirmaciones":
            lista_actual = page.session.store.get("lista_ri_actual") or []
            vistas["/confirmaciones"].lbl_info.value = (
                f"Se evaluarán {len(lista_actual)} números generados."
            )
            page.views.append(
                ft.View(route="/confirmaciones", controls=[vistas["/confirmaciones"]])
            )

        # LÓGICA PARA LAS PRUEBAS (VISTAS DESECHABLES)
        elif page.route == "/prueba_chi2":
            # 1. Apilamos el menú de confirmaciones abajo para poder darle a "Volver"
            page.views.append(
                ft.View(route="/confirmaciones", controls=[vistas["/confirmaciones"]])
            )

            # 2. INSTANCIAMOS LA PRUEBA EN ESTE MOMENTO EXACTO
            # Esto garantiza que la pantalla nazca totalmente en blanco cada vez que entras
            vista_chi2_fresca = VistaChiCuadrada(page)
            page.views.append(
                ft.View(route="/prueba_chi2", controls=[vista_chi2_fresca])
            )
        elif page.route == "/prueba_ks":
            page.views.append(
                ft.View(route="/confirmaciones", controls=[vistas["/confirmaciones"]])
            )
            vista_ks_fresca = VistaKS(page)
            page.views.append(ft.View(route="/prueba_ks", controls=[vista_ks_fresca]))

        elif page.route == "/prueba_arriba_abajo":
            page.views.append(
                ft.View(route="/confirmaciones", controls=[vistas["/confirmaciones"]])
            )
            vista_arribaabajo_fresca = VistaArribaAbajo(page)
            page.views.append(
                ft.View(
                    route="/prueba_arriba_abajo", controls=[vista_arribaabajo_fresca]
                )
            )
        page.update()

    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change()


if __name__ == "__main__":
    ft.run(main)
