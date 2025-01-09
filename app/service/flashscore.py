from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from service.log import logging_api
import time

def buscar_partido_flashcore(equipo, driver):
    try:
        logging_api.info("Iniciando búsqueda de partido en Flashscore.")
        # Navegar a la página principal de Flashscore
        driver.get("https://www.flashscore.co/futbol/")
        logging_api.info("Página de Flashscore cargada correctamente.")

        # Aceptar cookies
        try:
            btn_capcha = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
            )
            btn_capcha.click()
            logging_api.info("Cookies aceptadas correctamente.")
        except Exception as e:
            logging_api.warning(f"Error al aceptar cookies: {e}")

        # Abrir el buscador
        try:
            btn_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="search-window"]'))
            )
            btn_buscar.click()
            logging_api.info("Buscador abierto correctamente.")
        except Exception as e:
            logging_api.error(f"Error al abrir el buscador: {e}")
            return None

        # Ingresar el nombre del equipo
        try:
            input_equipo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-window"]/div/div/div[2]/input'))
            )
            input_equipo.send_keys(equipo)
            logging_api.info(f"Nombre del equipo '{equipo}' ingresado correctamente.")
        except Exception as e:
            logging_api.error(f"Error al ingresar el nombre del equipo: {e}")
            return None

        # Seleccionar el equipo
        try:
            btn_equipo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="search-window"]/div/div/div[3]/div/a[1]/div[1]'))
            )
            btn_equipo.click()
            logging_api.info(f"Equipo '{equipo}' seleccionado correctamente.")
        except Exception as e:
            logging_api.error(f"Error al seleccionar el equipo: {e}")
            return None
        
        # Validar si el equipo esta jugando en este momento
        try:
            time.sleep(2) 

            res = False
            
            # Ejecutar el script para interactuar con la pestaña de partidos
            script = """
                //partidos hoy
                const partidoHoy = document.querySelector(".tabs__ear");

                if (partidoHoy && partidoHoy.textContent == "Partidos de hoy") {
                    const finalizo = document.querySelector(".event__stage--block");
                    const partidoDatos = document.querySelector(".sportName.soccer");

                    if (partidoDatos) {

                        // Buscar el tiempo del evento dentro de partidoDatos
                        const fechaJuega = partidoDatos.querySelector(".event__time");

                        if (finalizo && finalizo.textContent == "Finalizado") {
                            return false;
                        } else if (fechaJuega) {
                            return true;
                        } else if (finalizo) {
                            return false;
                        } else {
                            return false;
                        }
                    } else {
                        return false;
                    }
                } else {
                    return true;
                }
            """
            res = driver.execute_script(script)
            logging_api.info(f"Se puede investigar: {res}")

        except Exception as e:
            logging_api.error(f"Error al abrir la pestaña de partidos: {e}")
            return None
            
        # Ir a la pestaña de partidos
        try:
            btn_partidos = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="li3"]'))
            )
            btn_partidos.click()
            logging_api.info("Pestaña de partidos abierta correctamente.")
        except Exception as e:
            logging_api.error(f"Error al abrir la pestaña de partidos: {e}")
            return None
        
        # iniciar variable para almacenar el estado del partido
        equipo_local = None
        equipo_visitante = None
        hora = None

        # Extraer información del próximo partido
        try:
            equipo_local_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'wcl-participant_KglL4'))
            )
            equipo_local = equipo_local_element.find_element(By.CLASS_NAME, 'wcl-simpleText_Asp-0').text

            equipo_visitante_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'event__awayParticipant'))
            )
            equipo_visitante = equipo_visitante_element.find_element(By.CLASS_NAME, 'wcl-simpleText_Asp-0').text

            hora_partido_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "event__time"))
            )
            hora = hora_partido_element.text

            dict_partido = {
                "equipo_local": equipo_local,
                "equipo_visitante": equipo_visitante,
                "fecha": hora,
                "estado": res
            }

            logging_api.info(f"Información del partido extraída correctamente: {dict_partido}")
            return dict_partido

        except Exception as e:
            logging_api.error(f"Error al extraer información del partido: {e}")
            return None

    except Exception as e:
        logging_api.error(f"Ocurrió un error general en buscar_partido_flashcore: {e}")
        return None
