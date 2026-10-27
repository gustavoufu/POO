from modelos import TITULO, VERDE, VERMELHO, NORMAL
from dados import salvar_arquivos
<<<<<<< Updated upstream
from validacoes import (verificar_int, pedir_input, pedir_severidade, 
    exibir_tipos_de_ativos, pedir_tipo_de_ativo, exibe_vulnerabilidades_ativo)
=======
from validacoes import (verificar_int, pedir_input,
    exibir_tipos_de_ativos, pedir_tipo_de_ativo, exibe_vulnerabilidades_ativo, pedir_cvss)
from calculo_risco import calculo_risco_proprio, calculo_risco_total
>>>>>>> Stashed changes
from classes import *

def mostrar_menu():
    print()
    print(f"{TITULO}-=-=-=-=-=-=-= MENU PRINCIPAL =-=-=-=-=-=--=-={NORMAL}")
    print()
    print("1 - Cadastro de ativos")
    print("2 - Cadastrar vulnerabilidades")
    print("3 - Listar ativos")
    print("4 - Buscar e Consultar ativos")
    print("5 - Atualizar ativos")
    print("6 - Remover ativos")
    print("7 - Mostrar riscos")
    print("8 - Sair")
    print()

def cadastrar_ativo(lista_ativos):
    print()
    print(f"{TITULO}=-=-=-=-=- CADASTRO DE NOVO ATIVO -=-=-=-=-=-={NORMAL}")
    print()
    if lista_ativos:
        novo_id = max(ativo.id for ativo in lista_ativos) + 1
    else:
        novo_id = 1

    id_ativo = novo_id
    nome_ativo = pedir_input("Digite o nome do ativo: ")
    responsavel_ativo = pedir_input("Digite o responsável pelo ativo: ")
    setor_ativo = pedir_input("Digite o setor responsável: ")
    tipo_ativo = exibir_tipos_de_ativos() or pedir_tipo_de_ativo()

    if tipo_ativo == 1:
        sistema_operacional_ativo = pedir_input("Digite o sistema operacional do notebook: ")
        ativo_objeto_novo = Notebook(id_ativo, nome_ativo, responsavel_ativo, setor_ativo, sistema_operacional_ativo)

    elif tipo_ativo == 2:
        tipo_servidor_ativo = pedir_input("Digite o tipo do servidor [Físico, Virtual, Nuvem]: ")
        ativo_objeto_novo = Servidor(id_ativo, nome_ativo, responsavel_ativo, setor_ativo, tipo_servidor_ativo)

    elif tipo_ativo == 3:
        versao_firmware_ativo = pedir_input("Digite a versão do firmware do roteador: ")
        ativo_objeto_novo = Roteador(id_ativo, nome_ativo, responsavel_ativo, setor_ativo, versao_firmware_ativo)
        
    elif tipo_ativo == 4:
        versao_aplicativo = pedir_input("Digite a versão do aplicativo: ")
        ativo_objeto_novo = Aplicativo(id_ativo, nome_ativo, responsavel_ativo, setor_ativo, versao_aplicativo)

    while True:
        escolha = pedir_input("Deseja cadastrar uma vulnerabilidade inicial? [S/N] ").lower()
        if escolha == "s":
            nome = pedir_input("Digite um nome para a vulnerabilidade: ")
            descricao = pedir_input("Digite uma descrição: ")
            categoria = pedir_input("Digite uma categoria: ")
            severidade = pedir_severidade()
            status = pedir_input("Status de tratamento: ")

            vulne_nova = Vulnerabilidade(nome, descricao, categoria, severidade, status)
            ativo_objeto_novo.adicionar_vulnerabilidade(vulne_nova)
            break
        elif escolha == "n":
            break 
        else:
            print(f"{VERMELHO}Essa opção não está disponível!{NORMAL}")
            continue

    print()
    lista_ativos.append(ativo_objeto_novo)

    if salvar_arquivos(lista_ativos):
        print(f"{VERDE}Ativo cadastrado com sucesso!{NORMAL}")

def cadastrar_vulnerabilidade(lista_ativos):
    if lista_ativos == []:
        print("Não há ativos cadastrados!")
        return
    else:
        print()
        print(f"{TITULO}=-=-=-=-=-=- ATIVOS CADASTRADOS -=-=-=-=-=-=-={NORMAL}")
        print()
        for ativo in lista_ativos:
            print(f"ID:{ativo.id} - {ativo.nome}")
            print()

        while True:
            escolha_id = verificar_int("Digite o ID do ativo selecionado: ")
            print()
            encontrado = False
            for ativo in lista_ativos:
                if ativo.id == escolha_id:
                    encontrado = True

                    nome = pedir_input("Digite um nome para a vulnerabilidade: ")
                    descricao = pedir_input("Digite uma descrição: ")
                    categoria = pedir_input("Digite uma categoria: ")
                    severidade = pedir_severidade()
                    status = pedir_input("Status de tratamento: ")

                    vulne_nova = Vulnerabilidade(nome, descricao, categoria, severidade, status)

                    ativo.adicionar_vulnerabilidade(vulne_nova)

                    if salvar_arquivos(lista_ativos):
                        print()
                        print(f"{VERDE}Vulnerabilidade cadastrada com sucesso!{NORMAL}")
                    break
                
            if encontrado:
                break

            if not encontrado:
                    print(f"{VERMELHO}Esse ID não está cadastrado!{NORMAL}")
                    continue 

