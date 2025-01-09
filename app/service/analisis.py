import json
import os
from env.env import dir_res
from service.bet import buscar_partido_bet
from service.log import logging_api
from service.forebet import buscar_partido_forebet
from service.flashscore import buscar_partido_flashcore
from service.wplay import buscar_partido_wplay
from service.besoccer import buscar_partido_besoccer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Función para inicializar el controlador de Chrome
def inicializar_driver():
    # Configuración del controlador de Chrome
    chrome_options = Options()

    # Ruta al ChromeDriver
    driver_path = "C:\\selenium\\chromedriver.exe"

    # Configurar el servicio de ChromeDriver
    service = Service(driver_path)

    # Crear instancia del navegador
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Maximizar la ventana del navegador
    driver.maximize_window()

    return driver

# Función para investigar un partido
def investigar_partido(equipo):

    logging_api.info(f"Investigando estadisticas del proximo partido de {equipo}")

    driver = inicializar_driver()

    res_flashscore = None
    res_bet = None
    res_forebet = None
    res_wplay = None
    res_besoccer = None

    try:
        logging_api.info(f"***** Investigando en flashcore *****")
        res_flashscore = buscar_partido_flashcore(equipo, driver)

        if res_flashscore['estado'] == False:
            logging_api.info(f"No es posible predecir el estado del partido ya que ha finalizado o está en curso.")
            driver.quit()
            return f"No es posible predecir el estado del partido, ya sea porque ya se jugó o está en vivo."

    except Exception as e:
        logging_api.error(f"Error en buscar_partido_flashscore: {e}")
        driver.quit()
        return f"No hay datos disponibles para el próximo partido de {equipo}."

    #todo: este esta en construccion
    # try:
    #     logging_api.info(f"Investigando partido: {equipo} en Bet")
    #     res_bet = buscar_partido_bet(equipo, driver)
    # except Exception as e:
    #     logging_api.error(f"Error en buscar_partido_bet: {e}")

    try:
        logging_api.info(f"***** Investigando en Forebet *****")
        res_forebet = buscar_partido_forebet(equipo, driver)
    except Exception as e:
        logging_api.error(f"Error en buscar_partido_forebet: {e}")

    try:
        logging_api.info(f"***** Investigando en Wplay *****")
        res_wplay = buscar_partido_wplay(equipo, driver)
    except Exception as e:
        logging_api.error(f"Error en buscar_partido_wplay: {e}")

    try:
        logging_api.info(f"***** Investigando en Besoccer *****")
        res_besoccer = buscar_partido_besoccer(equipo, driver)
    except Exception as e:
        logging_api.error(f"Error en buscar_partido_besoccer: {e}")

    # Cerrar el navegador
    driver.quit()

    dict_global = {
        "datos_partido": res_flashscore,
        "estadisticas": {
            # "cuotas_1": res_bet,
            "cuotas": res_wplay,
            "predicciones": res_forebet,
            "tendencias": res_besoccer

        }
    }

    logging_api.info(f"Datos del partido: {dict_global}")

    return diagnostico(dict_global)

