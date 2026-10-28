from modelos import VERMELHO, TITULO, NORMAL, TiposDeAtivos
from classes import *

def verificar_int(mensagem):
    while True:
        try:
            inteiro = int(input(mensagem))
        except (ValueError, TypeError):
            print(f"{VERMELHO}ERRO, digite um número inteiro válido...{NORMAL}")
            continue
        else:
            return inteiro

def pedir_cvss():
    while True:
        try:
            valor_cvss = float(input("Digite um nível de severidade [0.0 até 10.0]: "))
            if valor_cvss < 0.0 or valor_cvss > 10.0:
                print("Valor inválido. Por favor, insira um número entre 0.0 e 10.0")
                continue
        except (TypeError, ValueError):
            print("ERRO, esse valor não é valido, tente novamente...")
            continue
        else:
            return valor_cvss

def pedir_input(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            print(f"{VERMELHO}ERRO, digite um texto válido...{NORMAL}")
            continue
        else:
            return texto
        
def pedir_severidade():
    while True:
        try:
            severidade = int(input("Digite um nível de severidade [1 até 4]: "))
            if severidade not in range(1, 5):
                print(f"{VERMELHO}O número digitado não é um valor de 1 a 4{NORMAL}")
                continue
        except (ValueError, TypeError):
            print(f"{VERMELHO}ERRO, digite um número inteiro válido...{NORMAL}")
            continue
        else:
            return severidade

def exibir_tipos_de_ativos():
    print("")
    print(f"{TITULO}-=-=-=-=- TIPO DE ATIVOS DISPONÍVEIS -=-=-=-=-{NORMAL}")
    print("")
    for tipo in TiposDeAtivos:
        print(f"{tipo.value} - {tipo.name}")

def pedir_tipo_de_ativo():
    while True:
        try:
            print("")
            tipo = int(input(f"Digite o tipo do ativo [1 até {len(TiposDeAtivos)}]: "))
            if tipo not in range(1, len(TiposDeAtivos) + 1):
                print(f"{VERMELHO}O número digitado não é um valor de 1 a {len(TiposDeAtivos)}{NORMAL}")
                continue
        except (ValueError, TypeError):
            print(f"{VERMELHO}ERRO, digite um número inteiro válido...{NORMAL}")
            continue
        else:
            return tipo

def exibe_vulnerabilidades_ativo(ativo):
    if len(ativo.vulnerabilidades) == 0:
        print("Nenhuma vulnerabilidade cadastrada.")

    else:
        print(f"VULNERABILIDADES: ({len(ativo.vulnerabilidades)})")
        print()
        for posicao, vulnerabilidade in enumerate(ativo.vulnerabilidades, start=1):
            print(f"{posicao}. Vulnerabilidade:")
            print(f"Nome: {vulnerabilidade.nome}")
            print(f"Descrição: {vulnerabilidade.descricao}")
            print(f"Categoria: {vulnerabilidade.categoria}")
            print(f"Status: {vulnerabilidade.status}")
            print(f"CVSS: {vulnerabilidade.severidade}")
            print(f"CVE: {vulnerabilidade.codigo_cve}")

def pedir_fator_dependencia():
    while True:
        try:
            valor_digitado = float(input("Informe o fator de dependência entre 0 e 1: "))
            if 0 <= valor_digitado <= 1:
                return valor_digitado
            else:
                print("Erro, digite um valor entre 0 e 1...")
                continue
        except (ValueError, TypeError):
            print("ERRO, digite um número entre 0 e 1 válido...")

if __name__ == "__main__":
    pedir_fator_dependencia()