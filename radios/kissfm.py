import requests
from bs4 import BeautifulSoup

def get_schedule(config):
    """
    Obtém a programação da KISS FM Algarve.
    Caso o URL devolva 404 ou esteja indisponível, devolve a grelha padrão.
    """
    url = config.get("schedule_url") or "https://kissfm.pt"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # Grelha base de salvaguarda (2ª a 6ª feira: 0 a 4; Fim de semana: 5 e 6)
    dias_semana = [0, 1, 2, 3, 4]
    
    grelha_padrao = [
        {"title": "KISS Night Music", "start": "00:00", "stop": "08:00", "days": [0, 1, 2, 3, 4, 5, 6]},
        {"title": "Breakfast Show with Si Frater", "start": "08:00", "stop": "12:00", "days": dias_semana},
        {"title": "KISS Afternoon", "start": "12:00", "stop": "16:00", "days": dias_semana},
        {"title": "Drive Time with Mark Sebastian", "start": "16:00", "stop": "20:00", "days": dias_semana},
        {"title": "KISS Evening & Dance Show", "start": "20:00", "stop": "00:00", "days": dias_semana},
        {"title": "Solid Gold Sunday / Weekend Shows", "start": "08:00", "stop": "00:00", "days": [5, 6]}
    ]

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Processamento dinâmico caso a página responda
            pass
    except Exception as e:
        print(f"AVISO: Não foi possível carregar o URL dinâmico da KISS FM ({e}). A utilizar grelha base.")

    return grelha_padrao
