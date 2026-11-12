import copy
from calculo_risco import calculo_risco_efetivo, calculo_risco_proprio
from modelos import TITULO, VERDE, VERMELHO, NORMAL, TiposDeAtivos
from dados import salvar_arquivos
from validacoes import (verificar_int, pedir_input,
    exibir_tipos_de_ativos, pedir_tipo_de_ativo, exibe_vulnerabilidades_ativo, pedir_cvss, pedir_fator_dependencia)
from classes import *

def mostrar_menu():
    print()
    print(f"{TITULO}-=-=-=-=-=-=-= MENU PRINCIPAL =-=-=-=-=-=--=-={NORMAL}")
    print()
    print("1 - Cadastro de ativo")
    print("2 - Cadastrar vulnerabilidade")
    print("3 - Listar ativo")
    print("4 - Buscar e Consultar ativo")
    print("5 - Atualizar ativo")
    print("6 - Remover ativo")
    print("7 - Exibir riscos totais")
    print("8 - Cadastrar dependências")
    print("9 - Remover dependências")
    print("10 - Sair")
    print()

def cadastrar_ativo(lista_ativos):
    print()
    print(f"{TITULO}=-=-=-=-=- CADASTRO DE NOVO ATIVO -=-=-=-=-=-={NORMAL}")
    print()
    novo_id = max((ativo.id for ativo in lista_ativos), default=0) + 1

    nome_ativo = pedir_input("Digite o nome do ativo: ")
    responsavel_ativo = pedir_input("Digite o responsável pelo ativo: ")
    setor_ativo = pedir_input("Digite o setor responsável: ")
    exibir_tipos_de_ativos()
    tipo_ativo = TiposDeAtivos(pedir_tipo_de_ativo())

    classes_ativos = {
      TiposDeAtivos.Notebook: Notebook,
      TiposDeAtivos.Servidor: Servidor,
      TiposDeAtivos.Roteador: Roteador,
      TiposDeAtivos.Aplicativo: Aplicativo  
    }

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

def cadastrar_vulnerabilidade(lista_ativos):
    if not lista_ativos:
        print("Não há ativos cadastrados!")
        return
    
    listar_ativos(lista_ativos)

    while True:
        print()
        id_digitado = verificar_int("Digite o ID do ativo selecionado: ")
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

def listar_ativos(lista_ativos):
    print()
    print(f"{TITULO}=-=-=-=-=-=- ATIVOS CADASTRADOS -=-=-=-=-=-=-={NORMAL}")
    print()

    if not lista_ativos:
        print("Não há ativos cadastrados!")
        return
    
    for ativo in lista_ativos:
        print(f"ID:{ativo.id} - {ativo.nome}")

def consultar_ativo(lista_ativos):
    if not lista_ativos:
        print()
        print("Não há ativos cadastrados!")
        return
    
    while True:
        print()
        print(f"{TITULO}========== OPCÕES =========={NORMAL}")
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
                    break   
                print()
                ativo = buscar_ativo_por_id(id_digitado, lista_ativos)
                if ativo is None:
                    print("Esse ativo não foi encontrado, tente novamente...")
                    continue
                exibir_ativos_e_vulnerabilidades(ativo)
                input("\nPressione Enter para voltar ao menu de consulta...")
                break

        elif busca_opcao == 2: 
            while True:
                nome_digitado = pedir_input("Digite o nome do ativo que deseja buscar (0 para voltar): ")
                if nome_digitado == "0":
                    break
                print()
                ativos = buscar_ativo_por_nome(nome_digitado, lista_ativos)
                if not ativos:
                    print("Não foi encontrado nenhum ativo com esse nome, tente novamente...")
                    continue

                for ativo in ativos:
                    exibir_ativos_e_vulnerabilidades(ativo)
                input("\nPressione Enter para voltar ao menu de consulta...")
                break

        elif busca_opcao == 3:
            listar_ativos(lista_ativos)
            input("\nPressione Enter para voltar...")

        elif busca_opcao == 4:
            return

