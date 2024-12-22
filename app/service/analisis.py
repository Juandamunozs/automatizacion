import json
import os
from env.env import dir_res 
from service.bet import buscar_partido_bet
from service.forebet import buscar_partido_forebet
from service.flashscore import buscar_partido_flashcore
from service.wplay import buscar_partido_wplay
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Verificar si la carpeta 'res' existe; si no, crearla
if not os.path.exists(dir_res):
    os.makedirs(dir_res)

# Función para investigar un partido
def investigar_partido(equipo):
    # Ruta al ChromeDriver
    driver_path = "C:\\selenium\\chromedriver.exe"

    # Configurar el servicio de ChromeDriver
    service = Service(driver_path)

    # Crear instancia del navegador
    driver = webdriver.Chrome(service=service)

    res_flashscore = None
    res_bet = None
    res_forebet = None

    try:
        res_flashscore = buscar_partido_flashcore(equipo, driver)
    except Exception as e:
        print(f"Error en buscar_partido_flashcore: {e}")

    try:
        res_bet = buscar_partido_bet(equipo, driver)
    except Exception as e:
        print(f"Error en buscar_partido_bet: {e}")

    try:
        res_forebet = buscar_partido_forebet(equipo, driver)
    except Exception as e:
        print(f"Error en buscar_partido_forebet: {e}")

    try:
        res_wplay = buscar_partido_wplay(equipo, driver)
    except Exception as e:
        print(f"Error en buscar_partido_wplay: {e}")

    # Cerrar el navegador
    driver.quit()

    dict_global = {
        "datos_partido": res_flashscore,
        "estadisticas": {
            "cuotas_1": res_bet,
            "cuotas_2": res_wplay,
            "ganador": res_forebet
        }
    }

    return diagnostico(dict_global)

def diagnostico(dict_partido):

    try:
        # Extraemos los datos del diccionario
        equipo_local = dict_partido["datos_partido"]["equipo_local"]
        equipo_visitante = dict_partido["datos_partido"]["equipo_visitante"]
        fecha = dict_partido["datos_partido"]["fecha"]
        
        # Extraemos las cuotas del subdiccionario "estadisticas"
        cuota_local_1 = float(dict_partido["estadisticas"]["cuotas_1"]["cuota_local"])
        cuota_empate_1 = float(dict_partido["estadisticas"]["cuotas_1"]["cuota_empate"])
        cuota_visitante_1 = float(dict_partido["estadisticas"]["cuotas_1"]["cuota_visitante"])
        
        cuota_local_2 = float(dict_partido["estadisticas"]["cuotas_2"]["cuota_local"])
        cuota_empate_2 = float(dict_partido["estadisticas"]["cuotas_2"]["cuota_empate"])
        cuota_visitante_2 = float(dict_partido["estadisticas"]["cuotas_2"]["cuota_visitante"])
        # Calcular promedios de cuotas para local, empate y visitante
        promedio_local = (cuota_local_1 + cuota_local_2) / 2
        promedio_empate = (cuota_empate_1 + cuota_empate_2) / 2
        promedio_visitante = (cuota_visitante_1 + cuota_visitante_2) / 2
        
        ganador = dict_partido["estadisticas"]["ganador"]["Ganador"]

        # Determinamos la predicción según los promedios de las cuotas
        if ganador == "1":  # Ganador local
            if promedio_local < promedio_visitante and promedio_local < promedio_empate:
                prediccion = f"El ganador esperado es {equipo_local}, con una cuota promedio de {promedio_local}."
            else:
                prediccion = f"El ganador esperado es {equipo_local}, pero las cuotas favorecen a {equipo_visitante}."
        
        elif ganador == "2":  # Ganador visitante
            if promedio_visitante < promedio_local and promedio_visitante < promedio_empate:
                prediccion = f"El ganador esperado es {equipo_visitante}, con una cuota promedio de {promedio_visitante}."
            else:
                prediccion = f"El ganador esperado es {equipo_visitante}, pero las cuotas favorecen a {equipo_local}."

        elif ganador == "X":  # Empate
            if promedio_empate < promedio_local and promedio_empate < promedio_visitante:
                prediccion = f"Se espera un empate, con una cuota promedio de {promedio_empate}."
            else:
                prediccion = f"Se espera un empate, pero las cuotas favorecen a uno de los equipos."

        # Actualizamos el diccionario con la predicción
        dict_partido["prediccion"] = prediccion

        # Guardamos el resultado del partido en un archivo JSON
        try:
            archivo_json = os.path.join(dir_res, f"{equipo_local}-{equipo_visitante}.json")
            with open(archivo_json, "w") as archivo:
                json.dump(dict_partido, archivo)
            print(f"Archivo guardado: {archivo_json}")
        except Exception as e:
            print(f"Error al guardar el archivo JSON: {e}")

        return prediccion
 
    except Exception as e:
        return f"Error en diagnostico: {e}"
