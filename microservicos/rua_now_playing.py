import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime

def fetch_now_playing():
    url = "https://rua.pt/rds/rds.xml"
    headers = {"User-Agent": "RUA-FM-API/1.0"}
    
    try:
        # Pede o ficheiro à rádio
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        # Força a descodificação em ISO-8859-1 antes de qualquer tratamento
        xml_data = response.content.decode('iso-8859-1')
        
        # Processa o XML
        root = ET.fromstring(xml_data)
        
        def safe_text(element, tag):
            node = element.find(tag)
            return node.text.strip() if node is not None and node.text else ""

        # Bloco On Air
        onair = root.find("Onair")
        artist = safe_text(onair, "OnairArtist")
        title = safe_text(onair, "OnairTitle")
        program = safe_text(onair, "OnairSchemeName")

        # Bloco Last
        last = root.find("Last")
        last_artist = safe_text(last, "LastArtist")
        last_title = safe_text(last, "LastTitle")

        # Bloco Next
        next_block = root.find("Next")
        next_artist = safe_text(next_block, "NextArtist")
        next_title = safe_text(next_block, "NextTitle")
        next_program = safe_text(next_block, "NextSchemeName")

        timestamp = root.attrib.get("currentTime", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Constrói o JSON
        data = {
            "station": "RUA FM",
            "artist": artist,
            "title": title,
            "now_playing": f"{artist} - {title}" if artist and title else program,
            "program": program,
            "last": {
                "artist": last_artist,
                "title": last_title
            },
            "next": {
                "artist": next_artist,
                "title": next_title,
                "program": next_program
            },
            "updated": timestamp
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)

    except Exception as e:
        # Devolve um JSON estruturado mesmo em caso de falha da rádio
        erro_json = {
            "station": "RUA FM",
            "now_playing": "Emissão RUA FM",
            "error": str(e)
        }
        return json.dumps(erro_json, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print(fetch_now_playing())