def listar_ativos(lista_ativos):
    print()
    if lista_ativos == []:
        print(f"{TITULO}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={NORMAL}")
        print()
        print("Não há ativos cadastrados!")
        return
    else:
        print(f"{TITULO}=-=-=-=-=-=- ATIVOS CADASTRADOS -=-=-=-=-=-=-={NORMAL}")
        print()
        for ativo in lista_ativos:
            print(f"ID: {ativo.id} | {ativo.nome}")

def consultar_ativo(lista_ativos):
    if lista_ativos == []:
        print()
        print("Não há ativos cadastrados!")
        return
    else:
        print()
        print(f"{TITULO}========== OPCÕES =========={NORMAL}")
        print()
        print("1 - Buscar por ID")
        print("2 - Buscar por Nome")
        print("3 - Voltar ao menu principal")
        print()
        
        while True:
            busca_opcao = verificar_int("Escolha uma opção: ")
            if busca_opcao not in range(1, 4):
                print(f"{VERMELHO}Essa opção não está disponível, Tente novamente!{NORMAL}")
                continue
            else: break

        if busca_opcao == 1:
            id_digitado = verificar_int("Digite o ID do ativo que deseja buscar: ")
            print()
            if id_digitado not in [ativo.id for ativo in lista_ativos]:
                print(f"{VERMELHO}Esse ID não foi encontrado!{NORMAL}")
                return
            else:
                for ativo in lista_ativos:
                    if ativo.id == id_digitado:

                        print(f"{TITULO}-=-=-=-=-=-=- ATIVO ENCONTRADO -=-=-=-=-=-=-=-{NORMAL}")
                        print()
                        ativo.exibir_detalhes()
                        print()
                        exibe_vulnerabilidades_ativo(ativo)

        elif busca_opcao == 2: 
            nome_digitado = pedir_input("Digite o nome do ativo que deseja buscar: ").strip()
            print()
            if nome_digitado.lower() not in (ativo.nome.lower() for ativo in lista_ativos):
                print(f"{VERMELHO}Esse nome não pertence a um ativo cadastrado!{NORMAL}")
                return
            else:
                for ativo in lista_ativos:
                    if ativo.nome.lower() == nome_digitado.lower():
                        
                        print(f"{TITULO}-=-=-=-=-=-=- ATIVO ENCONTRADO -=-=-=-=-=-=-=-{NORMAL}")
                        print()
                        ativo.exibir_detalhes()
                        print()
                        exibe_vulnerabilidades_ativo(ativo)

        elif busca_opcao == 3:
            return

