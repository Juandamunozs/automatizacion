//Script para separar solo el partido de furbol y excluir el futbol femenino y otros deportes - wplay
const partidoElements = document.querySelectorAll(".date-group");

if (partidoElements) {
  count = 0;
  partidoElements.forEach((element) => {
    const evDetailElement = element.querySelector(".ev-detail.icon-FOOT");

    // Verificar si el texto de la clase 'ev-detail icon-FOOT' es 'Fútbol' y no contiene 'Fútbol Mujeres'
    if (
      evDetailElement &&
      evDetailElement.textContent.includes("Fútbol") &&
      !evDetailElement.textContent.includes("Fútbol Mujeres")
    ) {
      count++;
      // Buscar el primer enlace que contiene "Especiales"
      const enlaceEspeciales = element.querySelector('a[href*="Especiales"]');

      if (enlaceEspeciales) {
        // Si se encuentra, buscar el siguiente enlace
        const siguienteEnlace = element.querySelector(
          'a[href]:not([href*="Especiales"])'
        );

        if (siguienteEnlace) {
          if (count < 2) {
            console.log("Siguiente enlace encontrado:", siguienteEnlace.href);
            siguienteEnlace.click();
            return;
          }
        } else {
          throw new Error("No se encontró el siguiente enlace.");
        }
      } else {
        // Si no se encuentra "Especiales", buscar cualquier enlace dentro del elemento
        const enlace = element.querySelector("a");
        if (enlace) {
          if (count < 2) {
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

// proximo partido - besoccer
const nombreEquipoText = document.querySelector('.title.ta-c');
console.log("Nombre del equipo:", nombreEquipoText ? nombreEquipoText.textContent : "No encontrado");

const proximoPartido = document.querySelectorAll(".match-link");

if (proximoPartido) {
  proximoPartido.forEach((element) => {
    const equipoLocal = element.querySelector('.team-name.team_left .name');

    if (equipoLocal) {

      if (nombreEquipoText.textContent == equipoLocal.textContent) {
        console.log("Enlace encontrado:", element.href);
        element.click();
      }
    }
  });
}

// Partido en vivo - Prevenir errores en predicciones
const resultadoLocal = document.querySelector(".event__score.event__score--home");
const resultadoVisitante = document.querySelector(".event__score.event__score--away");
const equipoLocal = document.querySelector(".wcl-simpleText_Asp-0.wcl-scores-simpleText-01_pV2Wk.wcl-name_N76Hr");
const equipoVisitante = document.querySelector(".wcl-simpleText_Asp-0.wcl-scores-simpleText-01_pV2Wk.wcl-name_N76Hr");

// Verificar si todos los elementos existen
if (resultadoLocal && resultadoVisitante && equipoLocal && equipoVisitante) {
  const scoreLocal = resultadoLocal.textContent.trim();
  const scoreVisitante = resultadoVisitante.textContent.trim();
  const equipoLocalText = equipoLocal.textContent.trim();
  const equipoVisitanteText = equipoVisitante.textContent.trim();

  // Retornar un objeto JSON con los datos
  return {
    equipoLocal: equipoLocalText,
    resultadoLocal: scoreLocal,
    equipoVisitante: equipoVisitanteText,
    resultadoVisitante: scoreVisitante,
    enJuego: (scoreLocal !== "-" && scoreVisitante !== "-")
  };
} else {
  return null; // Elementos no encontrados
}


//partidos hoy
const partidoHoy = document.querySelector(".tabs__ear");

if (partidoHoy && partidoHoy.textContent == "Partidos de hoy") {
    const finalizo = document.querySelector(".event__stage--block");
    const partidoDatos = document.querySelector(".sportName.soccer");

    if (partidoDatos) {

        // Buscar el tiempo del evento dentro de partidoDatos
        const fechaJuega = partidoDatos.querySelector(".event__time");

        if (finalizo && finalizo.textContent == "Finalizado") {
            console.log("El partido finalizó");
        } else if (fechaJuega) {
            console.log("El partido se juega a las", fechaJuega.textContent);
        } else if (finalizo) {
            console.log("El partido está en el minuto", finalizo.textContent);
        } else {
            console.log("No hay información sobre el estado del partido.");
        }
    } else {
        console.log("No se encontró información sobre el partido en los datos proporcionados.");
    }
} else {
    console.log("No juegan hoy");
}




