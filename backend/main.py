"""
API REST do Sistema Atlas
Microsserviço para localização de estabelecimentos próximos
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
from pathlib import Path
import config
from models import (
    SearchRequest, SearchResponse, HealthResponse, 
    Location, SearchHistory
)
from services import GoogleMapsService
from database import db

# Inicializar aplicação FastAPI
app = FastAPI(
    title="Atlas API",
    description="Microsserviço para localização de estabelecimentos próximos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar diretório de arquivos estáticos (frontend)
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/", include_in_schema=False)
async def root():
    """Redireciona para o frontend"""
    return FileResponse(str(frontend_path / "index.html"))


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check do serviço
    
    Verifica se o serviço está funcionando e se a API do Google Maps está configurada
    """
    return HealthResponse(
        status="healthy",
        service="Atlas API",
        timestamp=datetime.now(),
        google_maps_configured=bool(config.GOOGLE_MAPS_API_KEY)
    )


@app.post("/api/search", response_model=SearchResponse, tags=["Search"])
async def search_establishments(request: SearchRequest):
    """
    Busca estabelecimentos próximos
    
    Args:
        request: Dados da busca (query, latitude, longitude, radius)
        
    Returns:
        Lista de estabelecimentos encontrados com informações de contato
        
    Raises:
        HTTPException: Se houver erro na busca ou API não configurada
    """
    # Verificar se API Key está configurada
    if not config.GOOGLE_MAPS_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google Maps API Key não configurada. Configure a variável de ambiente GOOGLE_MAPS_API_KEY."
        )
    
    try:
        # Inicializar serviço do Google Maps
        maps_service = GoogleMapsService()
        
        # Buscar estabelecimentos
        establishments = maps_service.search_nearby(
            query=request.query,
            latitude=request.latitude,
            longitude=request.longitude,
            radius=request.radius
        )
        
        # Salvar busca no histórico
        db.save_search(
            query=request.query,
            latitude=request.latitude,
            longitude=request.longitude,
            radius=request.radius,
            results_count=len(establishments)
        )
        
        # Preparar resposta
        response = SearchResponse(
            results=establishments,
            count=len(establishments),
            query=request.query,
            user_location=Location(lat=request.latitude, lng=request.longitude)
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estabelecimentos: {str(e)}"
        )


@app.get("/api/history", tags=["History"])
async def get_search_history(limit: int = 50):
    """
    Retorna histórico de buscas realizadas
    
    Args:
        limit: Número máximo de registros a retornar (padrão: 50)
        
    Returns:
        Lista de buscas anteriores
    """
    try:
        history = db.get_search_history(limit=limit)
        return {
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar histórico: {str(e)}"
        )


@app.get("/api/favorites", tags=["Favorites"])
async def get_favorites():
    """
    Retorna lista de estabelecimentos favoritos
    
    Returns:
        Lista de favoritos
    """
    try:
        favorites = db.get_favorites()
        return {
            "favorites": favorites,
            "count": len(favorites)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar favoritos: {str(e)}"
        )


@app.post("/api/favorites", tags=["Favorites"])
async def add_favorite(place_id: str, name: str, address: str, phone: str = None):
    """
    Adiciona um estabelecimento aos favoritos
    
    Args:
        place_id: ID do lugar no Google Maps
        name: Nome do estabelecimento
        address: Endereço
        phone: Telefone (opcional)
        
    Returns:
        Confirmação da operação
    """
    try:
        success = db.add_favorite(place_id, name, address, phone)
        if success:
            return {"message": "Estabelecimento adicionado aos favoritos"}
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Estabelecimento já está nos favoritos"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao adicionar favorito: {str(e)}"
        )


@app.delete("/api/favorites/{place_id}", tags=["Favorites"])
async def remove_favorite(place_id: str):
    """
    Remove um estabelecimento dos favoritos
    
    Args:
        place_id: ID do lugar no Google Maps
        
    Returns:
        Confirmação da operação
    """
    try:
        success = db.remove_favorite(place_id)
        if success:
            return {"message": "Estabelecimento removido dos favoritos"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estabelecimento não encontrado nos favoritos"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover favorito: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