def atualizar_ativo(lista_ativos):
    if lista_ativos == []:
        print()
        print(f"{TITULO}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={NORMAL}")
        print()
        print("Não há ativos cadastrados!")

    else:
        print()
        print(f"{TITULO}-=-=-=-=-=-=- ATIVOS CADASTRADOS -=-=-=-=-=-=-={NORMAL}")
        print()
        print("Qual ativo você deseja atualizar?")
        print()

        for ativo in lista_ativos:
            print(f"ID:{ativo.id} - {ativo.nome}")
            print()
            
        while True:
            id_escolhido = verificar_int("Digite o ID do ativo que deseja atualizar: ")

            encontrado = False
            for ativo in lista_ativos:
                if ativo.id == id_escolhido:
                    encontrado = True
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
                        
                        escolha_atualizar = verificar_int("Digite uma opção: ")
                        print()

                        if escolha_atualizar not in range(1, 6):
                            print(f"{VERMELHO}Essa opção não está disponível!{NORMAL}")
                            continue

                        elif escolha_atualizar == 1:
                            print(f"OBS: O nome atual é {ativo.nome}")
                            ativo.nome = pedir_input("Digite o novo nome do ativo: ")
                            if salvar_arquivos(lista_ativos):
                                print()
                                print(f"{VERDE}Nome alterado com sucesso!{NORMAL}")
                            

                        elif escolha_atualizar == 2:
                            print(f"OBS: O responsável atual é {ativo.responsavel}")
                            ativo.responsavel = pedir_input("Digite o responsável pelo ativo: ")
                            if salvar_arquivos(lista_ativos):
                                print()
                                print(f"{VERDE}Responsável alterado com sucesso!{NORMAL}")

                        elif escolha_atualizar == 3:
                            print(f"OBS: O setor responsável atual é {ativo.setor}")
                            ativo.setor = pedir_input("Digite o setor responsável: ")
                            if salvar_arquivos(lista_ativos):
                                print()
                                print(f"{VERDE}Setor alterado com sucesso!{NORMAL}")

                        elif escolha_atualizar == 4:
                            print(f"OBS: O ativo atual é do tipo {type(ativo).__name__}")
                            print()
                            exibir_tipos_de_ativos()
                            novo_ativo_tipo = pedir_tipo_de_ativo()

                            if novo_ativo_tipo == 1:
                                novo_ativo = Notebook(ativo.id, ativo.nome, ativo.responsavel, ativo.setor)
                            elif novo_ativo_tipo == 2:
                                novo_ativo = Servidor(ativo.id, ativo.nome, ativo.responsavel, ativo.setor)
                            elif novo_ativo_tipo == 3:
                                novo_ativo = Roteador(ativo.id, ativo.nome, ativo.responsavel, ativo.setor)
                            elif novo_ativo_tipo == 4:
                                novo_ativo = Aplicativo(ativo.id, ativo.nome, ativo.responsavel, ativo.setor)

                            # transferindo as vulnerabilidades do ativo antigo para o novo ativo
                            novo_ativo.vulnerabilidades = ativo.vulnerabilidades

                            posicao = lista_ativos.index(ativo)
                            lista_ativos[posicao] = novo_ativo
                            ativo = novo_ativo

                            if salvar_arquivos(lista_ativos):
                                print()
                                print(f"{VERDE}Tipo do ativo alterado com sucesso!{NORMAL}")

                        elif escolha_atualizar == 5:
                            break

            if encontrado:
                break 

            if not encontrado:
                print(f"{VERMELHO}Esse ID não está cadastrado!{NORMAL}")

def remover_ativo(lista_ativos):
    if lista_ativos == []:
        print()
        print(f"{TITULO}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={NORMAL}")
        print()
        print("Não há ativos cadastrados!")
        return

    print()
    print(f"{TITULO}-=-=-=-=-=- ATIVOS CADASTRADOS -=-=-=-=-=-=-={NORMAL}")
    print()
    print("Qual ativo você deseja remover?")
    print()

    for ativo in lista_ativos:
        print(f"ID:{ativo.id} - {ativo.nome}")
        print()

    while True:
        escolha_rem = verificar_int("Digite o ID do ativo a ser removido: ")
        print()
        
        encontrado = False
        for ativo in lista_ativos:
            if ativo.id == escolha_rem:
                encontrado = True

                print(f"{TITULO}=-=-=-=-=-= INFORMAÇÕES DO ATIVO =-=-=-=-=-=-={NORMAL}")
                print()
                ativo.exibir_detalhes()
                print()

                exibe_vulnerabilidades_ativo(ativo)

                while True:
                    print(f"{VERMELHO}Atenção{NORMAL}: ao excluir este ativo, todas as vulnerabilidades associadas a ele também serão removidas.")
                    confirmação = pedir_input("Confirma a exclusão? [S/N] ").lower()
                    print()
                    if confirmação == "s":
                        lista_ativos.remove(ativo)
                        if salvar_arquivos(lista_ativos):
                            print(f"{VERDE}Ativo removido com sucesso!{NORMAL}")
                        break
                    elif confirmação == "n":
                        print("Exclusão cancelada")
                        break
                    else:
                        print(f"{VERMELHO}Essa opção não está disponível, Tente novamente!{NORMAL}")
                        print()
                        continue

        if encontrado: break

        if not encontrado:
            print(f"{VERMELHO}Esse ID não foi encontrado!{NORMAL}")
            continue

def mostrar_riscos(lista_ativos):
    print()
    if lista_ativos == []:
        print(f"{TITULO}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-={NORMAL}")
        print()
        print("Não há ativos cadastrados!")
    else:
        print(f"{TITULO}-=-=-=-=-=-=-=-= RISCOS DOS ATIVOS =-=-=-=-=-=-=-=-={NORMAL}")
        print()

        risco_proprio = calculo_risco_proprio(lista_ativos)
        risco_total = calculo_risco_total(lista_ativos)

        for pos, ativo in enumerate(lista_ativos):
            print(f"ID: {ativo.id} | Nome: {ativo.nome}")
            print(f"Risco próprio: {risco_proprio[pos]}")
            print(f"Risco total: {risco_total[pos]:.2f}")
            print()