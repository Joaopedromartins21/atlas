# Arquitetura do Sistema Atlas

## Visão Geral
O Atlas é um microsserviço para localização de estabelecimentos próximos ao usuário, utilizando a API do Google Maps Places.

## Componentes

### 1. Backend (API REST)
- **Tecnologia**: Python + FastAPI
- **Porta**: 8000
- **Responsabilidades**:
  - Receber requisições de busca de estabelecimentos
  - Integrar com Google Maps Places API
  - Gerenciar histórico de buscas no banco de dados local
  - Fornecer endpoints RESTful

### 2. Frontend
- **Tecnologia**: HTML + CSS + JavaScript (Vanilla)
- **Responsabilidades**:
  - Interface para entrada de tipo de estabelecimento
  - Solicitar permissão de geolocalização do navegador
  - Exibir resultados com nome, endereço e telefone
  - Interface responsiva

### 3. Banco de Dados
- **Tecnologia**: SQLite (arquivo local)
- **Arquivo**: `atlas.db`
- **Tabelas**:
  - `searches`: histórico de buscas realizadas
  - `favorites`: estabelecimentos favoritos (preparado para futuras funcionalidades)

## Estrutura de Diretórios

```
atlas/
├── backend/
│   ├── main.py              # Aplicação FastAPI
│   ├── models.py            # Modelos de dados
│   ├── database.py          # Configuração do banco de dados
│   ├── services.py          # Lógica de negócio e integração com Google Maps
│   ├── config.py            # Configurações e variáveis de ambiente
│   └── requirements.txt     # Dependências Python
├── frontend/
│   ├── index.html           # Interface principal
│   ├── style.css            # Estilos
│   └── app.js               # Lógica do frontend
├── atlas.db                 # Banco de dados SQLite (gerado automaticamente)
├── .env.example             # Exemplo de arquivo de configuração
├── .gitignore               # Arquivos a serem ignorados pelo Git
├── README.md                # Documentação do projeto
└── docker-compose.yml       # Configuração Docker (opcional para futuro)
```

## Fluxo de Dados

1. Usuário acessa o frontend e permite geolocalização
2. Usuário digita tipo de estabelecimento (ex: "Distribuidora de Bebidas")
3. Frontend envia requisição POST para `/api/search` com:
   - `query`: tipo de estabelecimento
   - `latitude`: localização do usuário
   - `longitude`: localização do usuário
4. Backend recebe requisição e:
   - Valida dados
   - Chama Google Maps Places API (Nearby Search)
   - Salva busca no banco de dados
   - Retorna resultados formatados
5. Frontend exibe resultados com:
   - Nome do estabelecimento
   - Endereço
   - Telefone (se disponível)
   - Distância aproximada

## Endpoints da API

### POST /api/search
Busca estabelecimentos próximos

**Request Body**:
```json
{
  "query": "Distribuidora de Bebidas",
  "latitude": -23.5505,
  "longitude": -46.6333,
  "radius": 5000
}
```

**Response**:
```json
{
  "results": [
    {
      "name": "Distribuidora ABC",
      "address": "Rua Exemplo, 123",
      "phone": "+55 11 1234-5678",
      "distance": 1200,
      "location": {
        "lat": -23.5515,
        "lng": -46.6343
      }
    }
  ],
  "count": 1
}
```

### GET /api/history
Retorna histórico de buscas

### GET /health
Health check do serviço

## Configuração da API do Google Maps

O usuário deverá criar um arquivo `.env` na raiz do projeto com:

```
GOOGLE_MAPS_API_KEY=SUA_CHAVE_API_AQUI
```

## Segurança

- API Key do Google Maps armazenada em variável de ambiente
- CORS configurado para permitir requisições do frontend
- Validação de entrada de dados
- Rate limiting (preparado para implementação futura)

## Escalabilidade

A arquitetura de microsserviço permite:
- Adicionar novos serviços independentes
- Implementar cache de resultados
- Migrar para banco de dados mais robusto (PostgreSQL, MongoDB)
- Adicionar autenticação e autorização
- Implementar filas de mensagens para processamento assíncrono
