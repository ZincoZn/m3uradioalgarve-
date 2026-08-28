def get_schedule(config):
    """
    Grelha de salvaguarda estática para a Total FM Algarve.
    A rádio não fornece grelha de programação no site.
    """
    semana = [0, 1, 2, 3, 4, 5, 6]
    
    programas = [
        {"title": "Madrugada Total", "start": "00:00", "stop": "07:00", "days": semana, "category": "Música"},
        {"title": "Manhãs Total FM", "start": "07:00", "stop": "13:00", "days": semana, "category": "Música / Entretenimento"},
        {"title": "Tardes Total FM", "start": "13:00", "stop": "20:00", "days": semana, "category": "Música / Entretenimento"},
        {"title": "Noite Total", "start": "20:00", "stop": "23:59", "days": semana, "category": "Música"},
    ]

    return programas
