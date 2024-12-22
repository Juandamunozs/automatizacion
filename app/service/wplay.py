from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def buscar_partido_wplay(equipo, driver):
    try:
        driver.get("https://apuestas.wplay.co/es")

        # Ingresar el nombre del equipo
        try:
            input_equipo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="nav-area"]/div[1]/form/label/input'))
            )
            input_equipo.send_keys(equipo)
        except Exception as e:
            print(f"Error al ingresar el nombre del equipo: {e}")
            return None
        
        # Seleccionar el equipo para buscar
        try:
            btn_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-area"]/div[1]/form/div/button'))
            )
            btn_buscar.click()
        except Exception as e:
            print(f"Error al seleccionar el equipo: {e}")
            return None
        
        # Click al partido
        try:
            btn_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main-area"]/div/div[2]/div[1]/div/div/div[2]/a'))
            )
            btn_buscar.click()
        except Exception as e:
            print(f"Error al seleccionar el equipo: {e}")
            return None

        time.sleep(2)

        try:
            # Ejemplo de XPath para Local (Tottenham)
            local_price_xpath ='//*[@id="main-area"]/div[4]/div[3]/div[1]/div/table/tbody/tr/td[1]/div/button/span/span[4]'
            local_price = driver.find_element(By.XPATH, local_price_xpath).text

            # Ejemplo de XPath para Empate
            draw_price_xpath = '//*[@id="main-area"]/div[4]/div[3]/div[1]/div/table/tbody/tr/td[2]/div/button/span/span[3]'
            draw_price = driver.find_element(By.XPATH, draw_price_xpath).text

            # Ejemplo de XPath para Visitante (Liverpool)
            visitor_price_xpath = '//*[@id="main-area"]/div[4]/div[3]/div[1]/div/table/tbody/tr/td[3]/div/button/span/span[4]'
            visitor_price = driver.find_element(By.XPATH, visitor_price_xpath).text

            #Devolver las cuotas
            dict_cuotas = {
                "cuota_local": local_price,
                "cuota_empate": draw_price,
                "cuota_visitante": visitor_price
            }

            return dict_cuotas

        except Exception as e:
            print(f"Error al obtener las cuotas: {e}")
            return None

    except Exception as e:
        print(f"Error al cargar la pagina: {e}")
        return None