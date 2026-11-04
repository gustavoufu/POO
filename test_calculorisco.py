import numpy as np  
import json
from classes import Notebook, Vulnerabilidade
from calculo_risco import calculo_risco_proprio, matriz_dependencias, calculo_risco_efetivo

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

    resultado = list(resultado)

    assert resultado == [10, 5]

def test_criar_matriz_dependencia():
    
    notebook1 = Notebook(
        5,
        "Vitoria1",
        "Gustavo",
        "Setor TI",
        "Win10"        
    )

    notebook1.adicionar_dependencia(
        10,
        0.5
    )

    notebook2 = Notebook(
        10,
        "Vitoria",
        "degusta",
        "Setor TI",
        "Win10"        
    )

    vulnerabilidade_teste = Vulnerabilidade(
        "Vitoria virus",
        "virus brabo",
        "teste",
        10,
        "aberto",
        "CVE-2026-0004"
        )
    
    notebook2.adicionar_vulnerabilidade(vulnerabilidade_teste)

    lista_de_ativos = [notebook1, notebook2]

    resultado = (matriz_dependencias(lista_de_ativos))

    resultado_lista = resultado.tolist()

    assert resultado_lista == [[0, 0.5], [0, 0]]

def test_risco_efetivo():
    
    notebook1 = Notebook(
        1,
        "Vitoria1",
        "Gustavo",
        "Setor TI",
        "Win10"        
    )

    vulnerabilidade_teste1 = Vulnerabilidade(
        "Vitoria virus1",
        "virus brabo",
        "teste",
        5,
        "aberto",
        "CVE-2026-0001"
        )

    notebook1.adicionar_dependencia(
        2,
        0.5
    )

    notebook2 = Notebook(
        2,
        "Vitoria",
        "degusta",
        "Setor TI",
        "Win10"        
    )

    vulnerabilidade_teste2 = Vulnerabilidade(
        "Vitoria virus2",
        "virus brabo",
        "teste",
        10,
        "aberto",
        "CVE-2026-0002"
        )
    
    notebook1.adicionar_vulnerabilidade(vulnerabilidade_teste1)
    notebook2.adicionar_vulnerabilidade(vulnerabilidade_teste2)

    lista_de_ativos = [notebook1, notebook2]

    resultado = (calculo_risco_efetivo(lista_de_ativos))

    resultado_lista = resultado.tolist()

    assert resultado_lista == [10, 10]

def test_risco_efeito_condicao_infinito():
        
    matriz = np.array([
    [1, 2],
    [2, 4]
    ])
    
    numero_condicao = np.linalg.cond(matriz)

    if not np.isfinite(numero_condicao) or numero_condicao > 1e12:
        return None

    resultado = "É estável"

    assert resultado == None

def test_matriz_mal_condicionada():
    
    matriz = np.array([
    [1, 0.999999999999],
    [0.99999999999999, 1]
    ])
    
    numero_condicao = np.linalg.cond(matriz)

    if not np.isfinite(numero_condicao) or numero_condicao > 1e12:
        return None

    resultado = "É estável"
    print(resultado)

    assert resultado == None


def test_testar_persistencia(tmp_path):

    arquivo = tmp_path / "persistencia_teste"

    notebook_teste = Notebook(5, "persistencia_teste", "Gustavinho", "TI", "linux")

    notebook_em_dicionario = notebook_teste.retorna_dicionario()

    notebook_em_json = json.dumps(notebook_em_dicionario)

    arquivo.write_text(notebook_em_json)

    arquivo_lido = arquivo.read_text()

    assert notebook_em_json == arquivo_lido