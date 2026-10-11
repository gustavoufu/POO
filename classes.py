from abc import ABC, abstractmethod

class Vulnerabilidade:
    def __init__(self, nome, descricao, categoria, severidade, status):
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.severidade = severidade
        self.status = status

    def retorna_dicionario(self):
        return {
            "Nome": self.nome,
            "Descrição": self.descricao,
            "Categoria": self.categoria,
            "Severidade": self.severidade,
            "Status": self.status
        }

    def exibir_detalhes(self):
        print(f"Nome: {self.nome}")
        print(f"Descrição: {self.descricao}")
        print(f"Categoria: {self.categoria}")
        print(f"Severidade: {self.severidade}")
        print(f"Status: {self.status}")

class Ativo(ABC):
    def __init__(self, id, nome, responsavel, setor):
        self.id = id
        self.nome = nome
        self.responsavel = responsavel
        self.setor = setor

        self.vulnerabilidades = []

    def retorna_dicionario(self):
        return {
            "Tipo": type(self).__name__,
            "Id": self.id,
            "Nome": self.nome,
            "Responsavel": self.responsavel,
            "Setor": self.setor,
            "Vulnerabilidades": [v.retorna_dicionario() for v in self.vulnerabilidades]
        }

    def exibir_detalhes(self):
        print(f"Tipo: {type(self).__name__}")
        print(f"Nome: {self.nome}")
        print(f"Id: {self.id}")
        print(f"Responsável: {self.responsavel}")
        print(f"Setor: {self.setor}")
        print(f"Vulnerabilidades: {len(self.vulnerabilidades)}")

    def adicionar_vulnerabilidade(self, vulnerabilidade):
        self.vulnerabilidades.append(vulnerabilidade)

class Notebook(Ativo):
    pass

class Servidor(Ativo):
    pass

class Roteador(Ativo):
    pass

class Aplicativo(Ativo):
    pass