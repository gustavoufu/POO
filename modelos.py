from enum import Enum

VERMELHO = "\033[1;31m"
VERDE = "\033[1;32m"
TITULO = "\033[1;36m"
NORMAL = "\033[0m"

class TiposDeAtivos(Enum):
    Notebook = 1
    Servidor = 2
    Roteador = 3
    Aplicativo = 4

class Severidade_Extenso(Enum):
    Baixa = 1
    Média = 2
    Alta = 3
    Crítica = 4