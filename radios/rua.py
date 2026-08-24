def get_schedule(config):
    """
    Obtém a programação da RUA FM.
    Como a página da rádio não apresenta horários estruturados,
    cumprimos a directiva de não inventar programação e devolvemos
    um bloco diário contínuo.
    """
    return [
        {
            "title": "Programação não disponível",
            "start": "00:00",
            "stop": "00:00", 
            "days": [0, 1, 2, 3, 4, 5, 6]
        }
    ]
