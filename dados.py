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

            configuracoes_ativos = {
                "Notebook": {
                    "classe": Notebook,
                    "detalhe": "Sistema operacional"
                },
                "Servidor": {
                    "classe": Servidor,
                    "detalhe": "Tipo_servidor"
                },
                "Roteador": {
                    "classe": Roteador,
                    "detalhe": "Versão Firmware"
                },
                "Aplicativo": {
                    "classe": Aplicativo,
                    "detalhe": "Versão"
                },
            }

            for ativo in ativos_em_dicionarios:
                detalhe_do_ativo = ativo[configuracoes_ativos[ativo["Tipo"]]["detalhe"]]
                classe_do_ativo = configuracoes_ativos[ativo["Tipo"]]["classe"]

                objeto_criado = classe_do_ativo(ativo["Id"], ativo["Nome"], ativo["Responsavel"], ativo["Setor"])
                if detalhe_do_ativo != "Não informado":
                    objeto_criado.adicionar_detalhe(detalhe_do_ativo)

                for vulne in ativo["Vulnerabilidades"]:
                    vulne_nova = Vulnerabilidade(vulne["Nome"], vulne["Descrição"], vulne["Categoria"], vulne["Severidade"], vulne["Status"], vulne["CVE"])
                    objeto_criado.adicionar_vulnerabilidade(vulne_nova)

                for dependencia in ativo.get("Dependencias", []):
                    objeto_criado.adicionar_dependencia(dependencia["AtivoIdBaseRisco"], dependencia["Fator"])

                lista_objetos_criados.append(objeto_criado)
            return lista_objetos_criados

    except (FileNotFoundError, json.JSONDecodeError):
        return []