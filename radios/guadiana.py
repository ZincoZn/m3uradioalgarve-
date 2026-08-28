import requests
from bs4 import BeautifulSoup
import re

def get_schedule(config):
    """
    Captura a grelha de programação da Rádio Guadiana.
    """
    url = config.get("schedule_url") or "https://www.radioguadiana.pt/index.php?pagina=programacao"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    programas = []
    semana = [0, 1, 2, 3, 4, 5, 6]

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Forçar a leitura correcta da acentuação
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'lxml')
            texto = soup.get_text(separator=" ")
            
            # Procura blocos de hora no formato "08:00 Programa" ou "08h00 as 10h00 Programa"
            padrao = re.compile(r'(\d{2}[:h]\d{2})\s*(?:-|_|a|às|—)?\s*(\d{2}[:h]\d{2})?\s+(.*?)(?=\d{2}[:h]\d{2}|$)')
            matches = padrao.findall(texto)
            
            for i, match in enumerate(matches):
                hora_in = match[0].replace('h', ':').strip()
                hora_fim = match[1].replace('h', ':').strip() if match[1] else ""
                titulo = match[2].strip()
                
                if not titulo or len(titulo) < 3:
                    continue
                
                if not hora_fim:
                    hora_fim = matches[i + 1][0].replace('h', ':').strip() if i + 1 < len(matches) else "23:59"
                    
                programas.append({
                    "title": titulo,
                    "start": hora_in.zfill(5),
                    "stop": hora_fim.zfill(5),
                    "days": semana
                })
    except Exception as e:
        print(f"AVISO: Não foi possível obter a grelha da Rádio Guadiana ({e}). A aplicar salvaguarda.")

    # Grelha de salvaguarda caso o site bloqueie a leitura ou mude de estrutura
    if not programas:
        programas = [
            {"title": "Madrugada Guadiana", "start": "00:00", "stop": "07:00", "days": semana, "category": "Música"},
            {"title": "Manhãs do Guadiana", "start": "07:00", "stop": "13:00", "days": semana, "category": "Entretenimento / Informação"},
            {"title": "Tardes do Guadiana", "start": "13:00", "stop": "20:00", "days": semana, "category": "Entretenimento"},
            {"title": "Noite Guadiana", "start": "20:00", "stop": "23:59", "days": semana, "category": "Música"},
        ]

    return programas
