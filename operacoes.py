import copy

from calculo_risco import calculo_risco_efetivo, calculo_risco_proprio
from modelos import TITULO, VERDE, VERMELHO, AMARELO, NORMAL, TiposDeAtivos
from dados import salvar_arquivos
from validacoes import (verificar_int, pedir_input,
    exibir_tipos_de_ativos, pedir_tipo_de_ativo, exibe_vulnerabilidades_ativo, pedir_cvss, pedir_fator_dependencia)
from classes import Aplicativo, Notebook, Roteador, Servidor, Vulnerabilidade
from interface import limpar_terminal


classes_ativos = {
    TiposDeAtivos.Notebook: Notebook,
    TiposDeAtivos.Servidor: Servidor,
    TiposDeAtivos.Roteador: Roteador,
    TiposDeAtivos.Aplicativo: Aplicativo,
}

def cadastrar_ativo(lista_ativos):
    limpar_terminal()
    novo_id = max((ativo.id for ativo in lista_ativos), default=0) + 1

    nome_ativo = pedir_input("Digite o nome do ativo: ")
    responsavel_ativo = pedir_input("Digite o responsável pelo ativo: ")
    setor_ativo = pedir_input("Digite o setor responsável: ")
    exibir_tipos_de_ativos()
    tipo_ativo = TiposDeAtivos(pedir_tipo_de_ativo(mostrar_atual=False))

    classe_ativo = classes_ativos[tipo_ativo]

    ativo_novo = classe_ativo(
        novo_id,
        nome_ativo,
        responsavel_ativo,
        setor_ativo,
    )

    ativo_novo.pedir_detalhe()

    while True:
        escolha = pedir_input("Deseja cadastrar uma vulnerabilidade inicial? [S/N] ").lower()
        if escolha == "s":
            ativo_novo.adicionar_vulnerabilidade(criar_vulnerabilidade())
            break
        elif escolha == "n":
            break 
        else:
            print(f"{VERMELHO}Essa opção não está disponível!{NORMAL}")

    print()
    lista_ativos.append(ativo_novo)

    if salvar_arquivos(lista_ativos):
        print(f"{VERDE}Ativo cadastrado com sucesso!{NORMAL}")
    else:
        lista_ativos.remove(ativo_novo)
        print(f"{VERMELHO}Erro ao salvar o ativo!{NORMAL}")

    aguardar_retorno_menu()

def cadastrar_vulnerabilidade(lista_ativos):
    limpar_terminal()
    if not lista_ativos:
        print("Não há ativos cadastrados!")
        aguardar_retorno_menu()
        return
    
    listar_ativos(lista_ativos, aguardar=False)

    while True:
        print()
        id_digitado = verificar_int("Digite o ID do ativo selecionado (0 para voltar): ")
        if id_digitado == 0:
            return
        print()

        ativo = buscar_ativo_por_id(id_digitado, lista_ativos)
        if ativo is None:
            print("Esse ativo não foi encontrado, tente novamente...")
            continue

        vulnerabilidade = criar_vulnerabilidade()
        ativo.adicionar_vulnerabilidade(vulnerabilidade)

        if salvar_arquivos(lista_ativos):
            print()
            print(f"{VERDE}Vulnerabilidade cadastrada com sucesso!{NORMAL}")
        else:
            ativo.vulnerabilidades.remove(vulnerabilidade)
            print(f"{VERMELHO}Erro ao salvar a vulnerabilidade!{NORMAL}")
        break

    aguardar_retorno_menu()

def listar_ativos(lista_ativos, aguardar=True):
    limpar_terminal()
    if not lista_ativos:
        print("Não há ativos cadastrados!")
        aguardar_retorno_menu()
        return
    
    for ativo in lista_ativos:
        print(f"ID:{ativo.id} - {ativo.nome}")

    if aguardar:
        aguardar_retorno_menu()

