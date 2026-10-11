from modelos import VERMELHO, TITULO, NORMAL, TiposDeAtivos, Severidade_Extenso

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

def exibe_dados_ativo(ativo):
    print(f"ID: {ativo['id']}")
    print(f"Nome: {ativo['nome']}")
    print(f"Responsável: {ativo['responsavel']}")
    print(f"Setor: {ativo['setor']}")
    print(f"Tipo: {TiposDeAtivos(ativo['tipo']).name}") 

def exibe_vulnerabilidades_ativo(ativo):
    print(f"VULNERABILIDADES: ({len(ativo['vulnerabilidades'])})")
    print()
    for posicao, vulnerabilidade in enumerate(ativo['vulnerabilidades'], start=1):
        print(f"{posicao}. Vulnerabilidade:")
        for chave, valor in vulnerabilidade.items():
            if chave == "severidade":
                print(f"{chave.capitalize()}: {Severidade_Extenso(valor).name}")
            else:
                print(f"{chave.capitalize()}: {valor}")
        print()