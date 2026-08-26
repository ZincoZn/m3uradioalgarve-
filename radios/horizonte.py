import requests
from bs4 import BeautifulSoup
import re

def get_schedule(config):
    """
    Obtém a programação da Rádio Horizonte Algarve.
    Tenta aceder à página /pt-pt/programacao; caso não consiga extrair blocos horários válidos,
    devolve o programa padrão de 24 horas.
    """
    url = config.get("schedule_url") or "https://www.radiohorizonte.com/pt-pt/programacao"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    programas = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Tenta localizar blocos ou elementos de grelha de programação no Drupal
            items = soup.find_all(['div', 'article', 'tr'], class_=re.compile(r'(programa|programacao|schedule|views-row)', re.I))
            
            for item in items:
                texto = item.get_text(separator=' ', strip=True)
                # Procura padrões de hora (ex: 08:00 - 10:00 ou 08h00)
                match = re.search(r'(\d{1,2})[:h](\d{2})\s*[-–aA]\s*(\d{1,2})[:h](\d{2})\s*(.*)', texto)
                if match:
                    h_in, m_in, h_fim, m_fim, titulo = match.groups()
                    start = f"{int(h_in):02d}:{m_in}"
                    stop = f"{int(h_fim):02d}:{m_fim}"
                    titulo_limpo = titulo.strip()[:60] if titulo.strip() else "Programação Horizonte"
                    
                    programas.append({
                        "title": titulo_limpo,
                        "start": start,
                        "stop": stop,
                        "days": [0, 1, 2, 3, 4, 5, 6]
                    })
    except Exception as e:
        print(f"AVISO: Não foi possível obter grelha dinâmica para Rádio Horizonte: {e}")

    # Se não foram extraídos programas dinâmicos da página HTML, usa a emissão geral de 24h
    if not programas:
        programas = [
            {
                "title": "Emissão Horizonte Algarve",
                "start": "00:00",
                "stop": "00:00",
                "days": [0, 1, 2, 3, 4, 5, 6]
            }
        ]

    return programas
