from unittest.mock import patch

from interface import escolher_opcao, selecionar_opcao_menu


def test_escolher_opcao_retorna_valor_da_opcao():
    escolhas = [
        {"name": "Primeira", "value": 1},
        {"name": "Segunda", "value": 2},
    ]

    with patch("builtins.input", return_value="2"):
        assert escolher_opcao("Escolha", escolhas) == 2


def test_escolher_opcao_repete_entrada_invalida():
    escolhas = [{"name": "Voltar", "value": None}]

    with patch("builtins.input", side_effect=["abc", "1"]):
        assert escolher_opcao("Escolha", escolhas) is None


def test_menu_principal_retorna_opcao():
    with patch("builtins.input", return_value="10"):
        assert selecionar_opcao_menu() == 10
