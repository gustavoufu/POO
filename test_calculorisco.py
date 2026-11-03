import numpy as np  

from classes import Notebook, Vulnerabilidade
from calculo_risco import calculo_risco_proprio

def test_calculo_risco_proprio():
    notebook = Notebook(
        "01",
        "Gustavo pc",
        "Gustavo responsa",
        "Setor teste",
        "Win11"
    )

    vulnerabilidade = Vulnerabilidade(
        "Vulnerabilidade test",
        "Descricao teste",
        "categoria teste",
        10,
        "aberto",
        "CVE-2026-0001"
    )

    notebook.adicionar_vulnerabilidade(vulnerabilidade)

    resultado = calculo_risco_proprio([notebook])

    assert resultado[0] == 10

def test_calculo_risco_proprio_2_ativos():
    notebook1 = Notebook(
        "1",
        "Gustavo pc",
        "Gustavo responsa",
        "Setor teste",
        "Win11"
    )

    vulnerabilidade1 = Vulnerabilidade(
        "Vulnerabilidade test",
        "Descricao teste",
        "categoria teste",
        10,
        "aberto",
        "CVE-2026-0001"
    )

    notebook2 = Notebook(
        "2",
        "Gustavo pcc",
        "Gustavo responsa",
        "Setor teste",
        "Win11"
    )

    vulnerabilidade2 = Vulnerabilidade(
        "Vulnerabilidade teste 2",
        "Descricao teste",
        "categoria teste",
        5,
        "aberto",
        "CVE-2026-0002"
    )

    notebook1.adicionar_vulnerabilidade(vulnerabilidade1)
    notebook2.adicionar_vulnerabilidade(vulnerabilidade2)

    lista_de_ativos = [notebook1, notebook2]

    resultado = calculo_risco_proprio(lista_de_ativos)

    print(notebook1.nome)
    print(notebook2.nome)
    print(resultado)

    resultado = list(resultado)

    assert resultado == [10, 5]