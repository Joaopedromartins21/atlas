"""
Modelos de dados do Sistema Atlas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Location(BaseModel):
    """Modelo para coordenadas geográficas"""
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")


class SearchRequest(BaseModel):
    """Modelo para requisição de busca"""
    query: str = Field(..., min_length=1, max_length=200, description="Tipo de estabelecimento a buscar")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude do usuário")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude do usuário")
    radius: Optional[int] = Field(5000, ge=100, le=50000, description="Raio de busca em metros")


class Establishment(BaseModel):
    """Modelo para estabelecimento encontrado"""
    name: str = Field(..., description="Nome do estabelecimento")
    address: str = Field(..., description="Endereço completo")
    phone: Optional[str] = Field(None, description="Número de telefone")
    distance: Optional[float] = Field(None, description="Distância em metros")
    location: Location = Field(..., description="Coordenadas do estabelecimento")
    rating: Optional[float] = Field(None, description="Avaliação (0-5)")
    place_id: Optional[str] = Field(None, description="ID do lugar no Google Maps")


class SearchResponse(BaseModel):
    """Modelo para resposta de busca"""
    results: List[Establishment] = Field(..., description="Lista de estabelecimentos encontrados")
    count: int = Field(..., description="Número de resultados")
    query: str = Field(..., description="Consulta realizada")
    user_location: Location = Field(..., description="Localização do usuário")


class SearchHistory(BaseModel):
    """Modelo para histórico de buscas"""
    id: Optional[int] = None
    query: str
    latitude: float
    longitude: float
    radius: int
    results_count: int
    timestamp: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    """Modelo para resposta de health check"""
    status: str
    service: str
    timestamp: datetime
    google_maps_configured: bool
