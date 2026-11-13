from modelos import VERDE, NORMAL
from operacoes import (
    cadastrar_ativo,
    cadastrar_vulnerabilidade,
    listar_ativos,
    consultar_ativo,
    atualizar_ativo,
    remover_ativo,
    mostrar_riscos,
    cadastrar_dependencias,
    remover_dependencia,
    )
from dados import carregar_ativos
from interface import selecionar_opcao_menu, limpar_terminal

lista_ativos = carregar_ativos()

opcoes = {
    1:cadastrar_ativo,
    2:cadastrar_vulnerabilidade,
    3:listar_ativos,
    4:consultar_ativo,
    5:atualizar_ativo,
    6:remover_ativo,
    7:mostrar_riscos,
    8:cadastrar_dependencias,
    9:remover_dependencia
}

while True:

    limpar_terminal()
    opcao = selecionar_opcao_menu()

    if opcao == 10:
        print()
        print(f"{VERDE}Saindo do sistema. Até logo!{NORMAL}")
        print()
        break

    opcoes[opcao](lista_ativos)