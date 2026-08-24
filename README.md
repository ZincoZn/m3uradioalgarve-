# Radio EPG GitHub - Solução M3U + XMLTV

Este projecto gera automaticamente ficheiros M3U e XMLTV compatíveis com o Kodi, destinados a rádios portuguesas. Preserva o stream original da rádio para garantir que os metadados dinâmicos (ICY) relativos aos artistas e músicas sejam lidos directamente pelo leitor.

## Objectivo
A automatização recolhe a programação (horários e programas) dos sites oficiais das rádios e constrói uma grelha electrónica contínua (EPG), associando devidamente o identificador `tvg-id`.

## Funcionamento
O script central (`scripts/generate_all.py`) executa as seguintes acções para cada rádio definida no `config/radios.json`:
1. Inicializa o módulo de extracção específico (ex: `kissfm.py`).
2. Valida a existência de programas.
3. Calcula 7 dias de programação futura, respeitando o fuso horário (ex: `Europe/Lisbon`).
4. Compila os ficheiros `output/*.xml` e `output/*.m3u`.

## Instalação e Teste Local
1. Instalar as dependências: `pip install -r requirements.txt`
2. Executar o gerador: `python scripts/generate_all.py`

## Utilização no Kodi
Adicione a lista M3U (através do link "Raw" do GitHub) no PVR IPTV Simple Client. O ficheiro M3U possui internamente a etiqueta `x-tvg-url` para invocar o EPG de forma automática. Substitua a palavra `UTILIZADOR` e `REPOSITORIO` no script pelas suas credenciais reais.
