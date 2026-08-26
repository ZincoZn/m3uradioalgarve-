import requests
from bs4 import BeautifulSoup
import re

def get_schedule(config):
    """
    Extrai a programação da Rádio Portimão 106.5 FM directamente do site oficial:
    https://www.radioportimao.pt/programacao/
    """
    url = config.get("schedule_url") or "https://www.radioportimao.pt/programacao/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"ERRO ao aceder à página da Rádio Portimão ({url}): {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    texto_pagina = soup.get_text()

    # Identificação das secções na página
    pos_semana = texto_pagina.find("2ª a 6ª FEIRA")
    pos_sabado = texto_pagina.find("SÁBADO")
    pos_domingo = texto_pagina.find("DOMINGO")

    # Caso a estrutura falhe, devolve lista vazia para não corromper o EPG
    if pos_semana == -1 or pos_sabado == -1 or pos_domingo == -1:
        print("ERRO: Não foi possível localizar as secções de dias da semana no HTML da Rádio Portimão.")
        return []

    bloco_semana = texto_pagina[pos_semana:pos_sabado]
    bloco_sabado = texto_pagina[pos_sabado:pos_domingo]
    bloco_domingo = texto_pagina[pos_domingo:]

    def parse_block(texto_bloco, dias):
        # Captura linhas no formato "HH:MM NOME DO PROGRAMA"
        padrao = re.compile(r'(\d{2}:\d{2})\s+([^\n\r]+)')
        matches = padrao.findall(texto_bloco)
        
        programas_dia = []
        for i, (hora_inicio, titulo) in enumerate(matches):
            titulo_limpo = titulo.strip()
            if not titulo_limpo:
                continue

            # A hora de fim é a hora de início do programa seguinte (ou 00:00 se for o último)
            if i + 1 < len(matches):
                hora_fim = matches[i + 1][0]
            else:
                hora_fim = "00:00"

            programas_dia.append({
                "title": titulo_limpo,
                "start": hora_inicio,
                "stop": hora_fim,
                "days": dias
            })
        return programas_dia

    # Mapeamento dos dias (0=Segunda, ..., 6=Domingo)
    programas_semana = parse_block(bloco_semana, [0, 1, 2, 3, 4])
    programas_sabado = parse_block(bloco_sabado, [5])
    programas_domingo = parse_block(bloco_domingo, [6])

    total_programas = programas_semana + programas_sabado + programas_domingo

    if not total_programas:
        print("AVISO: Nenhum programa extraído da página da Rádio Portimão.")
    
    return total_programas
