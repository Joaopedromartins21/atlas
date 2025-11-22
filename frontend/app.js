/**
 * Atlas Frontend Application
 * Sistema de localização de estabelecimentos
 */

class AtlasApp {
    constructor() {
        this.userLocation = null;
        this.apiBaseUrl = window.location.origin;
        this.init();
    }

    /**
     * Inicializa a aplicação
     */
    init() {
        this.setupEventListeners();
        this.requestLocation();
        this.loadHistory();
    }

    /**
     * Configura event listeners
     */
    setupEventListeners() {
        const searchBtn = document.getElementById('searchBtn');
        const searchInput = document.getElementById('searchInput');

        searchBtn.addEventListener('click', () => this.performSearch());
        
        // Buscar ao pressionar Enter
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
    }

    /**
     * Solicita permissão de geolocalização
     */
    requestLocation() {
        const locationText = document.getElementById('locationText');

        if (!navigator.geolocation) {
            this.showMessage('Geolocalização não é suportada pelo seu navegador', 'error');
            locationText.textContent = 'Geolocalização não disponível';
            return;
        }

        locationText.textContent = 'Obtendo sua localização...';

        navigator.geolocation.getCurrentPosition(
            (position) => {
                this.userLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                locationText.textContent = `Localização obtida (${this.userLocation.latitude.toFixed(4)}, ${this.userLocation.longitude.toFixed(4)})`;
                locationText.style.color = '#10b981';
            },
            (error) => {
                let errorMessage = 'Erro ao obter localização';
                
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = 'Permissão de localização negada';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = 'Localização indisponível';
                        break;
                    case error.TIMEOUT:
                        errorMessage = 'Tempo esgotado ao obter localização';
                        break;
                }
                
                this.showMessage(errorMessage, 'error');
                locationText.textContent = errorMessage;
                locationText.style.color = '#ef4444';
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    }

    /**
     * Realiza busca de estabelecimentos
     */
    async performSearch() {
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');
        const radiusSelect = document.getElementById('radiusSelect');
        const query = searchInput.value.trim();

        // Validações
        if (!query) {
            this.showMessage('Por favor, digite o tipo de estabelecimento que deseja buscar', 'error');
            searchInput.focus();
            return;
        }

        if (!this.userLocation) {
            this.showMessage('Aguardando sua localização. Por favor, permita o acesso à localização.', 'error');
            this.requestLocation();
            return;
        }

        // Preparar UI para busca
        this.setLoading(true);
        searchBtn.disabled = true;
        document.getElementById('resultsSection').style.display = 'none';

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: query,
                    latitude: this.userLocation.latitude,
                    longitude: this.userLocation.longitude,
                    radius: parseInt(radiusSelect.value)
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Erro ao buscar estabelecimentos');
            }

            const data = await response.json();
            this.displayResults(data);
            this.loadHistory(); // Atualizar histórico

        } catch (error) {
            console.error('Erro na busca:', error);
            this.showMessage(`Erro: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
            searchBtn.disabled = false;
        }
    }

    /**
     * Exibe resultados da busca
     */
    displayResults(data) {
        const resultsSection = document.getElementById('resultsSection');
        const resultsList = document.getElementById('resultsList');
        const resultsCount = document.getElementById('resultsCount');

        if (data.count === 0) {
            this.showMessage('Nenhum estabelecimento encontrado. Tente aumentar o raio de busca ou usar termos diferentes.', 'info');
            resultsSection.style.display = 'none';
            return;
        }

        // Limpar resultados anteriores
        resultsList.innerHTML = '';
        resultsCount.textContent = `${data.count} encontrado${data.count > 1 ? 's' : ''}`;

        // Criar cards de resultados
        data.results.forEach((establishment, index) => {
            const card = this.createResultCard(establishment, index + 1);
            resultsList.appendChild(card);
        });

        resultsSection.style.display = 'block';
        this.showMessage(`Encontrados ${data.count} estabelecimento(s) para "${data.query}"`, 'success');

        // Scroll suave para resultados
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    /**
     * Cria card de resultado
     */
    createResultCard(establishment, index) {
        const card = document.createElement('div');
        card.className = 'result-card';

        const distanceText = establishment.distance 
            ? establishment.distance >= 1000 
                ? `${(establishment.distance / 1000).toFixed(1)} km`
                : `${Math.round(establishment.distance)} m`
            : '';

        const phoneHtml = establishment.phone
            ? `<div class="result-phone">${establishment.phone}</div>`
            : `<div class="no-phone">Telefone não disponível</div>`;

        const ratingHtml = establishment.rating
            ? `<div class="result-rating">⭐ ${establishment.rating.toFixed(1)}</div>`
            : '';

        card.innerHTML = `
            <div class="result-header">
                <div>
                    <div class="result-name">${index}. ${establishment.name}</div>
                    ${ratingHtml}
                </div>
                ${distanceText ? `<div class="result-distance">${distanceText}</div>` : ''}
            </div>
            <div class="result-address">📍 ${establishment.address}</div>
            ${phoneHtml}
        `;

        return card;
    }

    /**
     * Carrega histórico de buscas
     */
    async loadHistory() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/history?limit=10`);
            
            if (!response.ok) {
                throw new Error('Erro ao carregar histórico');
            }

            const data = await response.json();
            this.displayHistory(data.history);

        } catch (error) {
            console.error('Erro ao carregar histórico:', error);
        }
    }

    /**
     * Exibe histórico de buscas
     */
    displayHistory(history) {
        const historyList = document.getElementById('historyList');

        if (!history || history.length === 0) {
            historyList.innerHTML = '<p class="empty-state">Nenhuma busca realizada ainda</p>';
            return;
        }

        historyList.innerHTML = '';

        history.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';

            const date = new Date(item.timestamp);
            const dateStr = date.toLocaleDateString('pt-BR', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });

            historyItem.innerHTML = `
                <div class="history-query">${item.query}</div>
                <div class="history-meta">
                    ${item.results_count} resultado(s) • 
                    Raio: ${(item.radius / 1000).toFixed(1)} km • 
                    ${dateStr}
                </div>
            `;

            historyList.appendChild(historyItem);
        });
    }

    /**
     * Exibe mensagem para o usuário
     */
    showMessage(message, type = 'info') {
        const messageBox = document.getElementById('messageBox');
        messageBox.textContent = message;
        messageBox.className = `message-box ${type}`;
        messageBox.style.display = 'block';

        // Auto-ocultar após 5 segundos
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 5000);
    }

    /**
     * Controla estado de loading
     */
    setLoading(isLoading) {
        const btnText = document.querySelector('.btn-text');
        const btnLoading = document.querySelector('.btn-loading');

        if (isLoading) {
            btnText.style.display = 'none';
            btnLoading.style.display = 'inline';
        } else {
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
        }
    }
}

// Inicializar aplicação quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new AtlasApp();
});