def consultar_ativo(lista_ativos):
    limpar_terminal()
    if not lista_ativos:
        print("Não há ativos cadastrados!")
        aguardar_retorno_menu()
        return
    
    while True:
        print()
        print("1 - Buscar por ID")
        print("2 - Buscar por Nome")
        print("3 - Listar todos os ativos")
        print("4 - Voltar ao menu principal")
        print()

        busca_opcao = verificar_int("Escolha uma opção: ")
        if busca_opcao not in range(1, 5):
            print(f"{VERMELHO}Essa opção não está disponível, Tente novamente!{NORMAL}")
            continue

        if busca_opcao == 1:
            while True:
                id_digitado = verificar_int("Digite o ID do ativo que deseja buscar (0 para voltar): ")
                if id_digitado == 0:
                    limpar_terminal()
                    break   
                print()
                ativo = buscar_ativo_por_id(id_digitado, lista_ativos)
                if ativo is None:
                    print("Esse ativo não foi encontrado, tente novamente...")
                    continue
                limpar_terminal()
                exibir_ativos_e_vulnerabilidades(ativo)
                input("\nPressione Enter para voltar ao menu de consulta...")
                limpar_terminal()
                break

        elif busca_opcao == 2: 
            while True:
                nome_digitado = pedir_input("Digite o nome do ativo que deseja buscar (0 para voltar): ")
                if nome_digitado == "0":
                    limpar_terminal()
                    break
                print()
                ativos = buscar_ativo_por_nome(nome_digitado, lista_ativos)
                if not ativos:
                    print("Não foi encontrado nenhum ativo com esse nome, tente novamente...")
                    continue

                for ativo in ativos:
                    limpar_terminal()
                    exibir_ativos_e_vulnerabilidades(ativo)
                input("\nPressione Enter para voltar ao menu de consulta...")
                limpar_terminal()
                break

        elif busca_opcao == 3:
            listar_ativos(lista_ativos, aguardar=False)
            input("\nPressione Enter para voltar...")
            limpar_terminal()

        elif busca_opcao == 4:
            limpar_terminal()
            return

def atualizar_ativo(lista_ativos):
    limpar_terminal()
    if not lista_ativos:
        print("Não há ativos cadastrados!")
        aguardar_retorno_menu()
        return

    listar_ativos(lista_ativos, aguardar=False)

    opcoes_atualizar = {
        1: atualizar_nome,
        2: atualizar_responsavel,
        3: atualizar_setor,
        4: atualizar_tipo,
    }

    while True:
        print()
        id_digitado = verificar_int("Digite o ID do ativo que deseja atualizar (0 para voltar): ")
        if id_digitado == 0:
            break
        ativo = buscar_ativo_por_id(id_digitado, lista_ativos)
        if ativo is None:
            print("Esse ativo não foi encontrado, tente novamente...")
            continue

        while True:
            limpar_terminal()
            print("O que deseja atualizar no ativo?")
            print()
            print("1 - Nome")
            print("2 - Responsável")
            print("3 - Setor")
            print("4 - Tipo")
            print("5 - Voltar ao menu principal")
            
            print()
            escolha_digitada = verificar_int("Digite uma opção: ")
            if escolha_digitada not in range(1, 6):
                print(f"{VERMELHO}Essa opção não está disponível!{NORMAL}")
                continue

            elif escolha_digitada == 5:
                break

            opcoes_atualizar[escolha_digitada](ativo, lista_ativos)

            ativo = buscar_ativo_por_id(id_digitado, lista_ativos)
        break

    aguardar_retorno_menu()

def remover_ativo(lista_ativos):
    limpar_terminal()
    if not lista_ativos:
        print("Não há ativos cadastrados!")
        aguardar_retorno_menu()
        return

    listar_ativos(lista_ativos, aguardar=False)

    while True:
        print()
        id_digitado = verificar_int("Digite o ID do ativo a ser removido (0 para voltar): ")
        if id_digitado == 0:
            break
        ativo = buscar_ativo_por_id(id_digitado, lista_ativos)
        if ativo is None:
            print(f"{VERMELHO}Esse ID não foi encontrado!{NORMAL}")
            continue

        print()
        print(f"{TITULO}=-=-=-=-=-= INFORMAÇÕES DO ATIVO =-=-=-=-=-=-={NORMAL}")
        print()
        ativo.exibir_detalhes()
        print()

        exibe_vulnerabilidades_ativo(ativo)

        while True:
            print(f"{VERMELHO}Atenção{NORMAL}: ao excluir este ativo, "
            "suas vulnerabilidades e dependências "
            "também serão removidas.")
            print
            confirmacao = pedir_input("Confirma a exclusão? [S/N] ").lower()

            if confirmacao not in ["s", "n"]:
                print(f"{VERMELHO}Essa opção não está disponível, Tente novamente!{NORMAL}")
                continue

            if confirmacao == "n":
                print("Exclusão cancelada")
                break

            backup_lista_ativos = copy.deepcopy(lista_ativos)
            for ativo_da_lista in lista_ativos:
                for dependencia in ativo_da_lista.dependencias.copy():
                    if dependencia["AtivoIdBaseRisco"] == ativo.id:
                        ativo_da_lista.dependencias.remove(dependencia)
            lista_ativos.remove(ativo)

            if salvar_arquivos(lista_ativos):
                print()
                print(f"{VERDE}Ativo removido com sucesso!{NORMAL}")
            else:
                lista_ativos[:] = backup_lista_ativos
            aguardar_retorno_menu()
            return

