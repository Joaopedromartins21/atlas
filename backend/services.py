"""
Serviços de integração com Google Maps API
"""
import requests
from typing import List, Optional, Dict, Any
from math import radians, sin, cos, sqrt, atan2
import config
from models import Establishment, Location


class GoogleMapsService:
    """Serviço para integração com Google Maps Places API"""
    
    BASE_URL = "https://maps.googleapis.com/maps/api"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.GOOGLE_MAPS_API_KEY
        if not self.api_key:
            raise ValueError("Google Maps API Key não configurada")
    
    def search_nearby(self, query: str, latitude: float, longitude: float, 
                     radius: int = 5000) -> List[Establishment]:
        """
        Busca estabelecimentos próximos usando Google Places API
        
        Args:
            query: Tipo de estabelecimento (ex: "Distribuidora de Bebidas")
            latitude: Latitude do usuário
            longitude: Longitude do usuário
            radius: Raio de busca em metros
            
        Returns:
            Lista de estabelecimentos encontrados
        """
        # Endpoint: Text Search (mais flexível para queries em linguagem natural)
        url = f"{self.BASE_URL}/place/textsearch/json"
        
        params = {
            "query": query,
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "key": self.api_key,
            "language": "pt-BR"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                if data.get("status") == "ZERO_RESULTS":
                    return []
                raise Exception(f"Erro na API do Google Maps: {data.get('status')}")
            
            results = []
            user_location = (latitude, longitude)
            
            for place in data.get("results", [])[:config.MAX_RESULTS]:
                establishment = self._parse_place(place, user_location)
                if establishment:
                    results.append(establishment)
            
            return results
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao conectar com Google Maps API: {str(e)}")
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém detalhes completos de um estabelecimento
        
        Args:
            place_id: ID do lugar no Google Maps
            
        Returns:
            Dicionário com detalhes do estabelecimento
        """
        url = f"{self.BASE_URL}/place/details/json"
        
        params = {
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number,geometry,rating,opening_hours",
            "key": self.api_key,
            "language": "pt-BR"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK":
                return data.get("result")
            return None
            
        except requests.exceptions.RequestException:
            return None
    
    def _parse_place(self, place: Dict[str, Any], user_location: tuple) -> Optional[Establishment]:
        """
        Converte dados da API do Google Maps para modelo Establishment
        
        Args:
            place: Dados do lugar retornados pela API
            user_location: Tupla (latitude, longitude) do usuário
            
        Returns:
            Objeto Establishment ou None
        """
        try:
            # Localização do estabelecimento
            geometry = place.get("geometry", {})
            location = geometry.get("location", {})
            lat = location.get("lat")
            lng = location.get("lng")
            
            if not lat or not lng:
                return None
            
            # Calcular distância
            distance = self._calculate_distance(
                user_location[0], user_location[1],
                lat, lng
            )
            
            # Telefone (pode não estar disponível na busca inicial)
            phone = place.get("formatted_phone_number")
            
            # Se não tiver telefone, tentar buscar nos detalhes
            if not phone:
                place_id = place.get("place_id")
                if place_id:
                    details = self.get_place_details(place_id)
                    if details:
                        phone = details.get("formatted_phone_number")
            
            establishment = Establishment(
                name=place.get("name", "Nome não disponível"),
                address=place.get("formatted_address", "Endereço não disponível"),
                phone=phone,
                distance=round(distance, 2),
                location=Location(lat=lat, lng=lng),
                rating=place.get("rating"),
                place_id=place.get("place_id")
            )
            
            return establishment
            
        except Exception as e:
            print(f"Erro ao processar estabelecimento: {e}")
            return None
    
    @staticmethod
    def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula distância entre dois pontos usando fórmula de Haversine
        
        Args:
            lat1, lon1: Coordenadas do ponto 1
            lat2, lon2: Coordenadas do ponto 2
            
        Returns:
            Distância em metros
        """
        # Raio da Terra em metros
        R = 6371000
        
        # Converter para radianos
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        # Fórmula de Haversine
        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        
        return distance
