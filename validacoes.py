from modelos import VERMELHO, TITULO, NORMAL, TiposDeAtivos, Severidade_Extenso
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
            print(f"Severidade: {Severidade_Extenso(vulnerabilidade.severidade).name}")
            print(f"Status: {vulnerabilidade.status}")
            print()