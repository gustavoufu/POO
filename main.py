from modelos import VERDE, VERMELHO, NORMAL
from operacoes import (
    cadastrar_ativo,
    cadastrar_vulnerabilidade,
    listar_ativos,
    consultar_ativo,
    atualizar_ativo,
    remover_ativo,
    mostrar_menu)
from dados import carregar_ativos
from validacoes import verificar_int

lista_ativos = carregar_ativos()

opcoes = {
    1:cadastrar_ativo,
    2:cadastrar_vulnerabilidade,
    3:listar_ativos,
    4:consultar_ativo,
    5:atualizar_ativo,
    6:remover_ativo
}

while True:

    mostrar_menu()
    opcao = verificar_int("Escolha uma opção: ")

    if opcao == 7:
        print()
        print(f"{VERDE}Saindo do sistema. Até logo!{NORMAL}")
        break
            
    elif opcao not in opcoes:
        print()
        print(f"{VERMELHO}ERRO: Essa opção não está disponível...{NORMAL}")
        continue

    opcoes[opcao](lista_ativos)