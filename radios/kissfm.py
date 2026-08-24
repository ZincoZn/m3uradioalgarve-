import requests
from bs4 import BeautifulSoup
import re

def get_schedule(config):
    """
    Obtém a programação da KISS FM Algarve.
    Devolve: list de dicts com 'title', 'start', 'stop', 'days'
    """
    url = config.get("schedule_url")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"ERRO: Não foi possível aceder à programação da KISS FM: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    programas = []
    
    # A lógica procura padrões de texto (ex: 08:00 - 12:00) para garantir robustez
    time_pattern = re.compile(r'(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})')
    
    # Exemplo genérico de extracção baseado no comportamento habitual da KISS FM
    for block in soup.find_all(['div', 'li']):
        text = block.get_text(separator=' ', strip=True)
        match = time_pattern.search(text)
        
        if match:
            start_time = match.group(1)
            end_time = match.group(2)
            
            # Assumimos que o título do programa precede o horário na estrutura HTML
            title_element = block.find(['h2', 'h3', 'strong', 'b'])
            title = title_element.get_text(strip=True) if title_element else "Programa KISS FM"
            
            # Limpeza de título (remover descrições longas)
            title = title.split('-')[0].strip()
            
            # Para a KISS FM, vamos assumir por defeito dias úteis, ou extrair da secção correspondente.
            # Como a estrutura varia, aplica-se uma lógica conservadora para dias úteis (0 a 4).
            dias = [0, 1, 2, 3, 4] 
            
            if "Sunday" in title:
                dias = [6]
            elif "Saturday" in title:
                dias = [5]
                
            programas.append({
                "title": title,
                "start": start_time,
                "stop": end_time,
                "days": dias
            })
            
    return programas
