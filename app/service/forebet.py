from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def buscar_partido_forebet(equipo, driver):

    try:
        # Navegar a la página principal de Forebet
        driver.get("https://www.forebet.com/es/")

        # Clic en el botón de búsqueda
        try:
            btn_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'Uicon'))
            )
            btn_buscar.click()
        except Exception as e:
            print(f"Error al abrir el buscador: {e}")
            return None

        # Ingresar el nombre del equipo
        try:
            input_equipo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'sch_inp'))
            )
            input_equipo.send_keys(equipo)
        except Exception as e:
            print(f"Error al ingresar el nombre del equipo: {e}")
            return None

        # Seleccionar el equipo de la lista de resultados
        try:
            btn_equipo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'sch_li'))
            )
            btn_equipo.click()
        except Exception as e:
            print(f"Error al seleccionar el equipo: {e}")
            return None

        # Mover el cursor para asegurar clics en el área adecuada
        try:
            action = ActionChains(driver)
            action.move_by_offset(100, 100).click().perform()
        except Exception as e:
            print(f"Error al mover el cursor: {e}")

        # Elegir el equipo de los resultados
        try:
            btn_equipo_escoger = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'sch_res'))
            )
            btn_equipo_escoger.click()
        except Exception as e:
            print(f"Error al seleccionar equipo de los resultados: {e}")
            return None

        # Clic en el botón de estadísticas
        try:
            btn_estadisticas = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/div/div[2]/div[2]/div[1]/a'))
            )
            btn_estadisticas.click()
        except Exception as e:
            print(f"Error al abrir estadísticas: {e}")
            return None

        # Recoger datos de las estadísticas
        try:
            ganador_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/div[1]/div[7]/div/div[4]/span/span'))
            )
            ganador = ganador_element.text

        except Exception as e:
            print(f"Error al extraer información del ganador: {e}")
            return None
        
        #probabilidad de ganar - local empate visitante
        try:
            local_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/div[1]/div[7]/div/div[3]/span[1]'))
            )
            local  = local_element.text

            empate_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/div[1]/div[7]/div/div[3]/span[2]'))
            )
            empate  = empate_element.text

            visitante_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/div[1]/div[7]/div/div[3]/span[3]'))
            )
            visitante  = visitante_element.text

        except Exception as e:
            print(f"Error al extraer información del ganador: {e}")
            return None
        
        dict_partido = {
            "Ganador_predicho": ganador,
            "Local_porcentaje": local,
            "Empate_porcentaje": empate,
            "Visitante_porcentaje": visitante
        }
        
        return dict_partido

    except Exception as e:
        print(f"Ocurrió un error general: {e}")
        return None

