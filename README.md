# 🗺️ Atlas - Sistema de Localização de Estabelecimentos

Atlas é um microsserviço desenvolvido para localizar estabelecimentos próximos à localização do usuário, utilizando a API do Google Maps Places. O sistema permite buscar qualquer tipo de estabelecimento (distribuidoras de bebidas, farmácias, restaurantes, etc.) e retorna informações detalhadas incluindo nome, endereço e número de telefone.

## 🚀 Funcionalidades

- **Busca por proximidade**: Localiza estabelecimentos próximos baseado na geolocalização do usuário
- **Informações completas**: Nome, endereço, telefone, distância e avaliação
- **Raio de busca configurável**: De 1km até 20km
- **Histórico de buscas**: Mantém registro das buscas realizadas
- **Interface responsiva**: Funciona em desktop e dispositivos móveis
- **API REST**: Endpoints bem documentados para integração
- **Banco de dados local**: SQLite para armazenamento de histórico e favoritos

## 📋 Pré-requisitos

- Python 3.11 ou superior
- Chave de API do Google Maps com Places API habilitada
- Navegador web moderno com suporte a geolocalização

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/atlas.git
cd atlas
```

### 2. Configure o ambiente Python

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure a API do Google Maps

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Habilite a **Places API**
4. Crie uma chave de API
5. Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

6. Edite o arquivo `.env` e adicione sua chave:

```env
GOOGLE_MAPS_API_KEY=sua_chave_api_aqui
```

### 4. Inicie o servidor

```bash
cd backend
python main.py
```

O servidor estará disponível em `http://localhost:8000`

## 📖 Uso

### Interface Web

1. Acesse `http://localhost:8000` no navegador
2. Permita o acesso à sua localização quando solicitado
3. Digite o tipo de estabelecimento que deseja buscar (ex: "Distribuidora de Bebidas")
4. Selecione o raio de busca desejado
5. Clique em "Buscar"
6. Os resultados serão exibidos com todas as informações disponíveis

### API REST

#### Buscar estabelecimentos

```bash
POST /api/search
Content-Type: application/json

{
  "query": "Distribuidora de Bebidas",
  "latitude": -23.5505,
  "longitude": -46.6333,
  "radius": 5000
}
```

**Resposta:**

```json
{
  "results": [
    {
      "name": "Distribuidora ABC",
      "address": "Rua Exemplo, 123 - São Paulo, SP",
      "phone": "+55 11 1234-5678",
      "distance": 1200.5,
      "location": {
        "lat": -23.5515,
        "lng": -46.6343
      },
      "rating": 4.5,
      "place_id": "ChIJ..."
    }
  ],
  "count": 1,
  "query": "Distribuidora de Bebidas",
  "user_location": {
    "lat": -23.5505,
    "lng": -46.6333
  }
}
```

#### Obter histórico de buscas

```bash
GET /api/history?limit=10
```

#### Health Check

```bash
GET /health
```

## 🏗️ Arquitetura

O Atlas foi desenvolvido seguindo princípios de microsserviços para facilitar futuras expansões:

```
atlas/
├── backend/              # API REST
│   ├── main.py          # Aplicação FastAPI
│   ├── models.py        # Modelos de dados (Pydantic)
│   ├── database.py      # Gerenciamento SQLite
│   ├── services.py      # Integração Google Maps
│   ├── config.py        # Configurações
│   └── requirements.txt # Dependências
├── frontend/            # Interface web
│   ├── index.html      # Página principal
│   ├── style.css       # Estilos
│   └── app.js          # Lógica do cliente
├── atlas.db            # Banco de dados SQLite (gerado automaticamente)
├── .env.example        # Exemplo de configuração
└── README.md           # Documentação
```

### Tecnologias Utilizadas

**Backend:**
- FastAPI - Framework web moderno e rápido
- Pydantic - Validação de dados
- SQLite - Banco de dados local
- Requests - Cliente HTTP para Google Maps API

**Frontend:**
- HTML5 + CSS3 - Interface responsiva
- JavaScript (Vanilla) - Lógica do cliente
- Geolocation API - Obtenção de localização

## 🔒 Segurança

- A chave da API do Google Maps é armazenada em variável de ambiente
- Validação de entrada em todos os endpoints
- CORS configurado adequadamente
- Banco de dados local para privacidade

## 🚧 Roadmap

Funcionalidades planejadas para futuras versões:

- [ ] Sistema de favoritos completo
- [ ] Autenticação de usuários
- [ ] Cache de resultados
- [ ] Filtros avançados (horário de funcionamento, avaliação mínima)
- [ ] Exportação de resultados (PDF, CSV)
- [ ] Integração com outras APIs de mapas
- [ ] Notificações de estabelecimentos próximos
- [ ] Modo offline com dados em cache

## 📝 Documentação da API

A documentação interativa da API está disponível em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contribuindo

Contribuições são bem-vindas! Este projeto foi estruturado como microsserviço para facilitar a adição de novas funcionalidades.

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👤 Autor

Sistema Atlas - Desenvolvido como microsserviço escalável para localização de estabelecimentos.

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique a documentação da API
2. Consulte os logs do servidor
3. Abra uma issue no GitHub

## 📚 Recursos Adicionais

- [Documentação Google Maps Places API](https://developers.google.com/maps/documentation/places/web-service)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Geolocation API](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API)
