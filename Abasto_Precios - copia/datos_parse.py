import tika
tika.initVM()
from tika import parser
import os
from requests_html import HTMLSession
import pandas as pd


def parse_data(items=os.listdir("Datos")):

    lista_productos = []

    for i_pd in items:

        pdf_text = parser.from_file("Datos\\" + "A_01-11-2017.pdf")

        print("Procesando Archivo: " + i_pd)

        #Funciones
        #Devuelve el menor de dos numeros
        def find_menor(a, b):

            if a == 0 and b == 0:
                menor = 10000
            elif a == 0 or b == 0:
                if a == 0:
                    menor = b
                elif b == 0:
                    menor = a
            elif (a > b):
                menor = b
            else:
                menor = a
            return menor

        #Se lee y almacena el texto del pdf en pdf_parsed
        pdf_parsed = str((pdf_text["content"]))

        #Se quita solo la tabla del pdf de SIMA
        inicio = pdf_parsed.find("\n\nPRODUCTO")
        final = pdf_parsed.find("C.O")
        tabla = pdf_parsed[(inicio + 2):final]

        #Separamos la tabla en filas
        filas = tabla.split("\n\n")

        #Seleccionamos solo la cabecera de Asunción
        cabecera = filas[0]
        indice_cabecera = cabecera.find(" O ")
        cabecera_asu = cabecera[0:(indice_cabecera + 3)]

        #Limpiamos la tabla de productos
        #1. quitamos la cabecera
        #2. eliminamos el ultimo elemento (espacio)

        del filas[0]
        del filas[-1]

        #Asignamos valor de filas a productos para que sea más entendible
        productos = filas
        producto = []

        #Limpiamos los productos
        index = 0
        for i in productos:

            #Seleccionamos solo los datos correspondientes a Asunción
            indice_n = productos[index].find(" N ")
            if indice_n == -1:
                indice_n = 0
            indice_a = productos[index].find(" A ")
            if indice_a == -1:
                indice_a = 0
            indice_e = productos[index].find(" E ")
            if indice_e == -1:
                indice_e = 0
            indice_r = productos[index].find(" - ")
            if indice_r == -1:
                indice_r = 0

            #Seleccionamos el menor de los indices para hacer el corte
            if find_menor(indice_a, indice_e) < find_menor(indice_n, indice_r):
                menor = find_menor(indice_a, indice_e)
            else:
                menor = find_menor(indice_n, indice_r)

            prod_asunc = productos[index][0:(menor + 3)]

            #Separamos la descripción del producto
            indice_gs = prod_asunc.find("Gs")
            descripcion = prod_asunc[0:indice_gs - 1]

            producto.append(descripcion)

            #Separamos la unidad, tenemos que hacer a la inversa porque no funciona
            #con indices negativos
            inverso = prod_asunc[::-1]
            indice_mil = inverso.find("0.")
            if indice_mil == -1:
                indice_mil = inverso.find("-")
            indice_gs2 = inverso.find("sG")
            sub_unidad_inv = inverso[indice_mil:indice_gs2 + 2]
            indice_espacio = sub_unidad_inv.find(" ")
            unidad_inv = sub_unidad_inv[(indice_espacio + 1)::]
            unidad = unidad_inv[::-1]

            producto.append(unidad)

            #Separamos el precio
            indice_cero = inverso.find("0")
            indice_nulo = inverso.find("-")

            if indice_nulo == -1:
                sub_precio_1 = inverso[indice_cero::]
                indice_spac = sub_precio_1.find(" ")
                sub_precio_2 = sub_precio_1[0:indice_spac]
                precio = sub_precio_2[::-1].replace('.', '')
            elif indice_cero != 0 and indice_nulo != -1:
                sub_precio_3 = prod_asunc[prod_asunc.
                                          find("Gs"):prod_asunc.find("-") - 1]
                indice_mil2 = sub_precio_3.find(".0")
                if indice_mil2 != -1:
                    sub_precio_3_inv = sub_precio_3[::-1]
                    precio_inv = sub_precio_3_inv[sub_precio_3_inv.find("0"):
                                                  sub_precio_3_inv.find(" ")]
                    precio = precio_inv[::-1].replace('.', '')
            else:
                precio = 0

            producto.append(precio)

            #Separamos la calidad
            indice_c = prod_asunc.find(" C ")
            if indice_c == -1:
                indice_c = 0
            indice_ro = prod_asunc.find(" R ")
            if indice_ro == -1:
                indice_ro = 0
            indice_eo = prod_asunc.find(" E ")
            if indice_eo == -1:
                indice_eo = 0
            indice_g = prod_asunc.find(" - ")
            if indice_g == -1:
                indice_g = 0

            if find_menor(indice_c, indice_e) < find_menor(
                    indice_ro, indice_g):
                menor_c = find_menor(indice_c, indice_e)
            else:
                menor_c = find_menor(indice_ro, indice_g)

            calidad = prod_asunc[menor_c + 1]

            producto.append(calidad)

            #Seleccionamos la oferta

            oferta = prod_asunc[menor + 1]

            producto.append(oferta)

            #Seleccionamos la fecha
            bloque_a = pdf_parsed[pdf_parsed.find("FECHA: ")::]
            bloque_b = bloque_a[0:bloque_a.find("\n\n")]
            fecha = bloque_b[bloque_b.find(" ")::].replace(' ', '')

            producto.append(fecha)

            #Cargamos el producto con sus atributos a la lista de productos
            lista_productos.append(producto)

            producto = []
            menor = 0
            menor_c = 0
            precio = 0
            index += 1

    df = pd.DataFrame(
        lista_productos,
        columns=['PRODUCTO', 'UNIDAD', 'PRECIO', 'CALIDAD', 'OFERTA', 'FECHA'])
    df.to_csv('Datos_Productos.csv', index=False)
    print("Archivo CSV creado exitosamente")


if __name__ == "__main__":
    parse_data()