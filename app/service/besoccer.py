from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from service.log import logging_api

def buscar_partido_besoccer(equipo, driver):
    try:
        logging_api.info(f"Buscando partido en Besoccer para el equipo {equipo}")
        driver.get("https://es.besoccer.com/")

        # Clic en el botón de aceptar cookies
        try:
            btn_acepto = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'css-5fw3i6'))
            )
            btn_acepto.click()
            logging_api.info("Botón de aceptar cookies clickeado")
        except Exception as e:
            logging_api.error(f"Error al hacer clic en el botón de aceptar cookies: {e}")
            return None

        # Ingresar el nombre del equipo
        try:
            input_equipo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'search_input'))
            )
            input_equipo.send_keys(equipo)
            logging_api.info(f"Nombre del equipo '{equipo}' ingresado en el buscador")
        except Exception as e:
            logging_api.error(f"Error al ingresar el nombre del equipo: {e}")
            return None

        # Clic en seleccionar equipo
        try:
            btn_equipo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="autocomplete_values"]/li[2]/a'))
            )
            btn_equipo.click()
            logging_api.info("Botón para seleccionar equipo clickeado")
        except Exception as e:
            logging_api.error(f"Error al hacer clic en el botón de seleccionar equipo: {e}")
            return None

        # Clic en el próximo partido
        try:
            btn_proximo_partido = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.match-link"))
            )

            script = """
                    const nombreEquipoText = document.querySelector('.title.ta-c');  
                    console.log("Nombre del equipo:", nombreEquipoText ? nombreEquipoText.textContent : "No encontrado");

                    const proximoPartido = document.querySelectorAll(".match-link");

                    if (proximoPartido) {
                        proximoPartido.forEach((element) => {
                            const equipoLocal = element.querySelector('.team-name.team_left .name');
                            
                            if (equipoLocal) {

                                if(nombreEquipoText.textContent ==  equipoLocal.textContent){
                                    console.log("Enlace encontrado:", element.href);
                                    element.click();
                                }
                            }
                        });
                    }
            """
            
            driver.execute_script(script)
            logging_api.info("Botón para el próximo partido clickeado correctamente con JavaScript.")
        except Exception as e:
            logging_api.error(f"Error al hacer clic con JavaScript: {e}")
            return None

        # Clic en el análisis
        try:
            btn_analisis = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Análisis')]"))
            )
            btn_analisis.click()
            logging_api.info("Botón de análisis clickeado")
        except Exception as e:
            logging_api.error(f"Error al hacer clic en el botón de análisis: {e}")
            return None

        # Obtener porcentajes de local, empate y visitante
        try:
            # Local
            contenedor_local = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "content-box.t-1"))
            )
            bloque_local = contenedor_local.find_element(By.CLASS_NAME, "poss-box")
            local_porcentaje = bloque_local.find_element(By.TAG_NAME, "strong").text

            # Empate
            contenedor_empate = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "content-box.draw"))
            )
            bloque_empate = contenedor_empate.find_element(By.CLASS_NAME, "poss-box")
            empate_porcentaje = bloque_empate.find_element(By.TAG_NAME, "strong").text

            # Visitante
            contenedor_visitante = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "content-box.t-2"))
            )
            bloque_visitante = contenedor_visitante.find_element(By.CLASS_NAME, "poss-box")
            visitante_porcentaje = bloque_visitante.find_element(By.TAG_NAME, "strong").text

            logging_api.info("Porcentajes obtenidos correctamente")
        except Exception as e:
            logging_api.error(f"Error al buscar los porcentajes: {e}")
            return None

        # Crear diccionario con los porcentajes
        dict_partido = {
            "Local_porcentaje": local_porcentaje.replace('%', ''),
            "Empate_porcentaje": empate_porcentaje.replace('%', ''),
            "Visitante_porcentaje": visitante_porcentaje.replace('%', '')
        }

        logging_api.info(f"Porcentajes obtenidos: {dict_partido}")
        print(dict_partido)
        return dict_partido

    except Exception as e:
        logging_api.critical(f"Error en buscar_partido_besoccer: {e}")
        return None


