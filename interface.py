import subprocess
from InquirerPy import get_style, inquirer
from InquirerPy.separator import Separator

estilo_menu = get_style(
    {
        "questionmark": "#40e0b0",
        "question": "#94a3b8",
        "pointer": "#40e0b0 bold",
        "answer": "#40e0b0",
        "separator": "#718096",
        "instruction": "#718096",
    },
    style_override=False,
)

def selecionar_opcao_menu():

    opcao = inquirer.select(
        message="",
        choices=[
        Separator("── GERENCIAMENTO DE ATIVOS ─────────────────────────"),
        Separator(""),
        {"name": "1 - Cadastrar Ativo", "value": 1},
        {"name": "2 - Cadastrar Vulnerabilidade", "value": 2},
        {"name": "3 - Listar Ativos", "value": 3},
        {"name": "4 - Consultar Ativo", "value": 4},
        {"name": "5 - Atualizar Ativo", "value": 5},
        {"name": "6 - Remover Ativo", "value": 6},
        Separator(""),
        Separator("── ANÁLISE E DEPENDÊNCIAS ─────────────────────────"),
        Separator(""),
        {"name": "7 - Mostrar Riscos", "value": 7},
        {"name": "8 - Cadastrar Dependências", "value": 8},
        {"name": "9 - Remover Dependência", "value": 9},
        {"name": "10 - Sair", "value": 10},
        Separator(" "),
        Separator("────────────────────────────────────────────────────"),
        Separator("↑↓ Navegar    Enter Selecionar"),
    ],

    max_height="100%",
    style=estilo_menu,
    pointer="❯",
    qmark="",
    instruction="",
    show_cursor=False,
    ).execute()

    return opcao

def limpar_terminal():
    subprocess.run(["clear"], check=False)

if __name__ == "__main__":
    print(selecionar_opcao_menu())
    