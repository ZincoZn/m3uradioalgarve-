import requests
from bs4 import BeautifulSoup
import re

def get_schedule(config):
    """
    Captura a programação da Rádio Portimão 106.5 FM directamente do site oficial.
    Se o site estiver inacessível ou falhar, utiliza a grelha de salvaguarda detalhada.
    Mapeamento de dias: 0 = Segunda-feira ... 6 = Domingo.
    """
    url = config.get("schedule_url") or "https://www.radioportimao.pt/programacao/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    programas = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            texto_pagina = soup.get_text(separator=" ")

            pos_semana = texto_pagina.find("2ª a 6ª FEIRA")
            pos_sabado = texto_pagina.find("SÁBADO")
            pos_domingo = texto_pagina.find("DOMINGO")

            if pos_semana != -1 and pos_sabado != -1 and pos_domingo != -1:
                bloco_semana = texto_pagina[pos_semana:pos_sabado]
                bloco_sabado = texto_pagina[pos_sabado:pos_domingo]
                bloco_domingo = texto_pagina[pos_domingo:]

                def parse_block(texto_bloco, dias):
                    # Procura padrões "HH:MM Titulo" parando antes da hora seguinte ou fim do bloco
                    padrao = re.compile(r'(\d{2}:\d{2})\s+(.*?)(?=\d{2}:\d{2}|SÁBADO|DOMINGO|2ª|$)')
                    matches = padrao.findall(texto_bloco)
                    progs = []
                    for i, (hora_inicio, titulo) in enumerate(matches):
                        titulo_limpo = titulo.strip()
                        # Remove palavras de controlo que possam ser capturadas no final do bloco
                        titulo_limpo = re.sub(r'\s+(SÁBADO|DOMINGO|2ª a 6ª FEIRA).*$', '', titulo_limpo, flags=re.IGNORECASE).strip()
                        if not titulo_limpo:
                            continue
                        hora_fim = matches[i + 1][0] if i + 1 < len(matches) else "00:00"
                        progs.append({
                            "title": titulo_limpo,
                            "start": hora_inicio,
                            "stop": hora_fim,
                            "days": dias
                        })
                    return progs

                programas.extend(parse_block(bloco_semana, [0, 1, 2, 3, 4]))
                programas.extend(parse_block(bloco_sabado, [5]))
                programas.extend(parse_block(bloco_domingo, [6]))
    except Exception as e:
        print(f"AVISO: Não foi possível obter a grelha em tempo real da Rádio Portimão ({e}). A usar grelha de salvaguarda.")

    # Grelha de salvaguarda caso a captura web falhe ou não devolva dados
    if not programas:
        semana_dias = [0, 1, 2, 3, 4]
        semana = [
            {"title": "PLAYLIST OLP POP", "start": "00:00", "stop": "05:00", "days": semana_dias},
            {"title": "MÚSICA NO CORAÇÃO", "start": "05:00", "stop": "08:00", "days": semana_dias},
            {"title": "INFORMAÇÃO", "start": "08:00", "stop": "08:30", "days": semana_dias},
            {"title": "PRAZERES INTERROMPIDOS", "start": "08:30", "stop": "10:00", "days": [1, 3]},
            {"title": "CAFÉ & COMPANHIA", "start": "10:00", "stop": "12:30", "days": semana_dias},
            {"title": "PARODIANTES DE LISBOA", "start": "12:30", "stop": "13:00", "days": semana_dias},
            {"title": "INTERVALO", "start": "13:00", "stop": "14:00", "days": semana_dias},
            {"title": "INFORMAÇÃO / ESPAÇO REGIONAL", "start": "14:00", "stop": "15:00", "days": semana_dias},
            {"title": "PROGRAMAÇÃO DA TARDE", "start": "15:00", "stop": "17:00", "days": semana_dias},
            {"title": "HORA DO BRASIL / FADO", "start": "17:00", "stop": "18:00", "days": semana_dias},
            {"title": "SUPER KIZOMBA", "start": "18:00", "stop": "19:00", "days": semana_dias},
            {"title": "INFORMAÇÃO", "start": "19:00", "stop": "19:05", "days": semana_dias},
            {"title": "ANOS 80/90", "start": "19:05", "stop": "19:30", "days": semana_dias},
            {"title": "PARODIANTES DE LISBOA", "start": "19:30", "stop": "20:00", "days": semana_dias},
            {"title": "PROGRAMAÇÃO NOCTURNA", "start": "20:00", "stop": "00:00", "days": semana_dias},
        ]
        sabado = [
            {"title": "CASSETRO IN THE MIX", "start": "00:00", "stop": "01:00", "days": [5]},
            {"title": "PLAYLIST POP E OLD POP", "start": "01:00", "stop": "05:00", "days": [5]},
            {"title": "MÚSICA NO CORAÇÃO", "start": "05:00", "stop": "08:00", "days": [5]},
            {"title": "NOTÍCIAS", "start": "08:00", "stop": "08:30", "days": [5]},
            {"title": "PRAZERES INTERROMPIDOS", "start": "08:30", "stop": "10:00", "days": [5]},
            {"title": "CLUBE MHz", "start": "10:00", "stop": "12:06", "days": [5]},
            {"title": "REFLEXÕES", "start": "12:06", "stop": "12:15", "days": [5]},
            {"title": "OS DIAS DA HISTÓRIA", "start": "12:15", "stop": "12:40", "days": [5]},
            {"title": "AS CRÓNICAS DA ISABEL", "start": "12:40", "stop": "14:00", "days": [5]},
            {"title": "NOTÍCIAS", "start": "14:00", "stop": "15:00", "days": [5]},
            {"title": "AB PLAY", "start": "15:00", "stop": "17:00", "days": [5]},
            {"title": "HORA DO BRASIL", "start": "17:00", "stop": "18:00", "days": [5]},
            {"title": "TOP 10 KIZOMBA", "start": "18:00", "stop": "19:00", "days": [5]},
            {"title": "NOTÍCIAS", "start": "19:00", "stop": "19:10", "days": [5]},
            {"title": "ANOS 80/90", "start": "19:10", "stop": "20:00", "days": [5]},
            {"title": "UM CERTO ORIENTE", "start": "20:00", "stop": "21:00", "days": [5]},
            {"title": "CONVERSAS À MESA / ESPAÇO CULTURAL", "start": "21:00", "stop": "23:00", "days": [5]},
            {"title": "A QUEDA DOS ANJOS", "start": "23:00", "stop": "00:00", "days": [5]},
        ]
        domingo = [
            {"title": "DJ ULISSE DAPA", "start": "00:00", "stop": "01:00", "days": [6]},
            {"title": "MÚSICA NO CORAÇÃO", "start": "01:00", "stop": "07:00", "days": [6]},
            {"title": "DELAY", "start": "07:00", "stop": "08:00", "days": [6]},
            {"title": "NOTÍCIAS", "start": "08:00", "stop": "09:00", "days": [6]},
            {"title": "OS REIS DO ROCK", "start": "09:00", "stop": "12:06", "days": [6]},
            {"title": "REFLEXÕES", "start": "12:06", "stop": "12:30", "days": [6]},
            {"title": "ALMANAQUE", "start": "12:30", "stop": "12:40", "days": [6]},
            {"title": "AS CRÓNICAS DA ISABEL", "start": "12:40", "stop": "13:00", "days": [6]},
            {"title": "POP NACIONAL", "start": "13:00", "stop": "14:00", "days": [6]},
            {"title": "NOTÍCIAS", "start": "14:00", "stop": "15:00", "days": [6]},
            {"title": "PURO EXTENSO", "start": "15:00", "stop": "16:15", "days": [6]},
            {"title": "COMPACT MUSIC", "start": "16:15", "stop": "17:00", "days": [6]},
            {"title": "HORA DO BRASIL", "start": "17:00", "stop": "18:00", "days": [6]},
            {"title": "PISTA DE DANÇA KIZOMBA", "start": "18:00", "stop": "19:00", "days": [6]},
            {"title": "NOTÍCIAS / ANOS 80/90", "start": "19:00", "stop": "20:00", "days": [6]},
            {"title": "LUSITANIA EXPRESSO", "start": "20:00", "stop": "00:00", "days": [6]},
        ]
        programas = semana + sabado + domingo

    return programas
