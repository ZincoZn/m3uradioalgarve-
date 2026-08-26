import requests
from bs4 import BeautifulSoup

def get_schedule(config):
    """
    Programação da Rádio Horizonte Algarve.
    Dias: 0 = 2ª feira, ..., 6 = Domingo.
    """
    semana_dias = [0, 1, 2, 3, 4]

    # Grelha de Segunda a Sexta-feira
    semana = [
        {"title": "Madrugada Horizonte", "start": "00:00", "stop": "07:00", "days": semana_dias},
        {"title": "Manhãs da Horizonte", "start": "07:00", "stop": "10:00", "days": semana_dias},
        {"title": "Manhãs com Informação", "start": "10:00", "stop": "13:00", "days": semana_dias},
        {"title": "Edição de Informação Regional", "start": "13:00", "stop": "14:00", "days": semana_dias},
        {"title": "Tardes de Horizonte", "start": "14:00", "stop": "18:00", "days": semana_dias},
        {"title": "Regresso a Casa / Informação", "start": "18:00", "stop": "20:00", "days": semana_dias},
        {"title": "Noites da Horizonte", "start": "20:00", "stop": "00:00", "days": semana_dias},
    ]

    # Grelha de Sábado e Domingo
    fim_de_semana = [
        {"title": "Madrugada Horizonte", "start": "00:00", "stop": "08:00", "days": [5, 6]},
        {"title": "Manhãs de Fim de Semana", "start": "08:00", "stop": "13:00", "days": [5, 6]},
        {"title": "Informação Regional", "start": "13:00", "stop": "14:00", "days": [5, 6]},
        {"title": "Tardes de Fim de Semana / Desporto", "start": "14:00", "stop": "20:00", "days": [5, 6]},
        {"title": "Noites de Fim de Semana", "start": "20:00", "stop": "00:00", "days": [5, 6]},
    ]

    return semana + fim_de_semana

