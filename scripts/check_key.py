"""Muestra el cupo de la clave de OpenRouter, sin imprimir la clave ni la etiqueta."""

import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent


def main() -> None:
    load_dotenv(RAIZ / ".env")
    clave = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not clave:
        print(
            "Falta OPENROUTER_API_KEY. Copiá .env.example a .env y completá la clave.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    base = os.environ.get(
        "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
    ).rstrip("/")
    try:
        respuesta = httpx.get(
            f"{base}/key",
            headers={"Authorization": f"Bearer {clave}"},
            timeout=30.0,
        )
    except httpx.HTTPError:
        print("Error de red al consultar la clave.", file=sys.stderr)
        raise SystemExit(1)

    if respuesta.status_code >= 400:
        print(f"Error HTTP {respuesta.status_code}.", file=sys.stderr)
        raise SystemExit(1)

    try:
        cuerpo = respuesta.json()
    except ValueError:
        print("La respuesta no es JSON.", file=sys.stderr)
        raise SystemExit(1)

    datos = cuerpo.get("data", cuerpo) if isinstance(cuerpo, dict) else {}
    if not isinstance(datos, dict):
        datos = {}

    for campo in ("limit", "limit_reset", "limit_remaining", "usage"):
        valor = datos.get(campo, "")
        print(f"{campo}: {valor}")


if __name__ == "__main__":
    main()
