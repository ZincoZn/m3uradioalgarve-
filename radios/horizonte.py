import requests
from bs4 import BeautifulSoup
import re

def get_schedule(config):
    """
    Captura a programação da Rádio Horizonte Algarve directamente do site oficial.
    Mapeamento de dias: 0 = Segunda-feira ... 6 = Domingo.
    """
    url = config.get("schedule_url") or "https://www.radiohorizonte.com/pt-pt/programacao"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    programas_dinamicos = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Procura os elementos da grelha na página HTML
            elementos = soup.find_all(['div', 'tr', 'li', 'p'], class_=re.compile(r'(programa|schedule|views-row|item)', re.I))
            
            for elem in elementos:
                texto = elem.get_text(separator=' ', strip=True)
                # Procura padrões de horário (ex: 07:00 - 10:00 Programa X)
                match = re.search(r'(\d{1,2}:\d{2})\s*[-–aA]\s*(\d{1,2}:\d{2})\s+(.+)', texto)
                if match:
                    hora_in, hora_fim, titulo = match.groups()
                    programas_dinamicos.append({
                        "title": titulo.strip(),
                        "start": hora_in.zfill(5),
                        "stop": hora_fim.zfill(5),
                        "days": [0, 1, 2, 3, 4, 5, 6] # Aplica aos dias da semana
                    })
    except Exception as e:
        print(f"AVISO: Não foi possível obter a grelha em tempo real da Rádio Horizonte ({e}).")

    # Se a captura web falhar ou não devolver resultados, utiliza a grelha de salvaguarda
    if not programas_dinamicos:
        schedule = {
            0: [("00:00", "05:00", "Horizonte Dance Factory"), ("05:00", "07:00", "100% Nacional"), ("07:00", "10:00", "A Linha do Horizonte"), ("10:00", "13:00", "As Manhãs da Horizonte"), ("13:00", "20:00", "Horizonte Non Stop"), ("20:00", "21:00", "Soundtrip"), ("21:00", "22:00", "Horizonte Non Stop"), ("22:00", "00:00", "Do outro Lado do FM")],
            1: [("00:00", "01:00", "We Love House Music"), ("01:00", "02:00", "Logic Soul Radio Show"), ("02:00", "05:00", "Horizonte Dance Factory"), ("05:00", "07:00", "100% Nacional"), ("07:00", "10:00", "A Linha do Horizonte"), ("10:00", "13:00", "As Manhãs da Horizonte"), ("13:00", "20:00", "Horizonte Non Stop"), ("20:00", "21:00", "Soundtrip"), ("21:00", "22:00", "Horizonte Non Stop"), ("22:00", "23:00", "Horizonte Dance Factory"), ("23:00", "00:00", "Puro Extenso")],
            2: [("00:00", "01:00", "Urbana Radioshow"), ("01:00", "02:00", "X RadioShow Mayze & Faria"), ("02:00", "03:00", "Soulganster Records"), ("03:00", "05:00", "Horizonte Dance Factory"), ("05:00", "07:00", "100% Nacional"), ("07:00", "10:00", "A Linha do Horizonte"), ("10:00", "13:00", "As Manhãs da Horizonte"), ("13:00", "20:00", "Horizonte Non Stop"), ("20:00", "21:00", "Soundtrip"), ("21:00", "22:00", "Horizonte Non Stop"), ("22:00", "00:00", "Horizonte Dance Factory")],
            3: [("00:00", "01:00", "Infinity Radio Show"), ("01:00", "02:00", "We Love House Music (REP)"), ("02:00", "03:00", "Dance Connection (REP)"), ("03:00", "04:00", "Dance Connection (REP)"), ("04:00", "05:00", "Tanira Recordings Radio Show"), ("05:00", "07:00", "100% Nacional"), ("07:00", "10:00", "A Linha do Horizonte"), ("10:00", "13:00", "As Manhãs da Horizonte"), ("13:00", "20:00", "Horizonte Non Stop"), ("20:00", "21:00", "Soundtrip"), ("21:00", "22:00", "Horizonte Non Stop"), ("22:00", "00:00", "Horizonte Dance Factory")],
            4: [("00:00", "01:00", "Fresh Beats (REP)"), ("01:00", "02:00", "X Radio Show Mayze x Faria"), ("02:00", "03:00", "Cadência Eletrónica"), ("03:00", "04:00", "Soulganster Records"), ("04:00", "05:00", "Cadência Eletrónica (REP)"), ("05:00", "07:00", "100% Nacional"), ("07:00", "10:00", "A Linha do Horizonte"), ("10:00", "13:00", "As Manhãs da Horizonte"), ("13:00", "20:00", "Horizonte Non Stop"), ("20:00", "21:00", "Soundtrip"), ("21:00", "23:00", "Clubbing"), ("23:00", "00:00", "In Stereo")],
            5: [("00:00", "01:00", "Infinity Radio Show (REP)"), ("01:00", "02:00", "Sexysoundsystem"), ("02:00", "04:00", "Clubbing (REP)"), ("04:00", "05:00", "We Love House Music (REP)"), ("05:00", "07:00", "100% Nacional"), ("07:00", "10:00", "A Linha do Horizonte"), ("10:00", "20:00", "Horizonte Non Stop"), ("20:00", "21:00", "Deep & Soul"), ("21:00", "22:00", "DJ Sérgio T Radio Show"), ("22:00", "23:00", "Urbana Radio Show"), ("23:00", "00:00", "Projeto Global")],
            6: [("00:00", "01:00", "Dance Connections"), ("01:00", "02:00", "Dance Connections"), ("02:00", "03:00", "Vibesound Radio Show"), ("03:00", "04:00", "Deep & Soul (REP)"), ("04:00", "05:00", "In Stereo (REP)"), ("05:00", "06:00", "Urbana Radio Show"), ("06:00", "07:00", "100% Nacional"), ("07:00", "10:00", "A Linha do Horizonte"), ("10:00", "21:00", "Horizonte Non Stop"), ("21:00", "22:00", "Dancetaria"), ("22:00", "23:00", "Remember Dance"), ("23:00", "00:00", "Fresh Beats")]
        }

        for dia_semana, lista_progs in schedule.items():
            for start_str, stop_str, titulo in lista_progs:
                programas_dinamicos.append({
                    "title": titulo,
                    "start": start_str,
                    "stop": stop_str,
                    "days": [dia_semana]
                })

    return programas_dinamicos
