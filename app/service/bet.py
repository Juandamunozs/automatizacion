from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from service.log import logging_api

def buscar_partido_bet(equipo, driver):
    try:
        logging_api.info(f"Buscando partido en Bet365 para el equipo {equipo}")
        driver.get("https://www.365scores.com/es")
        logging_api.info("Página de Bet365 cargada correctamente.")
        
        try:
            btn_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'site-header_search_button__3pJPq'))
            )
            btn_buscar.click()
            logging_api.info("Botón de búsqueda clickeado.")
        except Exception as e:
            logging_api.error(f"Error al hacer clic en el botón de búsqueda: {e}")
            return None

        time.sleep(2)

        try:
            input_equipo = driver.find_element(By.CLASS_NAME, 'new-search-widget_input__aoNqC')
            input_equipo.send_keys(equipo)
            logging_api.info(f"Nombre del equipo '{equipo}' ingresado en el campo de búsqueda.")
        except Exception as e:
            logging_api.error(f"Error al ingresar el nombre del equipo: {e}")
            return None

        time.sleep(2)

        try:
            btn_equipo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'new-search-widget_entity_item_name__8GMjg'))
            )
            btn_equipo.click()
            logging_api.info(f"Equipo '{equipo}' seleccionado de los resultados.")
        except Exception as e:
            logging_api.error(f"Error al seleccionar el equipo: {e}")
            return None

        time.sleep(2)

        try:
            local_element = driver.find_element(By.XPATH, "//div[contains(@class, 'game-card-odds-cell_container__+hv7z')][1]//bdi")
            draw_element = driver.find_element(By.XPATH, "//div[contains(@class, 'game-card-odds-cell_container__+hv7z')][2]//bdi")
            visitor_element = driver.find_element(By.XPATH, "//div[contains(@class, 'game-card-odds-cell_container__+hv7z')][3]//bdi")

            estadistica_local = local_element.text.strip()
            estadistica_empate = draw_element.text.strip()
            estadistica_visitante = visitor_element.text.strip()
            logging_api.info("Cuotas obtenidas correctamente: "
                             f"Local: {estadistica_local}, Empate: {estadistica_empate}, Visitante: {estadistica_visitante}.")
        except Exception as e:
            logging_api.error(f"Error al obtener las estadísticas: {e}")
            return None

        time.sleep(2)

        try:
            btn_estadisticas = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/main/div[4]/div[2]/div[1]/div/div/div[1]/div/div[2]/div[4]/a[1]'))
            )
            btn_estadisticas.click()
            logging_api.info("Botón de estadísticas clickeado.")
        except Exception as e:
            logging_api.warning(f"Error al abrir las estadísticas: {e}")

        try:
            btn_probabilidades = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="navigation-tabs_game-center_odds"]/div'))
            )
            btn_probabilidades.click()
            logging_api.info("Pestaña de probabilidades abierta correctamente.")
        except Exception as e:
            logging_api.warning(f"Error al abrir probabilidades: {e}")

        try:
            btn_doble_chance = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/main/div[4]/div[2]/div[1]/div[4]/div[1]/div[2]/div'))
            )
            btn_doble_chance.click()
            logging_api.info("Opción de 'Doble Chance' seleccionada.")
        except Exception as e:
            logging_api.warning(f"Error al abrir doble chance: {e}")

        try:
            btn_goles_partido = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/main/div[4]/div[2]/div[1]/div[4]/div[1]/div[3]/div'))
            )
            btn_goles_partido.click()
            logging_api.info("Opción de 'Goles del Partido' seleccionada.")
        except Exception as e:
            logging_api.warning(f"Error al abrir goles del partido: {e}")

        dict_partido = {
            "cuota_local": estadistica_local, 
            "cuota_empate": estadistica_empate,
            "cuota_visitante": estadistica_visitante
        }

        logging_api.info(f"Datos del partido recopilados: {dict_partido}")
        print(f"bet {dict_partido}")

        return dict_partido

    except Exception as e:
        logging_api.critical(f"Ocurrió un error general en buscar_partido_bet: {e}")
        return None
