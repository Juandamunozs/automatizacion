from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from service.log import logging_api 

# def buscar_partido_wplay(equipo, driver):
def buscar_partido_wplay(equipo, driver):
    try:
        logging_api.info("Iniciando búsqueda de partido en Forebet.")
        driver.get("https://apuestas.wplay.co/es")

        # Ingresar el nombre del equipo
        try:
            input_equipo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="nav-area"]/div[1]/form/label/input'))
            )
            input_equipo.send_keys(equipo)
        except Exception as e:
            logging_api.error(f"Error al ingresar el nombre del equipo: {e}")  
            return None
        
        # Seleccionar el equipo para buscar
        try:
            btn_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-area"]/div[1]/form/div/button'))
            )
            btn_buscar.click()
        except Exception as e:
            logging_api.error(f"Error al seleccionar el equipo: {e}")  
            return None
        
        # Click al partido
        try:
            # Esperar a que el contenedor con la clase 'date-group' esté presente
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'date-group'))  # Sin el punto
            )

            # Esperar a que el enlace dentro de ese contenedor esté presente y sea clickeable
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'date-group'))  # Sin el punto
            )

            # Ejecutar el script para hacer clic en el enlace
            script = """ 
                    const partidoElements = document.querySelectorAll('.date-group');

                    if (partidoElements) {
                        count = 0;
                        partidoElements.forEach((element) => {
                            const evDetailElement = element.querySelector('.ev-detail.icon-FOOT');
                            
                            // Verificar si el texto de la clase 'ev-detail icon-FOOT' es 'Fútbol' y no contiene 'Fútbol Mujeres'
                            if (evDetailElement && evDetailElement.textContent.includes('Fútbol') && !evDetailElement.textContent.includes('Fútbol Mujeres')) {
                                count++;
                                // Buscar el primer enlace que contiene "Especiales"
                                const enlaceEspeciales = element.querySelector('a[href*="Especiales"]');
                                
                                if (enlaceEspeciales) {
                                    // Si se encuentra, buscar el siguiente enlace
                                    const siguienteEnlace = element.querySelector('a[href]:not([href*="Especiales"])');
                                    
                                    if (siguienteEnlace) {
                                        if(count < 2){
                                            console.log("Siguiente enlace encontrado:", siguienteEnlace.href);
                                            siguienteEnlace.click();
                                            return;
                                        }

                                    } else {
                                        throw new Error("No se encontró el siguiente enlace.");
                                    }
                                } else {
                                    // Si no se encuentra "Especiales", buscar cualquier enlace dentro del elemento
                                    const enlace = element.querySelector('a');
                                    if (enlace) {
                                        if(count < 2){
                                            console.log("Enlace encontrado:", enlace.href); 
                                            enlace.click(); // Hace clic en el primer enlace disponible
                                            return; // Detiene el ciclo una vez que se hace clic
                                        }
                                    } else {
                                        throw new Error("Enlace no encontrado dentro del contenedor.");
                                    }
                                }
                            }
                        });
                    } else {
                        throw new Error("Elemento con clase '.date-group' no encontrado.");
                    }
            """
            driver.execute_script(script)
        except Exception as e:
            # Manejo de error
            print(f"Error al seleccionar el partido: {e}")
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

        except Exception as e:
            logging_api.error(f"Error al obtener las cuotas: {e}")  
            return None
        
        intentos = 0
        max_intentos = 4

        while intentos < max_intentos:
            try:
                # Intentar hacer clic en el botón "Tendencias"
                btn_buscar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="content1"]/div[2]/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[3]/button')
                    )
                )
                btn_buscar.click()
                time.sleep(2)  # Pausa para permitir que el contenido cargue

                # Ejecutar el script JS para obtener las tendencias
                tendencias_js = driver.execute_script("""
                    const elementos = document.querySelectorAll('.sr-lmt-plus-0-meetingsandform__fc-value.srt-base-1-home-1, .sr-lmt-plus-0-meetingsandform__fc-value.srt-base-1-away-1');
                    
                    const tendencias = [];
                    elementos.forEach((el) => {
                        tendencias.push(el.textContent.trim());
                    });

                    return tendencias;
                """)

                if tendencias_js:
                    local_tendencia = tendencias_js[0]
                    visitante_tendencia = tendencias_js[1] if len(tendencias_js) > 1 else None
                    break 

                else:
                    logging_api.info("No se encontraron tendencias en este intento.")
                    intentos += 1
                    continue 

            except Exception as e:
                logging_api.error(f"Error al intentar hacer clic en el botón de tendencias: {e}")
                intentos += 1
                continue  #
       
        # Devolver las cuotas
        dict_cuotas = {
            "cuota_local": local_price,
            "cuota_empate": draw_price,
            "cuota_visitante": visitor_price,
            "tendencia_local": local_tendencia,
            "tendencia_visitante": visitante_tendencia
        }

        logging_api.info(f"wplay {dict_cuotas}")  

        return dict_cuotas

    except Exception as e:
        logging_api.error(f"Error al cargar la página: {e}")  
        return None
    