def mostrar_riscos(lista_ativos):
    limpar_terminal()
    if not lista_ativos:
        print("Nenhum ativo cadastrado.")
        aguardar_retorno_menu()
        return

    lista_dos_riscos_efetivos = calculo_risco_efetivo(lista_ativos)
    lista_dos_riscos_proprios = calculo_risco_proprio(lista_ativos)

    if lista_dos_riscos_efetivos is None:
        print(f"{VERMELHO}Erro{NORMAL}: Não foi possível calcular o risco efetivo. A matriz pode não ser invertível ou pode ser numericamente instável.")
        return

    for pos, ativo in enumerate(lista_ativos):
        print()
        print(f"Ativo: {ativo.nome}")
        print(f"Risco próprio: {lista_dos_riscos_proprios[pos]:.2f}")        
        print(f"Risco efetivo: {lista_dos_riscos_efetivos[pos]:.2f}")

    aguardar_retorno_menu()

def cadastrar_dependencias(lista_ativos):
    limpar_terminal()
    if len(lista_ativos) >= 2:
        listar_ativos(lista_ativos, aguardar=False)
        print()
    else:
        print("É necessário ter pelo menos 2 ativos cadastrados.")
        aguardar_retorno_menu()
        return

    while True: #ativo que recebe risco
        id_digitado = verificar_int("Digite o ID do ativo que receberá o risco (0 para voltar): ")
        if id_digitado == 0:
            return
        ativo_recebe_risco = buscar_ativo_por_id(id_digitado, lista_ativos)
        if ativo_recebe_risco is None:
            print(f"{VERMELHO}Esse ID não está cadastrado!{NORMAL}")
            continue
        break

    while True: #ativo que transmite risco
        id_digitado = verificar_int("Digite o ID do ativo que transmitirá o risco (0 para voltar): ")
        if id_digitado == 0:
            return
        ativo_transmite_risco = buscar_ativo_por_id(id_digitado, lista_ativos)
        if ativo_transmite_risco is None:
            print(f"{VERMELHO}Esse ID não está cadastrado!{NORMAL}")
            continue
        if ativo_transmite_risco == ativo_recebe_risco:
            print(f"{VERMELHO}O ativo receptor e o ativo transmissor devem ser diferentes.{NORMAL}")
            continue
        break

    for dependencia in ativo_recebe_risco.dependencias:
        if dependencia["AtivoIdBaseRisco"] == ativo_transmite_risco.id:
            print()
            print("Essa dependência já existe e não pode ser sobrescrita.")
            print("Exclua a dependência anterior para cadastrar outro fator.")
            return

    fator_digitado = pedir_fator_dependencia()

    soma_dos_fatores = 0

    for dependencia in ativo_recebe_risco.dependencias:
        soma_dos_fatores += dependencia["Fator"]

    if soma_dos_fatores + fator_digitado >= 1:
        print()
        print("Não foi possível cadastrar a dependência.")
        print("A soma dos fatores recebidos pelo ativo deve ser menor que 1.")
        return

    ativo_recebe_risco.adicionar_dependencia(ativo_transmite_risco.id, fator_digitado)
    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Dependência cadastrada com sucesso!{NORMAL}")
    else:
        ativo_recebe_risco.dependencias.pop()
    
    aguardar_retorno_menu()

