# Sistema de Inventário de Ativos

Aplicação de terminal para cadastrar ativos de TI, associar vulnerabilidades e dependências entre ativos e consultar riscos. Os dados são persistidos em `arquivoativos.json`.

## Funcionalidades

- Cadastro, consulta, atualização e remoção de ativos: notebooks, servidores, roteadores e aplicativos.
- Cadastro e consulta de vulnerabilidades associadas aos ativos.
- Cadastro e remoção de dependências entre ativos, com fator de transmissão de risco.
- Consulta do risco próprio e do risco efetivo de cada ativo.
- Persistência automática dos ativos, vulnerabilidades e dependências em JSON.

## Modelo de orientação a objetos

`Equipamentos` é a classe-base abstrata. `Notebook`, `Servidor`, `Roteador` e `Aplicativo` herdam dela e acrescentam seus detalhes específicos. Cada ativo cadastrado é um objeto individual; vulnerabilidades e dependências ficam associadas ao objeto correspondente.

## Cálculo de risco

O programa monta as matrizes e vetores a partir dos dados cadastrados:

- `M`: matriz de incidência entre ativos e CVEs;
- `v`: vetor de severidades CVSS;
- `b = Mv`: risco próprio de cada ativo;
- `A`: matriz de dependências, em que cada valor representa a fração do risco transmitida.

O risco efetivo é calculado resolvendo `x = b + Ax`, ou, equivalentemente, `(I - A)x = b`. Antes de resolver o sistema, a aplicação verifica a invertibilidade e o condicionamento da matriz. O cálculo usa NumPy.

## Requisitos

- Python 3.13 para executar localmente, ou Docker com Docker Compose.
- As dependências Python estão listadas em `requirements.txt`.

## Executar localmente

Na pasta do projeto:

```bash
python -m pip install -r requirements.txt
python main.py
```

Use as setas e Enter para navegar pelo menu. A opção **Sair** encerra o programa.

## Executar com Docker Compose

Na pasta que contém `compose.yaml`:

```bash
docker compose up -d --build
docker compose ps
docker compose exec -it inventario python main.py
```

O serviço mantém o container ativo com `tail -f /dev/null`; o CRUD é iniciado separadamente com `docker compose exec`. Sair do menu encerra o CRUD, mas não o processo principal do container. O serviço usa a política `unless-stopped` e monta `arquivoativos.json` no container, preservando os dados no arquivo do projeto.

## Persistência e testes

`arquivoativos.json` contém um array JSON de ativos. Cada registro inclui o tipo e os dados do ativo, suas vulnerabilidades e suas dependências.

Para executar os testes:

```bash
python -m pytest
```
