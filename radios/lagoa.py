def get_schedule(config):
    """
    Grelha de salvaguarda estática para a Rádio Lagoa.
    Como o site está inacessível, devolve blocos fixos de programação.
    Mapeamento de dias: 0 = Segunda-feira ... 6 = Domingo.
    """
    programas = [
        {"title": "Madrugada", "start": "00:00", "stop": "07:00", "days": [0, 1, 2, 3, 4, 5, 6]},
        {"title": "Manhãs da Lagoa", "start": "07:00", "stop": "13:00", "days": [0, 1, 2, 3, 4, 5, 6]},
        {"title": "Tardes da Lagoa", "start": "13:00", "stop": "20:00", "days": [0, 1, 2, 3, 4, 5, 6]},
        {"title": "Noite", "start": "20:00", "stop": "00:00", "days": [0, 1, 2, 3, 4, 5, 6]},
    ]

    return programas
