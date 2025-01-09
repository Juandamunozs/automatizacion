from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from service.analisis import investigar_partido
import time

# Crear la aplicación FastAPI
app = FastAPI()

# Modelo de datos para recibir el equipo de fútbol
class TeamRequest(BaseModel):
    team_name: str

@app.post("/buscar-partido", summary="Buscar partido en Flashscore", tags=["Partidos"])
def buscar_partido(data: TeamRequest) -> Dict[str, str]:

    inicia_analisis = time.time()

    team_name = data.team_name

    try:
        # Aquí se obtiene la predicción o el diagnóstico del partido
        match_info = investigar_partido(team_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No se encontró información para el equipo {team_name}: {str(e)}")
    
    finaliza_analisis = time.time()

    tiempo_analisis = finaliza_analisis - inicia_analisis
    minutos = int(tiempo_analisis // 60)
    segundos = int(tiempo_analisis % 60)
    # milisegundos = round((tiempo_analisis % 1) * 1000)

    return {
        "team_name": team_name,
        "match_info": match_info,
        "tiempo_analisis": f"{minutos} minutos, {segundos} segundos"
    }

"""

Para ejecutar la aplicación, puedes utilizar el siguiente comando:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

"""

"""
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
    
# # Configuración del controlador de Chrome
# chrome_options = Options()

# # Ruta al ChromeDriver
# driver_path = "C:\\selenium\\chromedriver.exe"

#     # Configurar el servicio de ChromeDriver
# service = Service(driver_path)

# # Crear instancia del navegador
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # Maximizar la ventana del navegador
# driver.maximize_window()

# equipo = "liverpool"
    
# buscar_partido_wplay(equipo, driver)
"""