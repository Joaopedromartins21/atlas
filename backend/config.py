"""
Configurações do Sistema Atlas
"""
import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações da API do Google Maps
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

# Configurações do banco de dados
DATABASE_PATH = BASE_DIR / "atlas.db"

# Configurações da API
API_HOST = "0.0.0.0"
API_PORT = 8000

# Configurações de busca
DEFAULT_RADIUS = 5000  # 5km em metros
MAX_RADIUS = 50000     # 50km em metros
MAX_RESULTS = 20

# Configurações de CORS
CORS_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
