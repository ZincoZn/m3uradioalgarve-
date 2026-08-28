def get_schedule(config):
    """
    Grelha de salvaguarda estática para a Rádio Vicentina FM.
    A rádio não fornece grelha de programação no site.
    """
    semana = [0, 1, 2, 3, 4, 5, 6]
    
    programas = [
        {"title": "Madrugada Vicentina", "start": "00:00", "stop": "07:00", "days": semana, "category": "Música"},
        {"title": "Manhãs Vicentina FM", "start": "07:00", "stop": "13:00", "days": semana, "category": "Música / Entretenimento"},
        {"title": "Tardes Vicentina", "start": "13:00", "stop": "20:00", "days": semana, "category": "Música / Entretenimento"},
        {"title": "Noites Vicentina FM", "start": "20:00", "stop": "23:59", "days": semana, "category": "Música"},
    ]

    return programas
