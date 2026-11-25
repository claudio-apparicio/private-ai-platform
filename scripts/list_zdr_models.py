"""Lista hasta 30 modelos con endpoint de retención cero, ordenados por precio de entrada."""

import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
TOPE = 30


def precio_numero(valor) -> float | None:
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        texto = valor.strip().replace(",", "")
        if not texto:
            return None
        try:
            return float(texto)
        except ValueError:
            return None
    return None


def por_millon(valor) -> float | None:
    """OpenRouter suele publicar USD por token. Si el número es chico, se pasa a USD por millón."""
    numero = precio_numero(valor)
    if numero is None:
        return None
    if abs(numero) < 0.01:
        return numero * 1_000_000
    return numero


def leer_precios(nodo: dict) -> tuple[float | None, float | None]:
    precios = nodo.get("pricing")
    if not isinstance(precios, dict):
        precios = {}
    entrada = None
    salida = None
    for clave in ("prompt", "input", "prompt_usd", "input_price"):
        if entrada is None and clave in precios:
            entrada = por_millon(precios.get(clave))
        if entrada is None and clave in nodo:
            entrada = por_millon(nodo.get(clave))
    for clave in ("completion", "output", "completion_usd", "output_price"):
        if salida is None and clave in precios:
            salida = por_millon(precios.get(clave))
        if salida is None and clave in nodo:
            salida = por_millon(nodo.get(clave))
    return entrada, salida


def leer_proveedor(nodo: dict) -> str:
    for clave in ("provider_name", "provider", "tag"):
        valor = nodo.get(clave)
        if isinstance(valor, str) and valor.strip():
            return valor.strip()
        if isinstance(valor, dict):
            for interna in ("name", "id"):
                candidato = valor.get(interna)
                if isinstance(candidato, str) and candidato.strip():
                    return candidato.strip()
    return ""


def leer_modelo(nodo: dict) -> str:
    for clave in ("model_id", "model", "id", "canonical_slug", "name"):
        valor = nodo.get(clave)
        if isinstance(valor, str) and valor.strip() and "/" in valor:
            return valor.strip()
    for clave in ("model_id", "model", "id", "name"):
        valor = nodo.get(clave)
        if isinstance(valor, str) and valor.strip():
            return valor.strip()
    return ""


def caminar(nodo, acumulado: list[dict]) -> None:
    if isinstance(nodo, list):
        for item in nodo:
            caminar(item, acumulado)
        return
    if not isinstance(nodo, dict):
        return
    modelo = leer_modelo(nodo)
    if modelo:
        entrada, salida = leer_precios(nodo)
        acumulado.append(
            {
                "modelo": modelo,
                "proveedor": leer_proveedor(nodo),
                "entrada": entrada,
                "salida": salida,
            }
        )
    for clave in ("data", "endpoints", "models", "items"):
        if clave in nodo:
            caminar(nodo[clave], acumulado)


def unicos(filas: list[dict]) -> list[dict]:
    mejores: dict[str, dict] = {}
    for fila in filas:
        clave = fila["modelo"]
        previo = mejores.get(clave)
        if previo is None:
            mejores[clave] = fila
            continue
        if not previo["proveedor"] and fila["proveedor"]:
            previo["proveedor"] = fila["proveedor"]
        if previo["entrada"] is None and fila["entrada"] is not None:
            previo["entrada"] = fila["entrada"]
            previo["salida"] = fila["salida"]
        elif (
            fila["entrada"] is not None
            and previo["entrada"] is not None
            and fila["entrada"] < previo["entrada"]
        ):
            previo["entrada"] = fila["entrada"]
            previo["salida"] = fila["salida"]
            if fila["proveedor"]:
                previo["proveedor"] = fila["proveedor"]
    orden = list(mejores.values())
    orden.sort(key=lambda fila: (fila["entrada"] is None, fila["entrada"] or 0.0, fila["modelo"]))
    return orden


def formatear(numero: float | None) -> str:
    if numero is None:
        return "-"
    return f"{numero:.4f}"


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
            f"{base}/endpoints/zdr",
            headers={"Authorization": f"Bearer {clave}"},
            timeout=60.0,
        )
    except httpx.HTTPError:
        print("Error de red al listar modelos con retención cero.", file=sys.stderr)
        raise SystemExit(1)

    if respuesta.status_code >= 400:
        print(f"Error HTTP {respuesta.status_code}.", file=sys.stderr)
        raise SystemExit(1)

    try:
        cuerpo = respuesta.json()
    except ValueError:
        print("La respuesta no es JSON.", file=sys.stderr)
        raise SystemExit(1)

    filas: list[dict] = []
    caminar(cuerpo, filas)
    elegidos = unicos(filas)[:TOPE]
    if not elegidos:
        print("No se encontraron modelos en la respuesta.")
        return

    for fila in elegidos:
        proveedor = fila["proveedor"] or "-"
        print(
            f"{fila['modelo']} | {proveedor} | "
            f"entrada_usd_por_millon={formatear(fila['entrada'])} | "
            f"salida_usd_por_millon={formatear(fila['salida'])}"
        )


if __name__ == "__main__":
    main()
