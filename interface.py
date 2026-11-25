from modelos import AMARELO, NORMAL
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
    prompt = inquirer.select(
        message="── GERENCIAMENTO DE ATIVOS ─────────────────────────",
        choices=[
        Separator(""),
        {"name": " Cadastrar Ativo", "value": 1},
        {"name": " Cadastrar Vulnerabilidade", "value": 2},
        {"name": " Listar Ativos", "value": 3},
        {"name": " Consultar Ativo", "value": 4},
        {"name": " Atualizar Ativo", "value": 5},
        {"name": " Remover Ativo", "value": 6},
        Separator(""),
        Separator("── ANÁLISE E DEPENDÊNCIAS ─────────────────────────"),
        Separator(""),
        {"name": " Mostrar Riscos", "value": 7},
        {"name": " Cadastrar Dependências", "value": 8},
        {"name": " Remover Dependência", "value": 9},
        {"name": " Sair", "value": 10},
        Separator(""),
        Separator("────────────────────────────────────────────────────"),
        Separator("↑↓ Navegar    Enter Selecionar"),
    ],

    max_height="100%",
    style=estilo_menu,
    pointer=">",
    qmark="",
    amark="",
    instruction="",
    show_cursor=False,
    default=0
    )
    prompt.application.erase_when_done = True
    return prompt.execute()

def escolher_opcao(mensagem, escolhas, titulo=None):
    prompt = inquirer.select(
        message=mensagem,
        choices=escolhas,
        style=estilo_menu,
        qmark="",
        amark="",
        pointer=">",
        show_cursor=False,
        default=0
    )
    prompt.application.erase_when_done = True
    return prompt.execute()

def limpar_terminal():
    print("\033[2J\033[H", end="", flush=True)

def imprimir_titulo(titulo, tamanho=55):
    prefixo = f"── {titulo.upper()} "
    print(prefixo + "─" * max(0, tamanho - len(prefixo)))
    print()

def aguardar_retorno_menu():
    input(f"\nPressione {AMARELO}Enter{NORMAL} para voltar ao menu...")
    limpar_terminal()

def ativos_em_opcoes_interface(lista_ativos):
    ativos_em_opcoes = []
    ativos_em_opcoes.append(Separator(""))
    for ativo in lista_ativos:
        opcao = {"name": f"ID {ativo.id} — {ativo.nome}", "value": ativo}
        ativos_em_opcoes.append(opcao)
    ativos_em_opcoes.append(Separator(""))
    ativos_em_opcoes.append({"name": "Voltar", "value": None})

    return ativos_em_opcoes

if __name__ == "__main__":
    print(selecionar_opcao_menu())
    