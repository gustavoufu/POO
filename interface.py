import os

def selecionar_opcao_menu():
    opcoes = [
        {"name": "1 - Cadastrar Ativo", "value": 1},
        {"name": "2 - Cadastrar Vulnerabilidade", "value": 2},
        {"name": "3 - Listar Ativos", "value": 3},
        {"name": "4 - Consultar Ativo", "value": 4},
        {"name": "5 - Atualizar Ativo", "value": 5},
        {"name": "6 - Remover Ativo", "value": 6},
        {"name": "7 - Mostrar Riscos", "value": 7},
        {"name": "8 - Cadastrar Dependências", "value": 8},
        {"name": "9 - Remover Dependência", "value": 9},
        {"name": "10 - Sair", "value": 10},
    ]
    return escolher_opcao("GERENCIAMENTO DE ATIVOS", opcoes)

def escolher_opcao(mensagem, escolhas, titulo=None):
    opcoes_validas = [escolha for escolha in escolhas if isinstance(escolha, dict)]

    print(mensagem)
    print()
    for posicao, escolha in enumerate(opcoes_validas, start=1):
        print(f"{posicao}. {escolha['name']}")
    print()

    while True:
        resposta = input("Digite o número da opção: ").strip()
        try:
            numero = int(resposta)
        except ValueError:
            print("Digite um número válido.")
            continue

        if 1 <= numero <= len(opcoes_validas):
            return opcoes_validas[numero - 1]["value"]
        print("Essa opção não está disponível.")

def limpar_terminal():
    print("\033[2J\033[H", end="", flush=True)

def imprimir_titulo(titulo, tamanho=55):
    prefixo = f"── {titulo.upper()} "
    print(prefixo + "─" * max(0, tamanho - len(prefixo)))

if __name__ == "__main__":
    print(selecionar_opcao_menu())
    