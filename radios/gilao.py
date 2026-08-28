import requests
from bs4 import BeautifulSoup
import re

def get_schedule(config):
    """
    Captura a programação da Rádio Gilão através dos separadores Joomla.
    Mapeamento de dias: 0 = Segunda-feira ... 6 = Domingo.
    """
    url = config.get("schedule_url") or "https://www.radiogilao.com/index.php/programacao.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    programas = []

    # Mapeamento do título do separador no HTML para o índice do dia no Kodi
    dias_map = {
        "SEGUNDA": 0,
        "TERÇA": 1,
        "QUARTA": 2,
        "QUINTA": 3,
        "SEXTA": 4,
        "SÁBADO": 5,
        "DOMINGO": 6
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Procura todas as abas de dias da semana (divs com classe jwts_tabbertab)
            separadores_dias = soup.find_all('div', class_='jwts_tabbertab')
            
            for separador in separadores_dias:
                # O título do separador (ex: "SEGUNDA") indica-nos o dia
                nome_dia = separador.get('title', '').strip().upper()
                dia_idx = dias_map.get(nome_dia)
                
                if dia_idx is None:
                    continue
                    
                # Procura a tabela dentro deste dia
                tabela = separador.find('table')
                if not tabela:
                    continue
                    
                linhas = tabela.find_all('tr')
                for linha in linhas:
                    celula = linha.find('td')
                    if celula:
                        texto = celula.get_text(strip=True)
                        # Exemplo do texto a extrair: "00:10H | 06:59H - Madrugadas Rádio - Rádio Gilão"
                        # Este Regex apanha Hora Inicio, Hora Fim e o Título do programa
                        match = re.search(r'(\d{2}:\d{2})H\s*\|\s*(\d{2}:\d{2})H\s*-\s*(.*)', texto)
                        
                        if match:
                            hora_inicio = match.group(1).replace('h', ':')
                            hora_fim = match.group(2).replace('h', ':')
                            titulo_completo = match.group(3).strip()
                            
                            # Limpeza opcional (remove " - Rádio Gilão" ou locutores, para o título ficar mais limpo)
                            titulo = titulo_completo.split('-')[0].strip()
                            locutor = ""
                            if "-" in titulo_completo:
                                locutor = titulo_completo.split('-', 1)[1].strip()
                            
                            prog = {
                                "title": titulo,
                                "start": hora_inicio,
                                "stop": hora_fim,
                                "days": [dia_idx]
                            }
                            
                            # Adiciona o locutor como descrição, se existir
                            if locutor:
                                prog["desc"] = locutor
                                
                            programas.append(prog)

    except Exception as e:
        print(f"AVISO: Não foi possível obter a grelha da Rádio Gilão ({e}). A aplicar salvaguarda.")

    # Se a extracção falhar completamente, aplica uma grelha básica
    if not programas:
        semana = [0, 1, 2, 3, 4, 5, 6]
        programas = [
            {"title": "Madrugadas Rádio", "start": "00:10", "stop": "06:59", "days": semana},
            {"title": "Manhãs Rádio", "start": "07:15", "stop": "13:59", "days": semana},
            {"title": "Tardes Rádio", "start": "14:05", "stop": "19:59", "days": semana},
            {"title": "Noites Rádio", "start": "20:05", "stop": "23:59", "days": semana},
        ]

    return programas

