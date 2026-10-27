import json
from classes import Vulnerabilidade, Notebook, Servidor, Roteador, Aplicativo

def salvar_arquivos(lista_ativos):
    try:
        ativos_em_dicionarios = [ativo.retorna_dicionario() for ativo in lista_ativos]
        with open("arquivoativos.json", "w", encoding="utf-8") as arquivo_lista_de_ativos:
            json.dump(ativos_em_dicionarios, arquivo_lista_de_ativos, indent=4)
            return True
    except OSError:
        print("Não foi possível salvar no arquivo!")
        return False

def carregar_ativos():
    try:
        with open("arquivoativos.json", "r", encoding="utf-8") as arquivolista:
            ativos_em_dicionarios = json.load(arquivolista)

            lista_objetos_criados = []
            for ativo in ativos_em_dicionarios:
                objeto_criado = None

                if ativo["Tipo"] == "Notebook":
                    objeto_criado = Notebook(ativo["Id"], ativo["Nome"], ativo["Responsavel"], ativo["Setor"], ativo["Sistema operacional"])
                elif ativo["Tipo"] == "Servidor":
                    objeto_criado = Servidor(ativo["Id"], ativo["Nome"], ativo["Responsavel"], ativo["Setor"], ativo["Tipo_servidor"])                
                elif ativo["Tipo"] == "Roteador":
                    objeto_criado = Roteador(ativo["Id"], ativo["Nome"], ativo["Responsavel"], ativo["Setor"], ativo["Versão Firmware"])
                elif ativo["Tipo"] == "Aplicativo":
                    objeto_criado = Aplicativo(ativo["Id"], ativo["Nome"], ativo["Responsavel"], ativo["Setor"], ativo["Versão"])

                if objeto_criado:
                    for vulne in ativo["Vulnerabilidades"]:
                        vulne_nova = Vulnerabilidade(vulne["Nome"], vulne["Descrição"], vulne["Categoria"], vulne["Severidade"], vulne["Status"], vulne["CVE"])
                        objeto_criado.adicionar_vulnerabilidade(vulne_nova)

                    for dependencia in ativo.get("Dependencias", []):
                        objeto_criado.adicionar_dependencia(dependencia["AtivoIdBaseRisco"], dependencia["Fator"])

                    lista_objetos_criados.append(objeto_criado)
            return lista_objetos_criados

    except (FileNotFoundError, json.JSONDecodeError):
        return []