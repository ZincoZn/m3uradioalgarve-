import json
import os
import sys
import datetime
from zoneinfo import ZoneInfo
import importlib

# O tal código para corrigir o caminho
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configurações Globais
EPG_DAYS = 7
CONFIG_FILE = "config/radios.json"
OUTPUT_DIR = "output"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/UTILIZADOR/REPOSITORIO/main/output"

def load_radios():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_xmltv_time(date_obj, time_str, timezone_str):
    """Formata a data/hora para o formato XMLTV (YYYYMMDDHHMMSS +ZZZZ)."""
    tz = ZoneInfo(timezone_str)
    hour, minute = map(int, time_str.split(':'))
    
    # Cria objecto datetime localizado
    dt = datetime.datetime.combine(date_obj, datetime.time(hour, minute))
    dt_aware = dt.replace(tzinfo=tz)
    
    return dt_aware.strftime("%Y%m%d%H%M%S %z")

def generate_epg_for_radio(radio):
    print(f"\nA processar: {radio['name']}...")
    
    try:
        mod = importlib.import_module(f"radios.{radio['module']}")
        programas_base = mod.get_schedule(radio)
    except Exception as e:
        print(f"ERRO: Falha ao carregar o módulo ou obter dados para {radio['name']}: {e}")
        return False

    if not programas_base:
        print(f"ERRO: Nenhum programa encontrado para {radio['name']}. O ficheiro não será substituído.")
        return False

    tz = ZoneInfo(radio['timezone'])
    hoje = datetime.datetime.now(tz).date()
    
    programas_xml = []
    
    for i in range(EPG_DAYS):
        dia_actual = hoje + datetime.timedelta(days=i)
        dia_semana = dia_actual.weekday()
        
        for prog in programas_base:
            if dia_semana in prog['days']:
                start_str = prog['start']
                stop_str = prog['stop']
                
                # Tratamento de programas que passam da meia-noite
                dia_fim = dia_actual
                if stop_str <= start_str:
                    dia_fim = dia_actual + datetime.timedelta(days=1)
                
                xml_start = format_xmltv_time(dia_actual, start_str, radio['timezone'])
                xml_stop = format_xmltv_time(dia_fim, stop_str, radio['timezone'])
                
                programas_xml.append(f"""
    <programme start="{xml_start}" stop="{xml_stop}" channel="{radio['id']}">
        <title lang="{radio['language']}">{prog['title']}</title>
    </programme>""")

    # Validação Final
    if not programas_xml:
        print(f"ERRO: A grelha gerada está vazia para {radio['name']}. Ficheiro intocado.")
        return False
        
    # Construção do XMLTV
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="Radio EPG GitHub" generator-info-url="https://github.com/">
    <channel id="{radio['id']}">
        <display-name>{radio['name']}</display-name>
        <icon src="{radio['logo']}"/>
    </channel>
{''.join(programas_xml)}
</tv>"""

    # Escrita do ficheiro XML
    xml_path = os.path.join(OUTPUT_DIR, f"{radio['module']}.xml")
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
        
    # Construção e escrita do ficheiro M3U
    m3u_path = os.path.join(OUTPUT_DIR, f"{radio['module']}.m3u")
    xml_url = f"{GITHUB_RAW_BASE}/{radio['module']}.xml"
    
    m3u_content = f"""#EXTM3U x-tvg-url="{xml_url}"
#EXTVLCOPT:http-user-agent="Radio-EPG-Kodi/1.0"
#EXTINF:-1 tvg-id="{radio['id']}" tvg-name="{radio['name']}" tvg-logo="{radio['logo']}" is-radio="true" group-title="{radio['group']}",{radio['name']}
{radio['stream']}"""

    with open(m3u_path, 'w', encoding='utf-8') as f:
        f.write(m3u_content)
        
    print(f"SUCESSO: Ficheiros gerados para {radio['name']} ({len(programas_xml)} programas inseridos).")
    return True

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    radios = load_radios()
    sucesso_total = True
    
    for radio in radios:
        if not generate_epg_for_radio(radio):
            sucesso_total = False
            
    if not sucesso_total:
        print("\nAVISO: Uma ou mais rádios falharam a actualização.")
        sys.exit(1) # Provoca a falha no GitHub Actions para alertar o utilizador
        
if __name__ == "__main__":
    main()
