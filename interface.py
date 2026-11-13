import subprocess
from InquirerPy import inquirer

def selecionar_opcao_menu():

    opcao = inquirer.select(
        message="Escolha uma opção",
        choices=[
        {"name": "1 - Cadastrar Ativo", "value": 1},
        {"name": "2 - Cadastrar Vulnerabilidade", "value": 2},
        {"name": "3 - Listar Ativos", "value": 3},
        {"name": "4 - Consultar Ativo", "value": 4},
        {"name": "5 - Atualizar Ativo", "value": 5},
        {"name": "6 - Remover Ativo", "value": 6},
        {"name": "7 - Mostrar Riscos", "value": 7},
        {"name": "8 - Cadastrar Dependências", "value": 8},
        {"name": "9 - Remover Dependência", "value": 9},
        {"name": "10 - Sair", "value": 10}
    ],
    max_height="100%"
    ).execute()

    return opcao

def limpar_terminal():
    subprocess.run(["clear"], check=False)

if __name__ == "__main__":
    print(selecionar_opcao_menu())
    