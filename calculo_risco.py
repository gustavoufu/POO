from dados import carregar_ativos

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
    
def matriz_cves(lista_ativos):
    matriz = []