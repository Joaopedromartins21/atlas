"""
Gerenciamento do banco de dados SQLite
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import config


class Database:
    """Classe para gerenciar operações do banco de dados"""
    
    def __init__(self, db_path: Path = config.DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Cria e retorna uma conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de histórico de buscas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                radius INTEGER NOT NULL,
                results_count INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de favoritos (preparada para futuras funcionalidades)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Índices para melhor performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_searches_timestamp 
            ON searches(timestamp DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_favorites_place_id 
            ON favorites(place_id)
        """)
        
        conn.commit()
        conn.close()
    
    def save_search(self, query: str, latitude: float, longitude: float, 
                   radius: int, results_count: int) -> int:
        """Salva uma busca no histórico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO searches (query, latitude, longitude, radius, results_count)
            VALUES (?, ?, ?, ?, ?)
        """, (query, latitude, longitude, radius, results_count))
        
        search_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return search_id
    
    def get_search_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retorna o histórico de buscas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, query, latitude, longitude, radius, results_count, timestamp
            FROM searches
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                "id": row["id"],
                "query": row["query"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "radius": row["radius"],
                "results_count": row["results_count"],
                "timestamp": row["timestamp"]
            })
        
        return history
    
    def add_favorite(self, place_id: str, name: str, address: str, phone: str = None) -> bool:
        """Adiciona um estabelecimento aos favoritos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO favorites (place_id, name, address, phone)
                VALUES (?, ?, ?, ?)
            """, (place_id, name, address, phone))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Já existe nos favoritos
            return False
    
    def get_favorites(self) -> List[Dict[str, Any]]:
        """Retorna a lista de favoritos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, place_id, name, address, phone, added_at
            FROM favorites
            ORDER BY added_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        favorites = []
        for row in rows:
            favorites.append({
                "id": row["id"],
                "place_id": row["place_id"],
                "name": row["name"],
                "address": row["address"],
                "phone": row["phone"],
                "added_at": row["added_at"]
            })
        
        return favorites
    
    def remove_favorite(self, place_id: str) -> bool:
        """Remove um estabelecimento dos favoritos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM favorites WHERE place_id = ?", (place_id,))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted


# Instância global do banco de dados
db = Database()
