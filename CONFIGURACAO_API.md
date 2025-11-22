# 🔑 Configuração da API Key do Google Maps

## ✅ Sua API Key já está configurada!

A API Key do Google Maps já foi configurada no sistema e está funcionando perfeitamente.

---

## 📍 Localização do Arquivo

A chave está armazenada no arquivo `.env` na raiz do projeto:

```
atlas/
├── .env              ← Arquivo com sua API Key (NÃO commitar no Git)
├── .env.example      ← Exemplo para referência
└── ...
```

---

## 🔒 Segurança Importante

### ⚠️ NUNCA commite o arquivo `.env` no Git!

O arquivo `.env` contém sua chave privada e **NÃO deve** ser enviado para o GitHub. Ele já está protegido no `.gitignore`.

**Arquivos protegidos:**
- ✅ `.env` - Está no `.gitignore` (não será commitado)
- ✅ `atlas.db` - Banco de dados local (não será commitado)

**Arquivo seguro para compartilhar:**
- ✅ `.env.example` - Exemplo sem chave real (pode ser commitado)

---

## 🔄 Como Usar em Outro Computador

Quando clonar o repositório em outro lugar:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Joaopedromartins21/atlas.git
   cd atlas
   ```

2. **Copie o arquivo de exemplo:**
   ```bash
   cp .env.example .env
   ```

3. **Edite o arquivo `.env` e adicione sua chave:**
   ```bash
   nano .env
   # ou
   vim .env
   ```

4. **Cole sua API Key:**
   ```
   GOOGLE_MAPS_API_KEY=AIzaSyDcooggMr75_n-LnQL8R_rMyUQFbhpOZJ8
   ```

5. **Salve e inicie o sistema:**
   ```bash
   cd backend
   python main.py
   ```

---

## 🧪 Teste Realizado

A API foi testada com sucesso e retornou resultados reais:

**Busca:** "Distribuidora de Bebidas" em São Paulo
**Resultados encontrados:** 20 estabelecimentos
**Informações retornadas:**
- ✅ Nome do estabelecimento
- ✅ Endereço completo
- ✅ Número de telefone
- ✅ Distância em metros
- ✅ Avaliação (rating)

**Exemplo de resultado:**
```json
{
  "name": "Lojas IFRANE distribuidora de bebidas em São Paulo",
  "address": "R. São Paulo, 432 - Liberdade, São Paulo - SP",
  "phone": "(11) 91038-4613",
  "distance": 880.71,
  "rating": 5.0
}
```

---

## 🔧 Gerenciamento da API Key

### Verificar se está configurada

```bash
# No terminal
cat .env
```

### Testar a API

```bash
# Health check
curl http://localhost:8000/health

# Deve retornar:
# "google_maps_configured": true
```

### Alterar a API Key

Se precisar trocar a chave:

1. Edite o arquivo `.env`
2. Substitua a chave antiga pela nova
3. Reinicie o servidor

---

## 📊 Limites da API do Google Maps

A API do Google Maps tem limites de uso:

- **Gratuito:** $200 de crédito mensal
- **Places API:** ~$17 por 1.000 requisições de busca
- **Aproximadamente:** ~11.700 buscas gratuitas por mês

**Dica:** Configure alertas de billing no Google Cloud Console para monitorar o uso.

---

## 🔗 Links Úteis

- **Google Cloud Console:** https://console.cloud.google.com/
- **Gerenciar API Keys:** https://console.cloud.google.com/apis/credentials
- **Documentação Places API:** https://developers.google.com/maps/documentation/places
- **Preços da API:** https://mapsplatform.google.com/pricing/

---

## ✅ Status Atual

- ✅ API Key configurada
- ✅ Places API habilitada
- ✅ Sistema testado e funcionando
- ✅ Banco de dados criado
- ✅ Histórico de buscas ativo
- ✅ Pronto para uso!

---

## 🆘 Solução de Problemas

### Erro: "API Key não configurada"
- Verifique se o arquivo `.env` existe
- Confirme que a chave está sem espaços extras
- Reinicie o servidor

### Erro: "API request failed"
- Verifique se a Places API está habilitada no Google Cloud
- Confirme que a chave não tem restrições que bloqueiam o uso
- Verifique se não excedeu o limite de uso

### Erro: "ZERO_RESULTS"
- Aumente o raio de busca
- Tente termos diferentes
- Verifique se há estabelecimentos do tipo na região

---

## 🎯 Próximos Passos

Agora que a API está configurada, você pode:

1. ✅ Usar o sistema normalmente
2. ✅ Fazer buscas de qualquer tipo de estabelecimento
3. ✅ Integrar com outros sistemas via API REST
4. ✅ Adicionar novas funcionalidades ao microsserviço

**O sistema Atlas está 100% operacional! 🗺️**
