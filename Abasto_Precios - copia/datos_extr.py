import os
from requests_html import HTMLSession
import datetime


def download_data(fecha_actual=datetime.datetime.now(), data_dir='Datos'):
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    session = HTMLSession()

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
        "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    #Datos desde junio de 2017

    for i_anho in range(2005, fecha_actual.year + 1):

        anho = str(i_anho)
        for i_mes in range(1, 13):
            nombre_mes = ""
            mes = i_mes

            if i_mes < 10:
                mes = "0" + str(i_mes)

            nombre_mes = meses[i_mes - 1]

            for i_dia in range(1, 32):
                dia = i_dia
                if i_dia < 10:
                    dia = "0" + str(i_dia)

                fecha_final = str(dia) + '-' + str(mes) + '-' + anho

                response = session.get(
                    'http://www.mag.gov.py/Comercializacion/' + anho + '/' +
                    nombre_mes + '/A_' + fecha_final + '.pdf',
                    verify=False,
                    headers=headers)

                code_response = str(response)

                if code_response == "<Response [404]>":
                    print("No existe archivo con la fecha: " + fecha_final)
                elif code_response == "<Response [200]>":
                    print("Archivo " + fecha_final + " guardado exitosamente")
                    with open("Datos\A_" + fecha_final + ".pdf", "x+b") as f:
                        f.write(response.content)

    session.close()


if __name__ == "__main__":
    download_data()