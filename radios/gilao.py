import requests
from bs4 import BeautifulSoup
import re

def get_schedule(config):
    """
    Captura a programação da Rádio Gilão directamente do site oficial.
    Mapeamento de dias: 0 = Segunda-feira ... 6 = Domingo.
    """
    url = config.get("schedule_url") or "https://www.radiogilao.com/index.php/programacao.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    programas = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            texto_pagina = soup.get_text(separator=" ")

            # 1ª Tentativa: Procura blocos com intervalos (ex: 08:00 - 10:00 ou 08h00 as 10h00)
            padrao_intervalo = re.compile(r'(\d{2}[:h]\d{2})\s*(?:-|_|a|às)?\s*(\d{2}[:h]\d{2})\s+(.*?)(?=\d{2}[:h]\d{2}|$)', re.IGNORECASE)
            matches_intervalo = padrao_intervalo.findall(texto_pagina)

            if matches_intervalo:
                for match in matches_intervalo:
                    hora_in = match[0].replace('h', ':').strip()
                    hora_fim = match[1].replace('h', ':').strip()
                    titulo = match[2].strip()
                    
                    if titulo:
                        programas.append({
                            "title": titulo,
                            "start": hora_in.zfill(5),
                            "stop": hora_fim.zfill(5),
                            "days": [0, 1, 2, 3, 4, 5, 6]
                        })
            else:
                # 2ª Tentativa: Procura formato simples (ex: 08:00 Titulo)
                padrao_simples = re.compile(r'(\d{2}[:h]\d{2})\s+(.*?)(?=\d{2}[:h]\d{2}|$)')
                matches_simples = padrao_simples.findall(texto_pagina)
                for i, (hora_inicio, titulo) in enumerate(matches_simples):
                    titulo_limpo = titulo.strip()
                    if not titulo_limpo:
                        continue
                    hora_in = hora_inicio.replace('h', ':').strip()
                    hora_fim = matches_simples[i + 1][0].replace('h', ':').strip() if i + 1 < len(matches_simples) else "00:00"
                    programas.append({
                        "title": titulo_limpo,
                        "start": hora_in.zfill(5),
                        "stop": hora_fim.zfill(5),
                        "days": [0, 1, 2, 3, 4, 5, 6]
                    })
    except Exception as e:
        print(f"AVISO: Não foi possível obter a grelha da Rádio Gilão ({e}). A aplicar salvaguarda.")

    # Grelha de salvaguarda caso a extracção falhe
    if not programas:
        programas = [
            {"title": "Madrugada Gilão", "start": "00:00", "stop": "07:00", "days": [0, 1, 2, 3, 4, 5, 6]},
            {"title": "Manhãs da Gilão", "start": "07:00", "stop": "13:00", "days": [0, 1, 2, 3, 4, 5, 6]},
            {"title": "Tardes da Gilão", "start": "13:00", "stop": "20:00", "days": [0, 1, 2, 3, 4, 5, 6]},
            {"title": "Noite Gilão", "start": "20:00", "stop": "00:00", "days": [0, 1, 2, 3, 4, 5, 6]},
        ]

    return programas