def remover_dependencia(lista_ativos):
    limpar_terminal()
    if not lista_ativos:
        print("Não há ativos cadastrados")
        aguardar_retorno_menu()
        return

    listar_ativos(lista_ativos, aguardar=False)

    while True:
        print()
        id_digitado = verificar_int("Digite o ID do ativo que recebe o risco (0 para voltar) ")
        if id_digitado == 0:
            limpar_terminal()
            return
        ativo_recebe_risco = buscar_ativo_por_id(id_digitado, lista_ativos)
        if ativo_recebe_risco is None:
            print("Esse ID não pertence a um ativo cadastrado.")
            print()
            continue

        if not ativo_recebe_risco.dependencias:
            print("Esse ativo não possui dependências cadastradas, tente novamente...")
            print()
            continue
        break

    limpar_terminal()
    print(f"{TITULO}=-=-=-=-=- RELAÇÕES -=-=-=-=-=-={NORMAL}")
    print()

    for dependencia in ativo_recebe_risco.dependencias:
        id_transmissor = dependencia["AtivoIdBaseRisco"]
        fator_percentual = dependencia["Fator"]

        print(f"Transmissor: ID {id_transmissor}")
        print(f"Risco recebido: {fator_percentual:.0%}")
        print()

    ids_transmissores = [dependencia["AtivoIdBaseRisco"] for dependencia in ativo_recebe_risco.dependencias]

    while True:
        id_digitado = verificar_int("Digite o ID do ativo transmissor do risco (0 para voltar): ")
        if id_digitado == 0:
            limpar_terminal()
            return
        if id_digitado not in ids_transmissores:
            print("Esse ID não pertence a uma dependência deste ativo.")
            print()
            continue
        break

    for dependencia in ativo_recebe_risco.dependencias.copy():
        if dependencia["AtivoIdBaseRisco"] == id_digitado:
            dependencia_removida = dependencia
            ativo_recebe_risco.dependencias.remove(dependencia)
            break

    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Dependência removida com sucesso!{NORMAL}")
        aguardar_retorno_menu()
        return
    else:
        ativo_recebe_risco.dependencias.append(dependencia_removida)
    
    limpar_terminal()

def atualizar_nome(ativo, lista_ativos):
    print()
    print(f"OBS: O nome atual é {ativo.nome}")
    backup_nome = ativo.nome
    ativo.nome = pedir_input("Digite o novo nome do ativo: ")
    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Nome alterado com sucesso!{NORMAL}")
    else:
        ativo.nome = backup_nome

def atualizar_responsavel(ativo, lista_ativos):
    print()
    print(f"OBS: O responsável atual é {ativo.responsavel}")
    backup_responsavel = ativo.responsavel
    ativo.responsavel = pedir_input("Digite o responsável pelo ativo: ")
    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Responsável alterado com sucesso!{NORMAL}")
    else:
        ativo.responsavel = backup_responsavel

def atualizar_setor(ativo, lista_ativos):
    print()
    print(f"OBS: O setor responsável atual é {ativo.setor}")
    backup_setor = ativo.setor
    ativo.setor = pedir_input("Digite o setor responsável: ")
    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Setor alterado com sucesso!{NORMAL}")
    else:
        ativo.setor = backup_setor

def atualizar_tipo(ativo, lista_ativos):
    backup_ativo = ativo
    limpar_terminal()
    exibir_tipos_de_ativos()

    tipo_escolhido = TiposDeAtivos(pedir_tipo_de_ativo(ativo, mostrar_atual=True))
    classe_escolhida = classes_ativos[tipo_escolhido]

    if classe_escolhida is type(ativo):
        print()
        print(f"{VERMELHO}ERRO:{NORMAL} O ativo já é do tipo {type(ativo).__name__}")
        return

    novo_ativo = classe_escolhida(ativo.id, ativo.nome, ativo.responsavel, ativo.setor)
    novo_ativo.vulnerabilidades = ativo.vulnerabilidades
    novo_ativo.dependencias = ativo.dependencias
    novo_ativo.pedir_detalhe()

    posicao = lista_ativos.index(ativo)
    lista_ativos[posicao] = novo_ativo

    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Tipo do ativo alterado com sucesso!{NORMAL}")
    else:
        lista_ativos[posicao] = backup_ativo

def buscar_ativo_por_id(id_do_ativo, lista_ativos):
    for ativo in lista_ativos:
        if ativo.id == id_do_ativo:
            return ativo
    return None

def buscar_ativo_por_nome(nome_do_ativo, lista_ativos):
    return [ativo for ativo in lista_ativos if nome_do_ativo.lower() == ativo.nome.lower()]

def exibir_ativos_e_vulnerabilidades(ativo):
    print(f"{TITULO}-=-=-=-=-=-=- ATIVO ENCONTRADO -=-=-=-=-=-=-=-{NORMAL}")
    print()
    ativo.exibir_detalhes()
    print()
    exibe_vulnerabilidades_ativo(ativo)

def criar_vulnerabilidade():
    nome = pedir_input("Digite um nome para a vulnerabilidade: ")
    descricao = pedir_input("Digite uma descrição: ")
    categoria = pedir_input("Digite uma categoria: ")
    severidade = pedir_cvss()
    status = pedir_input("Status de tratamento: ")
    cve = pedir_input("Digite o código CVE: ")

    return Vulnerabilidade(nome, descricao, categoria, severidade, status, cve)

def aguardar_retorno_menu():
    input(f"\nPressione {AMARELO}Enter{NORMAL} para voltar ao menu de consulta...")
    limpar_terminal()