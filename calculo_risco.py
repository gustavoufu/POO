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

    return lista_cvss
    
def matriz_cves(lista_ativos):
    matriz = []
    cves = cves_unicos(lista_ativos)

    for ativo in lista_ativos:
        vetor_cves_ativo = []
        cves_do_ativo = []

        for vulnerabilidade in ativo.vulnerabilidades:
            cves_do_ativo.append(vulnerabilidade.codigo_cve)

        for cve in cves:
            if cve in cves_do_ativo:
                vetor_cves_ativo.append(1)
            else:
                vetor_cves_ativo.append(0)

        matriz.append(vetor_cves_ativo)

    return matriz

print(matriz_cves(lista_ativos))