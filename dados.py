import json

def salvar_arquivos(lista_ativos):
    try:
        with open("arquivoativos.json", "w", encoding="utf-8") as arquivolista:
            json.dump(lista_ativos, arquivolista)
            return True
    except OSError:
        print("Não foi possível salvar no arquivo!")
        return False

def carregar_ativos():
    try:
        with open("arquivoativos.json", "r", encoding="utf-8") as arquivolista:
            return json.load(arquivolista)
    except (FileNotFoundError, json.JSONDecodeError):
        return []