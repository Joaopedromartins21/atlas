# 🚀 Guia Rápido - Atlas

## Configuração Inicial (5 minutos)

### 1. Obter Chave da API do Google Maps

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto ou selecione um existente
3. No menu lateral, vá em **APIs e Serviços** > **Biblioteca**
4. Procure por **Places API** e clique em **ATIVAR**
5. Vá em **Credenciais** > **Criar Credenciais** > **Chave de API**
6. Copie a chave gerada

### 2. Configurar o Projeto

```bash
# Clone o repositório
git clone https://github.com/Joaopedromartins21/atlas.git
cd atlas

# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e cole sua chave da API
nano .env
# ou
vim .env
# ou use seu editor preferido
```

No arquivo `.env`, substitua:
```
GOOGLE_MAPS_API_KEY=sua_chave_api_aqui
```

Por:
```
GOOGLE_MAPS_API_KEY=AIzaSyD... (sua chave real)
```

### 3. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 4. Iniciar o Sistema

**Opção 1: Script automático**
```bash
./start.sh
```

**Opção 2: Manual**
```bash
cd backend
python main.py
```

### 5. Acessar o Sistema

Abra seu navegador em: **http://localhost:8000**

## Como Usar

1. **Permitir Localização**: Quando solicitado, clique em "Permitir" para o navegador acessar sua localização
2. **Digite o Estabelecimento**: Ex: "Distribuidora de Bebidas", "Farmácia", "Restaurante"
3. **Escolha o Raio**: Selecione a distância de busca (1km a 20km)
4. **Buscar**: Clique no botão "Buscar"
5. **Ver Resultados**: Os estabelecimentos aparecerão com nome, endereço, telefone e distância

## Endpoints da API

### Buscar Estabelecimentos
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Distribuidora de Bebidas",
    "latitude": -23.5505,
    "longitude": -46.6333,
    "radius": 5000
  }'
```

### Ver Histórico
```bash
curl http://localhost:8000/api/history
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Documentação Interativa da API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Solução de Problemas

### Erro: "Google Maps API Key não configurada"
- Verifique se o arquivo `.env` existe na raiz do projeto
- Confirme que a chave está correta e sem espaços extras
- Certifique-se de que a Places API está habilitada no Google Cloud Console

### Erro: "Localização não disponível"
- Verifique se seu navegador tem permissão para acessar a localização
- Tente usar HTTPS ou localhost (HTTP não funciona em alguns navegadores)
- Em configurações do navegador, permita localização para o site

### Erro: "Nenhum estabelecimento encontrado"
- Aumente o raio de busca
- Tente termos de busca diferentes
- Verifique se há estabelecimentos do tipo buscado na sua região

### Porta 8000 já em uso
```bash
# Encontrar processo usando a porta
lsof -i :8000

# Parar o processo
kill -9 <PID>

# Ou usar outra porta
cd backend
# Edite config.py e altere API_PORT
```

## Estrutura de Arquivos

```
atlas/
├── backend/              # API REST
│   ├── main.py          # Servidor FastAPI
│   ├── models.py        # Modelos de dados
│   ├── database.py      # Banco de dados SQLite
│   ├── services.py      # Integração Google Maps
│   ├── config.py        # Configurações
│   └── requirements.txt # Dependências
├── frontend/            # Interface web
│   ├── index.html      # Página principal
│   ├── style.css       # Estilos
│   └── app.js          # JavaScript
├── .env                # Configuração (NÃO commitar)
├── .env.example        # Exemplo de configuração
├── atlas.db            # Banco de dados (gerado automaticamente)
└── README.md           # Documentação completa
```

## Próximos Passos

- Explore a documentação completa no `README.md`
- Veja a arquitetura detalhada em `ARCHITECTURE.md`
- Adicione favoritos através da API
- Integre com outros sistemas usando os endpoints REST

## Suporte

- Repositório: https://github.com/Joaopedromartins21/atlas
- Issues: https://github.com/Joaopedromartins21/atlas/issues
- Google Maps API Docs: https://developers.google.com/maps/documentation/places
