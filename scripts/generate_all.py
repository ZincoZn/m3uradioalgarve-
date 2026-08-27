import json
import os
import sys
import datetime
from zoneinfo import ZoneInfo
import importlib
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Ajusta o caminho de execução
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configurações Globais
EPG_DAYS = 7
CONFIG_FILE = "config/radios.json"
OUTPUT_DIR = "output"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/ZincoZn/m3uradioalgarve-/main/output"

def load_radios():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_xmltv_time(date_obj, time_str, timezone_str):
    """Formata a data/hora para o formato XMLTV (YYYYMMDDHHMMSS +ZZZZ)."""
    tz = ZoneInfo(timezone_str)
    hour, minute = map(int, time_str.split(':'))
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
        return False, None

    if not programas_base:
        print(f"ERRO: Nenhum programa encontrado para {radio['name']}. O ficheiro não será substituído.")
        return False, None

    tz = ZoneInfo(radio['timezone'])
    hoje = datetime.datetime.now(tz).date()
    
    programas_xml_str = []
    programas_dados = []
    
    for i in range(EPG_DAYS):
        dia_actual = hoje + datetime.timedelta(days=i)
        dia_semana = dia_actual.weekday()
        
        for prog in programas_base:
            if dia_semana in prog['days']:
                start_str = prog['start']
                stop_str = prog['stop']
                
                dia_fim = dia_actual
                if stop_str <= start_str:
                    dia_fim = dia_actual + datetime.timedelta(days=1)
                
                xml_start = format_xmltv_time(dia_actual, start_str, radio['timezone'])
                xml_stop = format_xmltv_time(dia_fim, stop_str, radio['timezone'])
                
                # Para ficheiro XML individual (string)
                programas_xml_str.append(f"""
    <programme start="{xml_start}" stop="{xml_stop}" channel="{radio['id']}">
        <title lang="{radio['language']}">{prog['title']}</title>
    </programme>""")
                
                # Para o ficheiro unificado
                programas_dados.append({
                    "start": xml_start,
                    "stop": xml_stop,
                    "title": prog['title']
                })

    if not programas_dados:
        print(f"ERRO: A grelha gerada está vazia para {radio['name']}. Ficheiro intocado.")
        return False, None
        
    # Escreve o ficheiro XMLTV Individual da rádio
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="Radio EPG GitHub" generator-info-url="https://github.com/">
    <channel id="{radio['id']}">
        <display-name>{radio['name']}</display-name>
        <icon src="{radio['logo']}"/>
    </channel>
{''.join(programas_xml_str)}
</tv>"""

    xml_path = os.path.join(OUTPUT_DIR, f"{radio['module']}.xml")
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
        
    # Escreve o ficheiro M3U Individual
    m3u_path = os.path.join(OUTPUT_DIR, f"{radio['module']}.m3u")
    xml_url = f"{GITHUB_RAW_BASE}/{radio['module']}.xml"
    m3u_content = f"""#EXTM3U x-tvg-url="{xml_url}"
#EXTVLCOPT:http-user-agent="Radio-EPG-Kodi/1.0"
#EXTINF:-1 tvg-id="{radio['id']}" tvg-name="{radio['name']}" tvg-logo="{radio['logo']}" is-radio="true" group-title="{radio['group']}",{radio['name']}
{radio['stream']}"""

    with open(m3u_path, 'w', encoding='utf-8') as f:
        f.write(m3u_content)
        
    m3u_entry = f"""#EXTINF:-1 tvg-id="{radio['id']}" tvg-name="{radio['name']}" tvg-logo="{radio['logo']}" is-radio="true" group-title="{radio['group']}",{radio['name']}
{radio['stream']}"""

    print(f"SUCESSO: Ficheiros gerados para {radio['name']} ({len(programas_dados)} programas inseridos).")
    
    dados_radio = {
        "id": radio['id'],
        "name": radio['name'],
        "logo": radio['logo'],
        "language": radio['language'],
        "programmes": programas_dados,
        "m3u_entry": m3u_entry
    }
    
    return True, dados_radio

def generate_combined_xmltv(all_radios_data, output_path):
    """Gera o ficheiro epg_todas.xml combinando todos os canais e programas num único XMLTV."""
    root = ET.Element("tv", {
        "generator-info-name": "Radio EPG Geral",
        "generator-info-url": "https://github.com/ZincoZn/m3uradioalgarve-"
    })

    # Adiciona todos os canais
    for r in all_radios_data:
        channel = ET.SubElement(root, "channel", {"id": r['id']})
        ET.SubElement(channel, "display-name").text = r['name']
        if r['logo']:
            ET.SubElement(channel, "icon", {"src": r['logo']})

    # Adiciona todos os programas
    for r in all_radios_data:
        for prog in r['programmes']:
            programme = ET.SubElement(root, "programme", {
                "start": prog['start'],
                "stop": prog['stop'],
                "channel": r['id']
            })
            ET.SubElement(programme, "title", {"lang": r['language']}).text = prog['title']

    rough_string = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8")

    with open(output_path, "wb") as f:
        f.write(pretty_xml)
        
    print(f"\nSUCESSO: Ficheiro unificado '{output_path}' gerado com sucesso.")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    radios = load_radios()
    sucesso_total = True
    
    all_radios_data = []
    
    for radio in radios:
        sucesso, dados = generate_epg_for_radio(radio)
        if sucesso:
            all_radios_data.append(dados)
        else:
            sucesso_total = False
            
    if all_radios_data:
        # 1. Gera o XMLTV único para o Kodi
        combined_xml_path = os.path.join(OUTPUT_DIR, "epg_todas.xml")
        generate_combined_xmltv(all_radios_data, combined_xml_path)
        
        # 2. Gera a M3U Geral apontando para o XMLTV único
        combined_xml_url = f"{GITHUB_RAW_BASE}/epg_todas.xml"
        m3u_entries = [r['m3u_entry'] for r in all_radios_data]
        
        m3u_geral_content = f'#EXTM3U x-tvg-url="{combined_xml_url}"\n#EXTVLCOPT:http-user-agent="Radio-EPG-Kodi/1.0"\n' + "\n".join(m3u_entries)
        
        m3u_geral_path = os.path.join(OUTPUT_DIR, "radios_todas.m3u")
        with open(m3u_geral_path, 'w', encoding='utf-8') as f:
            f.write(m3u_geral_content)
            
        print("SUCESSO: Ficheiro 'radios_todas.m3u' gerado com apontamento unificado.")

    if not sucesso_total:
        print("\nAVISO: Uma ou mais rádios falharam a actualização.")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
