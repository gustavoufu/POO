# Sistema de Inventario de Ativos

## Sobre o projeto

O Sistema de Inventario de Ativos e uma aplicacao desenvolvida em Python voltada para o gerenciamento de ativos de TI e o acompanhamento de suas respectivas vulnerabilidades de seguranca. O programa opera diretamente pelo terminal e utiliza um arquivo local em formato JSON (`arquivoativos.json`) para a persistencia automatica dos dados, carregando as informacoes ao iniciar e atualizando-as apos cada operacao realizada.

## Funcionalidades

* **Gestao de Ativos:** Cadastro, listagem, busca, atualizacao e remocao de ativos no sistema.
* **Busca Avancada:** Localizacao de ativos especificos utilizando criterios como ID ou nome.
* **Controle de Vulnerabilidades:** Registro de vulnerabilidades associadas diretamente a cada ativo cadastrado.
* **Consulta de Vulnerabilidades:** Visualizacao detalhada das falhas de seguranca vinculadas a cada item do inventario.
* **Seguranca na Exclusao:** Etapa de confirmacao previa antes da remocao de um ativo, garantindo tambem a exclusao controlada de suas vulnerabilidades associadas.

## Como obter o projeto

Para clonar e configurar o repositorio em sua maquina local, abra o terminal e execute os comandos abaixo, que nao exigem autenticacao previa:

```bash
git clone https://github.com/gustavoufu/sistema-inventario.git
cd sistema-inventario

```

## Como executar

Certifique-se de possuir o Python instalado em seu ambiente. Com o repositorio clonado e acessando o diretorio do projeto atraves do terminal, execute o seguinte comando:

```bash
python main.py

```

## Dados armazenados

O sistema estrutura as informacoes utilizando dois componentes principais salvos no arquivo `arquivoativos.json`:

* **Ativos:** Cada registro e composto por ID, nome, responsavel, setor, tipo e uma lista dedicada de vulnerabilidades.
* **Vulnerabilidades:** Cada item vinculado ao ativo possui nome, descricao, categoria, severidade e status de tratamento.