def atualizar_ativo(lista_ativos):
    if not lista_ativos:
        print()
        print(f"{TITULO}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={NORMAL}")
        print()
        print("Não há ativos cadastrados!")
        return

    listar_ativos(lista_ativos)

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
            print()
            print(f"{TITULO}-=-=-=-=-=- ATUALIZAÇÃO DE ATIVO -=-=-=-=-=-={NORMAL}")
            print()
            print("O que deseja atualizar no ativo?")
            print()
            print("1 - Nome")
            print("2 - Responsável")
            print("3 - Setor")
            print("4 - Tipo")
            print("5 - Voltar ao menu principal")
            print()
            
            escolha_digitada = verificar_int("Digite uma opção: ")
            print()

            if escolha_digitada not in range(1, 6):
                print(f"{VERMELHO}Essa opção não está disponível!{NORMAL}")
                continue

            elif escolha_digitada == 5:
                break

            opcoes_atualizar = {
                1: atualizar_nome,
                2: atualizar_responsavel,
                3: atualizar_setor,
                4: atualizar_tipo,
            }

            opcoes_atualizar[escolha_digitada](ativo, lista_ativos)

            ativo = buscar_ativo_por_id(id_digitado, lista_ativos)
        break

def remover_ativo(lista_ativos):
    if not lista_ativos:
        print()
        print(f"{TITULO}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={NORMAL}")
        print()
        print("Não há ativos cadastrados!")
        return

    listar_ativos(lista_ativos)

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
            return

def mostrar_riscos(lista_ativos):

    if not lista_ativos:
        print()
        print("Nenhum ativo cadastrado.")
        return

    print(f"{TITULO}=-=-=-=-=-=-=-=-=- RISCOS -=-=-=-=-=-=-=-=-=-={NORMAL}")

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

def cadastrar_dependencias(lista_ativos):
    if len(lista_ativos) >= 2:
        listar_ativos(lista_ativos)
        print()
    else:
        print()
        print("É necessário ter pelo menos 2 ativos cadastrados.")
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

def remover_dependencia(lista_ativos):
    if not lista_ativos:
        print()
        print("Não há ativos cadastrados")
        return

    listar_ativos(lista_ativos)

    while True:
        print()
        id_digitado = verificar_int("Digite o ID do ativo que recebe o risco (0 para voltar) ")
        if id_digitado == 0:
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

    print()
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
        return
    else:
        ativo_recebe_risco.dependencias.append(dependencia_removida)

def atualizar_nome(ativo, lista_ativos):
    print(f"OBS: O nome atual é {ativo.nome}")
    ativo.nome = pedir_input("Digite o novo nome do ativo: ")
    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Nome alterado com sucesso!{NORMAL}")

def atualizar_responsavel(ativo, lista_ativos):
    print(f"OBS: O responsável atual é {ativo.responsavel}")
    ativo.responsavel = pedir_input("Digite o responsável pelo ativo: ")
    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Responsável alterado com sucesso!{NORMAL}")

def atualizar_setor(ativo, lista_ativos):
    print(f"OBS: O setor responsável atual é {ativo.setor}")
    ativo.setor = pedir_input("Digite o setor responsável: ")
    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Setor alterado com sucesso!{NORMAL}")

def atualizar_tipo(ativo, lista_ativos):
    print(f"OBS: O ativo atual é do tipo {type(ativo).__name__}")
    print()
    exibir_tipos_de_ativos()
    tipo_escolhido = pedir_tipo_de_ativo()

    tipos_de_ativos = {
        1: Notebook,
        2: Servidor,
        3: Roteador,
        4: Aplicativo
    }

    novo_ativo = tipos_de_ativos[tipo_escolhido](ativo.id, ativo.nome, ativo.responsavel, ativo.setor)

    novo_ativo.vulnerabilidades = ativo.vulnerabilidades
    novo_ativo.dependencias = ativo.dependencias

    posicao = lista_ativos.index(ativo)
    lista_ativos[posicao] = novo_ativo
    ativo = novo_ativo

    if salvar_arquivos(lista_ativos):
        print()
        print(f"{VERDE}Tipo do ativo alterado com sucesso!{NORMAL}")

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