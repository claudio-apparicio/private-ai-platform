"""Comprueba que el intérprete activo es el del entorno virtual y que httpx está instalado."""

import sys

import httpx

en_venv = sys.prefix != sys.base_prefix

print(f"Python: {sys.version}")
print(f"Ejecutable: {sys.executable}")
print(f"Entorno virtual: {en_venv}")
print(f"httpx: {httpx.__version__}")
