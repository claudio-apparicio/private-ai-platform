"""Una llamada de chat a OpenRouter y una fila en data/runs/model_calls.csv."""

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
RUTA_CSV = RAIZ / "data" / "runs" / "model_calls.csv"
COLUMNAS = [
    "timestamp_utc",
    "model_requested",
    "model_resolved",
    "provider",
    "generation_id",
    "prompt_tokens",
    "completion_tokens",
    "cost_usd",
    "latency_ms",
    "status",
    "error",
]
PROMPT_DEFECTO = (
    "¿Qué es la generación aumentada por recuperación (RAG)? "
    "Respondé en tres oraciones."
)


def cargar_entorno() -> None:
    load_dotenv(RAIZ / ".env")


def exigir_clave() -> str:
    clave = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not clave:
        print(
            "Falta OPENROUTER_API_KEY. Copiá .env.example a .env y completá la clave.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return clave


def base_url() -> str:
    return os.environ.get(
        "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
    ).rstrip("/")


def ahora_utc() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def registrar(fila: dict) -> None:
    RUTA_CSV.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not RUTA_CSV.exists()
    with RUTA_CSV.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        if nuevo:
            escritor.writeheader()
        escritor.writerow({columna: fila.get(columna, "") for columna in COLUMNAS})


def texto_asistente(cuerpo: dict) -> str:
    opciones = cuerpo.get("choices") or []
    if not opciones or not isinstance(opciones[0], dict):
        return ""
    mensaje = opciones[0].get("message") or {}
    if not isinstance(mensaje, dict):
        return ""
    contenido = mensaje.get("content")
    if isinstance(contenido, str):
        return contenido
    if isinstance(contenido, list):
        partes = []
        for bloque in contenido:
            if isinstance(bloque, dict) and isinstance(bloque.get("text"), str):
                partes.append(bloque["text"])
            elif isinstance(bloque, str):
                partes.append(bloque)
        return "".join(partes)
    return ""


def proveedor_de(cuerpo: dict) -> str:
    valor = cuerpo.get("provider")
    if isinstance(valor, str) and valor.strip():
        return valor.strip()
    if isinstance(valor, dict):
        for clave in ("name", "id", "provider"):
            candidato = valor.get(clave)
            if isinstance(candidato, str) and candidato.strip():
                return candidato.strip()
    opciones = cuerpo.get("choices") or []
    if opciones and isinstance(opciones[0], dict):
        anidado = opciones[0].get("provider")
        if isinstance(anidado, str) and anidado.strip():
            return anidado.strip()
        if isinstance(anidado, dict):
            for clave in ("name", "id"):
                candidato = anidado.get(clave)
                if isinstance(candidato, str) and candidato.strip():
                    return candidato.strip()
    return ""


def uso_de(cuerpo: dict) -> tuple[str, str, str]:
    uso = cuerpo.get("usage") if isinstance(cuerpo.get("usage"), dict) else {}
    return (
        "" if uso.get("prompt_tokens") is None else str(uso.get("prompt_tokens")),
        "" if uso.get("completion_tokens") is None else str(uso.get("completion_tokens")),
        "" if uso.get("cost") is None else str(uso.get("cost")),
    )


def mensaje_http(respuesta: httpx.Response) -> str:
    base = f"Error HTTP {respuesta.status_code}"
    try:
        cuerpo = respuesta.json()
    except ValueError:
        return f"{base}."
    error = cuerpo.get("error") if isinstance(cuerpo, dict) else None
    detalle = ""
    if isinstance(error, dict) and isinstance(error.get("message"), str):
        detalle = error["message"]
    elif isinstance(error, str):
        detalle = error
    detalle = " ".join(detalle.split())
    if not detalle:
        return f"{base}."
    return f"{base}: {detalle[:200]}"


def fallar(modelo: str, mensaje: str, latencia_ms: str = "") -> None:
    registrar(
        {
            "timestamp_utc": ahora_utc(),
            "model_requested": modelo,
            "model_resolved": "",
            "provider": "",
            "generation_id": "",
            "prompt_tokens": "",
            "completion_tokens": "",
            "cost_usd": "",
            "latency_ms": latencia_ms,
            "status": "error",
            "error": mensaje,
        }
    )
    print(mensaje, file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    cargar_entorno()
    clave = exigir_clave()

    parser = argparse.ArgumentParser(description="Pregunta a un modelo vía OpenRouter.")
    parser.add_argument(
        "--model",
        default=os.environ.get("DEFAULT_MODEL", "").strip(),
        help="Identificador del modelo. Por defecto, DEFAULT_MODEL.",
    )
    parser.add_argument("--prompt", default=PROMPT_DEFECTO)
    parser.add_argument("--max-tokens", type=int, default=300)
    args = parser.parse_args()

    modelo = (args.model or "").strip()
    if not modelo:
        fallar("", "Falta el modelo. Pasá --model o definí DEFAULT_MODEL en .env.")

    url = f"{base_url()}/chat/completions"
    cuerpo = {
        "model": modelo,
        "messages": [{"role": "user", "content": args.prompt}],
        "max_tokens": args.max_tokens,
        "provider": {"zdr": True, "data_collection": "deny"},
    }
    cabeceras = {
        "Authorization": f"Bearer {clave}",
        "Content-Type": "application/json",
        "X-Title": "private-ai-platform",
    }

    inicio = time.perf_counter()
    try:
        respuesta = httpx.post(url, json=cuerpo, headers=cabeceras, timeout=60.0)
    except httpx.HTTPError:
        latencia = f"{(time.perf_counter() - inicio) * 1000:.1f}"
        fallar(modelo, "Error de red al llamar al modelo.", latencia)
    latencia_ms = int(round((time.perf_counter() - inicio) * 1000))

    if respuesta.status_code >= 400:
        fallar(modelo, mensaje_http(respuesta), str(latencia_ms))

    try:
        datos = respuesta.json()
    except ValueError:
        fallar(modelo, "La respuesta no es JSON.", str(latencia_ms))

    if not isinstance(datos, dict):
        fallar(modelo, "La respuesta no tiene el formato esperado.", str(latencia_ms))

    entrada, salida, costo = uso_de(datos)
    modelo_resuelto = datos.get("model") if isinstance(datos.get("model"), str) else ""
    identificador = datos.get("id") if isinstance(datos.get("id"), str) else ""
    proveedor = proveedor_de(datos)
    texto = texto_asistente(datos)

    if costo == "":
        costo_csv = ""
        costo_txt = "-"
    else:
        try:
            costo_csv = f"{float(costo):.6f}"
            costo_txt = costo_csv
        except ValueError:
            costo_csv = ""
            costo_txt = "-"

    registrar(
        {
            "timestamp_utc": ahora_utc(),
            "model_requested": modelo,
            "model_resolved": modelo_resuelto,
            "provider": proveedor,
            "generation_id": identificador,
            "prompt_tokens": entrada,
            "completion_tokens": salida,
            "cost_usd": costo_csv,
            "latency_ms": latencia_ms,
            "status": "ok",
            "error": "",
        }
    )

    print(texto)
    print(
        f"modelo={modelo_resuelto or modelo} proveedor={proveedor or '-'} "
        f"entrada={entrada or 0} salida={salida or 0} "
        f"costo_usd={costo_txt} latencia_ms={latencia_ms}"
    )


if __name__ == "__main__":
    main()
