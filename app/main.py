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
    """
    Endpoint que recibe el nombre de un equipo de fútbol y utiliza la función buscar_partido_flashcore para obtener información del partido.

    **Parámetros:**
    - `team_name` (str): Nombre del equipo de fútbol.

    **Respuesta:**
    - Devuelve un diccionario con la información del partido encontrado.

    **Errores:**
    - Si no se encuentra información del partido, devuelve un error 404.

    **Ejemplo de uso:**
    ```json
    {
        "team_name": "atletico nacional"
    }
    ```

    Respuesta esperada:
    ```json
    {
        "team_name": "atletico nacional",
        "match_info": "Detalles del partido encontrado"
    }
    """

    inicia_analisis = time.time()

    team_name = data.team_name

    try:
        # Aquí se obtiene la predicción o el diagnóstico del partido
        match_info = investigar_partido(team_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No se encontró información para el equipo {team_name}: {str(e)}")
    
    finaliza_analisis = time.time()

    tiempo_analisis = finaliza_analisis - inicia_analisis

    return {
        "team_name": team_name,
        "match_info": match_info,
        "tiempo_analisis": f"{tiempo_analisis:.2f} s"
    }

"""

Para ejecutar la aplicación, puedes utilizar el siguiente comando:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

"""