#!/bin/bash

# Script de inicialização do Atlas
# Este script configura e inicia o sistema Atlas

echo "🗺️  Atlas - Sistema de Localização de Estabelecimentos"
echo "=================================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11 ou superior."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "📝 Criando .env a partir do .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua chave da API do Google Maps"
    echo "   Abra o arquivo .env e substitua 'sua_chave_api_aqui' pela sua chave real"
    echo ""
    read -p "Pressione Enter após configurar a API Key no arquivo .env..."
fi

# Verificar se as dependências estão instaladas
echo "📦 Verificando dependências..."
cd backend

if [ ! -d "venv" ]; then
    echo "🔧 Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

echo "📥 Instalando/atualizando dependências..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Configuração concluída!"
echo ""
echo "🚀 Iniciando servidor Atlas..."
echo "   Acesse: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

# Carregar variáveis de ambiente
export $(cat ../.env | grep -v '^#' | xargs)

# Iniciar servidor
python main.py
