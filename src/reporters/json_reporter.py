import json
import os
from datetime import datetime
from config.settings import RESULTS_FOLDER


def guardar_resultado(
    contacto: dict,
    consenso: dict,
    score: dict,
    match: dict | None = None,
) -> str:
    """
    Guarda el resultado completo del análisis en un archivo JSON.

    Returns:
        Ruta del archivo generado
    """
    os.makedirs(RESULTS_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"resultado_{timestamp}.json"
    ruta = os.path.join(RESULTS_FOLDER, nombre_archivo)

    resultado = _construir_resultado(contacto, consenso, score, match)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    return ruta


def cargar_resultado(ruta: str) -> dict:
    """Carga un resultado guardado desde un archivo JSON."""
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def listar_resultados() -> list[dict]:
    """
    Lista todos los resultados guardados ordenados por fecha descendente.

    Returns:
        Lista de dicts con {ruta, candidato, fecha, score_final}
    """
    if not os.path.exists(RESULTS_FOLDER):
        return []

    archivos = [
        f for f in os.listdir(RESULTS_FOLDER)
        if f.endswith(".json")
    ]
    archivos.sort(reverse=True)

    resultados = []
    for archivo in archivos:
        ruta = os.path.join(RESULTS_FOLDER, archivo)
        try:
            datos = cargar_resultado(ruta)
            resultados.append({
                "ruta":        ruta,
                "candidato":   datos.get("contacto", {}).get("nombre", "Desconocido"),
                "email":       datos.get("contacto", {}).get("email", ""),
                "fecha":       datos.get("fecha_analisis", ""),
                "score_final": datos.get("consenso", {}).get("score_final", 0),
            })
        except Exception:
            continue

    return resultados


def _construir_resultado(
    contacto: dict,
    consenso: dict,
    score: dict,
    match: dict | None,
) -> dict:
    return {
        "fecha_analisis": datetime.now().isoformat(),
        "contacto":       contacto,
        "consenso":       consenso,
        "score":          score,
        "match":          match,
    }