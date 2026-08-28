import requests
from bs4 import BeautifulSoup
import re

def get_schedule(config):
    """
    Captura a grelha de programação da RUA FM.
    """
    dias_urls = [
        (0, "https://rua.pt/grelha/segunda/"),
        (1, "https://rua.pt/grelha/terca/"),
        (2, "https://rua.pt/grelha/quarta/"),
        (3, "https://rua.pt/grelha/quinta/"),
        (4, "https://rua.pt/grelha/sexta/"),
        (5, "https://rua.pt/grelha/sabado/"),
        (6, "https://rua.pt/grelha/domingo/")
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    programas = []

    for dia_idx, url in dias_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                texto = soup.get_text(separator=" ")
                padrao = re.compile(r'(\d{2}:\d{2})\s*(?:—|-)?\s*(.*?)(?=\d{2}:\d{2}|$)')
                matches = padrao.findall(texto)
                
                for i, (hora_inicio, titulo) in enumerate(matches):
                    titulo_limpo = titulo.strip()
                    if not titulo_limpo or len(titulo_limpo) < 3:
                        continue
                    
                    hora_fim = matches[i + 1][0] if i + 1 < len(matches) else "23:59"
                    
                    programas.append({
                        "title": titulo_limpo,
                        "start": hora_inicio,
                        "stop": hora_fim,
                        "days": [dia_idx]
                    })
        except Exception as e:
            print(f"Falha ao ler {url}: {e}")

    # Grelha de salvaguarda caso a extracção web falhe
    if not programas:
        semana = [0, 1, 2, 3, 4]
        programas = [
            {"title": "Espaço Zion", "start": "00:00", "stop": "02:00", "days": semana},
            {"title": "Ilha de Faro", "start": "02:00", "stop": "08:00", "days": semana},
            {"title": "Café Duplo", "start": "08:00", "stop": "08:15", "days": semana},
            {"title": "Faro em Foco", "start": "08:15", "stop": "08:45", "days": semana},
            {"title": "P de Poesia", "start": "08:45", "stop": "17:00", "days": semana},
            {"title": "Sentido Obrigatório", "start": "17:00", "stop": "18:15", "days": semana},
            {"title": "Faro em Foco", "start": "18:15", "stop": "18:45", "days": semana},
            {"title": "Exercício e Dor", "start": "18:45", "stop": "19:00", "days": semana},
            {"title": "Grande Auditório", "start": "19:00", "stop": "20:00", "days": semana},
            {"title": "Rua 80", "start": "20:00", "stop": "21:00", "days": semana},
            {"title": "Soluçar dos Esquecidos", "start": "21:00", "stop": "23:00", "days": semana},
            {"title": "Reis do Rock", "start": "23:00", "stop": "00:00", "days": semana},
        ]

    return programas
