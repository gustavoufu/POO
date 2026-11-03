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
        "10",
        "aberto",
        "CVE-2026-0001"
    )

    notebook.adicionar_vulnerabilidade(vulnerabilidade)

    resultado = calculo_risco_proprio([notebook])

    assert resultado[0] == 10

def