from dados import carregar_ativos
import numpy as np

lista_ativos = carregar_ativos()

def cves_unicos(lista_ativos):
    cves = []

    for ativo in lista_ativos:
        for vulnerabilidade in ativo.vulnerabilidades:
            if vulnerabilidade.codigo_cve not in cves:
                cves.append(vulnerabilidade.codigo_cve)
    
    return cves

def vetor_cvss(lista_ativos):
    cves = cves_unicos(lista_ativos)
    lista_cvss = []
    lista_de_vulnerabilidades = []

    for ativo in lista_ativos:
        for vulnerabilidade in ativo.vulnerabilidades:
            lista_de_vulnerabilidades.append(vulnerabilidade)

    for cve in cves:
        for vulnerabilidade in lista_de_vulnerabilidades:
            if cve == vulnerabilidade.codigo_cve:
                lista_cvss.append(vulnerabilidade.severidade) 
                break

    return lista_cvss
    
def matriz_incidencia(lista_ativos):
    matriz = []
    cves = cves_unicos(lista_ativos)

    for ativo in lista_ativos:
        vetor_cves_ativo_booleano = []
        cves_do_ativo = []

        for vulnerabilidade in ativo.vulnerabilidades:
            cves_do_ativo.append(vulnerabilidade.codigo_cve)

        for cve in cves:
            if cve in cves_do_ativo:
                vetor_cves_ativo_booleano.append(1)
            else:
                vetor_cves_ativo_booleano.append(0)

        matriz.append(vetor_cves_ativo_booleano)

    return matriz

def calculo_risco_proprio(lista_ativos):
    matriz = matriz_incidencia(lista_ativos)
    vetor = vetor_cvss(lista_ativos)

    m = np.array(matriz)
    v = np.array(vetor, dtype=float)

    b = m @ v

    return b

def exibir_risco_proprio(lista_ativos):
    riscos_proprios = calculo_risco_proprio(lista_ativos)

    for pos, ativo in enumerate(lista_ativos):
        print(f"Ativo: {ativo.nome} - Risco próprio: {riscos_proprios[pos]}")

def matriz_dependencias(lista_ativos):
    qtd_de_ativos = len(lista_ativos)


    matriz = np.zeros((qtd_de_ativos, qtd_de_ativos), dtype=float)

    posicao_por_id = {}
    for posicao, ativo in enumerate(lista_ativos):
        posicao_por_id[ativo.id] = posicao
 
    for ativo in lista_ativos:
        linha = posicao_por_id[ativo.id]
        
        for dependencia in ativo.dependencias:
            id_transmissor = dependencia["AtivoIdBaseRisco"]    
            coluna = posicao_por_id[id_transmissor]
            fator = dependencia["Fator"]
            
            matriz[linha, coluna] = fator

    return matriz

def matriz_identidade(lista_ativos):

    quantidade_ativos = len(lista_ativos)
    matriz_identidade = np.eye(quantidade_ativos, quantidade_ativos)

    return matriz_identidade

def calculo_risco_efetivo(lista_ativos):

    #(I - D):
    I = matriz_identidade(lista_ativos)
    D = matriz_dependencias(lista_ativos)

    A = I - D

    #A @ x = b
    b = calculo_risco_proprio(lista_ativos)

    vetor_risco_total_final = np.linalg.solve(A, b)

    return vetor_risco_total_final