def diagnostico(dict_partido):
    try:
        # Extraemos los datos del diccionario
        equipo_local = dict_partido["datos_partido"]["equipo_local"]
        equipo_visitante = dict_partido["datos_partido"]["equipo_visitante"]
        fecha = dict_partido["datos_partido"]["fecha"]

        cuota_local_2 = float(dict_partido["estadisticas"]["cuotas"]["cuota_local"])
        cuota_empate_2 = float(dict_partido["estadisticas"]["cuotas"]["cuota_empate"])
        cuota_visitante_2 = float(dict_partido["estadisticas"]["cuotas"]["cuota_visitante"])

        tendencia_local = float(dict_partido["estadisticas"]["cuotas"]["tendencia_local"])
        tendencia_visitante = float(dict_partido["estadisticas"]["cuotas"]["tendencia_visitante"])

        Ganador_predicho = dict_partido["estadisticas"]["predicciones"]["Ganador_predicho"]

        probabilidad_local = (float(dict_partido["estadisticas"]["predicciones"]["Local_porcentaje"]) + float(dict_partido["estadisticas"]["tendencias"]["Local_porcentaje"])) / 2
        probabilidad_empate = (float(dict_partido["estadisticas"]["predicciones"]["Empate_porcentaje"]) + float(dict_partido["estadisticas"]["tendencias"]["Empate_porcentaje"])) / 2
        probabilidad_visitante = (float(dict_partido["estadisticas"]["predicciones"]["Visitante_porcentaje"]) + float(dict_partido["estadisticas"]["tendencias"]["Visitante_porcentaje"])) / 2

        # Sistema ponderado basado en cuotas, tendencias, probabilidades y ganador predicho
        peso_cuotas = 0.3  
        peso_tendencias = 0.3  
        peso_probabilidades = 0.3  
        peso_ganador_predicho = 0.1  

        # Normalizamos las cuotas para que las menores sean mejores
        puntaje_local = (
            peso_cuotas * (1 / cuota_local_2) +
            peso_tendencias * (tendencia_local / 100) +
            peso_probabilidades * (probabilidad_local / 100) +
            (peso_ganador_predicho if Ganador_predicho == "1" else 0)
        )
        puntaje_visitante = (
            peso_cuotas * (1 / cuota_visitante_2) +
            peso_tendencias * (tendencia_visitante / 100) +
            peso_probabilidades * (probabilidad_visitante / 100) +
            (peso_ganador_predicho if Ganador_predicho == "2" else 0)
        )
        puntaje_empate = (
            peso_cuotas * (1 / cuota_empate_2) +
            peso_probabilidades * (probabilidad_empate / 100) +
            (peso_ganador_predicho if Ganador_predicho == "X" else 0)
        )

        # Definimos el umbral mínimo para decidir un resultado claro
        diferencia_minima = 0.10

        # Determinar el resultado considerando el umbral
        if puntaje_local > puntaje_visitante and puntaje_local > puntaje_empate:
            if puntaje_local - max(puntaje_visitante, puntaje_empate) <= diferencia_minima:
                prediccion = f"{equipo_local} podria ganar o empatar con un puntaje de {puntaje_local:.2f} frente a {equipo_visitante} con puntaje de {puntaje_visitante:.2f}."
            else:
                prediccion = f"El ganador esperado es {equipo_local} con un puntaje de {puntaje_local:.2f} frente a {equipo_visitante} con puntaje de {puntaje_visitante:.2f}."
        elif puntaje_visitante > puntaje_local and puntaje_visitante > puntaje_empate:
            if puntaje_visitante - max(puntaje_local, puntaje_empate) <= diferencia_minima:
                prediccion = f"{equipo_visitante} podria ganar o empatar con un puntaje de {puntaje_visitante:.2f} frente a {equipo_local} con puntaje de {puntaje_local:.2f}."
            else:
                prediccion = f"El ganador esperado es {equipo_visitante} con un puntaje de {puntaje_visitante:.2f} frente a {equipo_local} con puntaje de {puntaje_local:.2f}."
        else:
            if puntaje_empate - max(puntaje_local, puntaje_visitante) <= diferencia_minima:
                prediccion = f"Se espera un empate o un resultado muy ajustado con un puntaje de {puntaje_empate:.2f}."
            else:
                prediccion = f"Se espera un empate con un puntaje de {puntaje_empate:.2f}."

        # Actualizamos el diccionario con la predicción
        dict_partido["prediccion"] = prediccion
        logging_api.info(f"Predicción: {prediccion}")

        # Guardamos el resultado del partido en un archivo JSON
        try:
            archivo_json = os.path.join(dir_res, f"{equipo_local}-{equipo_visitante}.json")
            with open(archivo_json, "w") as archivo:
                json.dump(dict_partido, archivo)
            logging_api.info(f"Archivo JSON guardado: {archivo_json}")
        except Exception as e:
            logging_api.error(f"Error al guardar archivo JSON: {e}")

        return prediccion

    except Exception as e:
        logging_api.error(f"Error en diagnostico: {e}")
        return f"Error en diagnostico: {e}"
    