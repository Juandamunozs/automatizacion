from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def buscar_partido_flashcore(equipo, driver):
    
    try:
        # Navegar a la página principal de Flashscore
        driver.get("https://www.flashscore.co/futbol/")

        # Aceptar cookies
        try:
            btn_capcha = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
            )
            btn_capcha.click()
        except Exception as e:
            print(f"Error al aceptar cookies: {e}")

        # Abrir el buscador
        try:
            btn_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="search-window"]'))
            )
            btn_buscar.click()
        except Exception as e:
            print(f"Error al abrir el buscador: {e}")
            return None

        # Ingresar el nombre del equipo
        try:
            input_equipo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-window"]/div/div/div[2]/input'))
            )
            input_equipo.send_keys(equipo)
        except Exception as e:
            print(f"Error al ingresar el nombre del equipo: {e}")
            return None

        # Seleccionar el equipo
        try:
            btn_equipo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="search-window"]/div/div/div[3]/div/a[1]/div[1]'))
            )
            btn_equipo.click()
        except Exception as e:
            print(f"Error al seleccionar el equipo: {e}")
            return None

        # Ir a la pestaña de partidos
        try:
            btn_partidos = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="li3"]'))
            )
            btn_partidos.click()
        except Exception as e:
            print(f"Error al abrir la pestaña de partidos: {e}")
            return None

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
                "fecha": hora
            }

            return dict_partido

        except Exception as e:
            print(f"Error al extraer información del partido: {e}")
            return None

    except Exception as e:
        print(f"Ocurrió un error general: {e}")
        return None
