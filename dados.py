import json
from classes import Vulnerabilidade, Notebook, Servidor, Roteador, Aplicativo

def salvar_arquivos(lista_ativos, caminho_arquivo="arquivoativos.json"):
    try:
        ativos_em_dicionarios = [ativo.retorna_dicionario() for ativo in lista_ativos]
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_lista_de_ativos:
            json.dump(ativos_em_dicionarios, arquivo_lista_de_ativos, indent=4)
            return True
    except OSError:
        print("Não foi possível salvar no arquivo!")
        return False

def carregar_ativos(caminho_arquivo="arquivoativos.json"):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivolista:
            ativos_em_dicionarios = json.load(arquivolista)
            lista_objetos_criados = []

            tipos_de_ativos = {
                "Notebook": Notebook,
                "Servidor": Servidor,
                "Roteador": Roteador,
                "Aplicativo": Aplicativo
            }

            detalhes_de_ativos = {
                "Notebook": "Sistema operacional",
                "Servidor": "Tipo_servidor",
                "Roteador": "Versão Firmware",
                "Aplicativo": "Versão"
            }

            for ativo in ativos_em_dicionarios:
                objeto_criado = None
                detalhe = ativo[detalhes_de_ativos[ativo["Tipo"]]]
                objeto_criado = tipos_de_ativos[ativo["Tipo"]](ativo["Id"], ativo["Nome"], ativo["Responsavel"], ativo["Setor"])
                if detalhe != "Não informado":
                    objeto_criado.adicionar_detalhe(detalhe)

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