from dados import salvar_arquivos, carregar_ativos
from classes import Aplicativo, Notebook, Roteador, Servidor, Vulnerabilidade
from calculo_risco import (
    calculo_risco_efetivo,
    calculo_risco_proprio,
    matriz_dependencias,
)


def test_calculo_risco_proprio():
    notebook = Notebook("01", "Teste", "Gustavo", "Setor teste")
    notebook.adicionar_detalhe("Windows 11")

    vulnerabilidade = Vulnerabilidade(
        "Teste",
        "Descricao-Teste",
        "Categoria-Teste",
        10,
        "Aberto",
        "CVE-2026-0001",
    )

    notebook.adicionar_vulnerabilidade(vulnerabilidade)

    resultado = calculo_risco_proprio([notebook])

    assert resultado[0] == 10


def test_calculo_risco_proprio_2_ativos():
    notebook1 = Notebook("1", "Teste", "Gustavo", "Setor-Teste")
    notebook1.adicionar_detalhe("Win11")

    vulnerabilidade1 = Vulnerabilidade(
        "Teste",
        "Descricao-Teste",
        "Categoria-Teste",
        10,
        "Aberto",
        "CVE-2026-0001",
    )

    notebook2 = Notebook("2", "Teste", "Gustavo", "Setor-Teste")
    notebook2.adicionar_detalhe("Win11")

    vulnerabilidade2 = Vulnerabilidade(
        "Teste",
        "Descricao teste",
        "categoria teste",
        5,
        "aberto",
        "CVE-2026-0002",
    )

    notebook1.adicionar_vulnerabilidade(vulnerabilidade1)
    notebook2.adicionar_vulnerabilidade(vulnerabilidade2)

    lista_de_ativos = [notebook1, notebook2]

    resultado = list(calculo_risco_proprio(lista_de_ativos))

    assert resultado == [10, 5]


def test_criar_matriz_dependencia():
    notebook1 = Notebook(5, "Teste", "Gustavo", "Setor TI")
    notebook1.adicionar_detalhe("Win10")
    notebook1.adicionar_dependencia(10, 0.5)

    notebook2 = Notebook(10, "Teste", "Gustavo", "Setor TI")
    notebook2.adicionar_detalhe("Win10")

    vulnerabilidade_teste = Vulnerabilidade(
        "Teste",
        "virus brabo",
        "teste",
        10,
        "aberto",
        "CVE-2026-0004",
    )

    notebook2.adicionar_vulnerabilidade(vulnerabilidade_teste)

    lista_de_ativos = [notebook1, notebook2]

    resultado_lista = matriz_dependencias(lista_de_ativos).tolist()

    assert resultado_lista == [[0, 0.5], [0, 0]]


def test_risco_efetivo():
    notebook1 = Notebook(1, "Teste", "Gustavo", "Setor TI")
    notebook1.adicionar_detalhe("Win10")

    vulnerabilidade_teste1 = Vulnerabilidade(
        "Teste",
        "virus brabo",
        "teste",
        5,
        "aberto",
        "CVE-2026-0001",
    )

    notebook1.adicionar_dependencia(2, 0.5)

    notebook2 = Notebook(2, "Teste", "Gustavo", "Setor TI")
    notebook2.adicionar_detalhe("Win10")

    vulnerabilidade_teste2 = Vulnerabilidade(
        "Teste",
        "virus brabo",
        "teste",
        10,
        "aberto",
        "CVE-2026-0002",
    )

    notebook1.adicionar_vulnerabilidade(vulnerabilidade_teste1)
    notebook2.adicionar_vulnerabilidade(vulnerabilidade_teste2)

    lista_de_ativos = [notebook1, notebook2]

    resultado_lista = calculo_risco_efetivo(lista_de_ativos).tolist()

    assert resultado_lista == [10, 10]


def test_risco_efetivo_condicao_infinito():
    notebook_1 = Notebook(1, "Teste", "Gustavo", "TI")
    notebook_1.adicionar_detalhe("Windows 11")
    notebook_2 = Notebook(2, "Teste", "Gustavo", "TI")
    notebook_2.adicionar_detalhe("MacOS")

    notebook_1.adicionar_dependencia(2, 1)
    notebook_2.adicionar_dependencia(1, 1)

    lista_ativos = [notebook_1, notebook_2]

    resultado = calculo_risco_efetivo(lista_ativos)

    assert resultado is None


def test_matriz_mal_condicionada():
    notebook_1 = Notebook(1, "Teste", "Gustavo", "TI")
    notebook_1.adicionar_detalhe("Windows 11")
    notebook_2 = Notebook(2, "Teste", "Gustavo", "TI")
    notebook_2.adicionar_detalhe("MacOS")

    notebook_1.adicionar_dependencia(2, 0.9999999999999)
    notebook_2.adicionar_dependencia(1, 0.9999999999999)

    lista_ativos = [notebook_1, notebook_2]

    resultado = calculo_risco_efetivo(lista_ativos)

    assert resultado is None


def test_testar_persistencia(tmp_path):

    caminho_temporario = tmp_path / "ativos_teste.json"

    notebook_1 = Notebook(1, "Notebook", "Gustavo", "TI")
    notebook_1.adicionar_detalhe("Windows 11")

    servidor_2 = Servidor(2, "Servidor", "Gustavo", "TI")
    servidor_2.adicionar_detalhe("Físico")

    roteador_3 = Roteador(3, "Roteador", "Gustavo", "TI")
    roteador_3.adicionar_detalhe("1.0")

    aplicativo_4 = Aplicativo(4, "Aplicativo", "Gustavo", "TI")
    aplicativo_4.adicionar_detalhe("2.0")

    vulnerabilidade = Vulnerabilidade(
        "Teste",
        "Descrição teste",
        "Sistema operacional",
        10,
        "Aberto",
        "CVE-2026-0001",
    )

    notebook_1.adicionar_vulnerabilidade(vulnerabilidade)
    notebook_1.adicionar_dependencia(2, 0.6)

    servidor_2.adicionar_vulnerabilidade(vulnerabilidade)
    servidor_2.adicionar_dependencia(3, 0.4)

    roteador_3.adicionar_vulnerabilidade(vulnerabilidade)
    roteador_3.adicionar_dependencia(4, 0.3)

    aplicativo_4.adicionar_vulnerabilidade(vulnerabilidade)
    aplicativo_4.adicionar_dependencia(1, 0.5)

    lista_ativos = [notebook_1, servidor_2, roteador_3, aplicativo_4]

    ativos_salvos = salvar_arquivos(lista_ativos, caminho_temporario)
    ativos_carregados = carregar_ativos(caminho_temporario)

    dados_originais = [ativo.retorna_dicionario() for ativo in lista_ativos]
    dados_carregados = [ativo.retorna_dicionario() for ativo in ativos_carregados]

    assert ativos_salvos is True
    assert dados_carregados == dados_originais