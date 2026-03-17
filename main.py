from cuadradosmedios import Cuadrado_medio
from productosmedios import Producto_medio
from multplicadorconstante import Multiplicador_constante
from metodolineal import Metodo_lineal
from chicuadrada import Prueba_chi2
from ks import KS_metodo


def main():
    print("menu de seleccion")
    print("escoge el metodo que quieras usar")
    print("1 cuadrados medios")
    print("2 productos medios")
    print("3 multiplicador constantes")
    print("4 algoritmo lineal")
    op = int(input("ingrese su opcion "))

    if op == 1:
        seed = int(input("introduce la semilla "))
        iteraciones = int(input("introduce las iteraciones que quieres hacer "))
        gen = Cuadrado_medio(seed, iteraciones)
        lista_ri = gen.cuadradosmedios()
        gen.imprimir_tabla()
        second(lista_ri)
    elif op == 2:
        seed1 = int(input("introduce la primera semilla "))
        seed2 = int(input("introduce la segunda semilla "))
        iteraciones = int(input("introduce las iteraciones que quieres hacer "))
        gen = Producto_medio(seed1, seed2, iteraciones)
        lista_ri = gen.productosmedios()
        gen.imprimir_tabla()
        second(lista_ri)
    elif op == 3:
        seed = int(input("introduce la semilla "))
        a = int(input("introduce el multiplicador "))
        iteraciones = int(input("introduce las iteraciones que quieres hacer"))
        gen = Multiplicador_constante(a, seed, iteraciones)
        gen.imprimir()
    elif op == 4:
        a = int(input("introduce el multiplicador: "))
        semilla = int(input("introduce la semilla: "))
        c = int(input("introduce el elemento aditivo: "))
        modulo = int(input("introduce el modulo: "))
        n = int(input("introduce el numero de iteraciones: "))
        gen = Metodo_lineal(a, semilla, c, modulo, n)
        gen.metodolineal()
        gen.imprimir_tabla()


def second(lista_ri):
    print("menu de seleccion")
    print("escoge el metodo que quieras usar")
    print("1 chi cuadrada")
    print("2 kolgomorov-smirnof")

    op = int(input("ingrese su opcion "))

    if op == 1:
        alpha = int(input("introduce tu grado de confianza de  0 a 100%:"))
        alpha = 100 - alpha
        alpha = float(alpha / 100)
        chi_cuadrada = Prueba_chi2(lista_ri, alpha)
    elif op == 2:
        alpha = int(input("introduce tu grado de confianza de  0 a 100%:"))
        alpha = 100 - alpha
        alpha = float(alpha / 100)
        ks = KS_metodo(lista_ri, alpha)


if __name__ == "__main__":
    main()
