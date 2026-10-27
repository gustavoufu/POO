from abc import ABC, abstractmethod

class Vulnerabilidade:
    def __init__(self, nome, descricao, categoria, severidade, status, codigo_cve="Não informado"):
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.severidade = severidade
        self.status = status
        self.codigo_cve = codigo_cve

    def retorna_dicionario(self):
        return {
            "Nome": self.nome,
            "Descrição": self.descricao,
            "Categoria": self.categoria,
            "Severidade": self.severidade,
            "Status": self.status,
            "CVE": self.codigo_cve
        }

    def exibir_detalhes(self):
        print(f"Nome: {self.nome}")
        print(f"Descrição: {self.descricao}")
        print(f"Categoria: {self.categoria}")
        print(f"Severidade: {self.severidade}")
        print(f"Status: {self.status}")
        print(f"CVE: {self.codigo_cve}")

class Ativo(ABC):
    def __init__(self, id, nome, responsavel, setor):
        self.id = id
        self.nome = nome
        self.responsavel = responsavel
        self.setor = setor

        self.vulnerabilidades = []
        self.dependencias = []

    def retorna_dicionario(self):
        return {
            "Tipo": type(self).__name__,
            "Id": self.id,
            "Nome": self.nome,
            "Responsavel": self.responsavel,
            "Setor": self.setor,
            "Vulnerabilidades": [v.retorna_dicionario() for v in self.vulnerabilidades],
            "Dependencias" : self.dependencias
        }

    def exibir_detalhes(self):
        print(f"Tipo: {type(self).__name__}")
        print(f"Nome: {self.nome}")
        print(f"Id: {self.id}")
        print(f"Responsável: {self.responsavel}")
        print(f"Setor: {self.setor}")
        print(f"Vulnerabilidades: {len(self.vulnerabilidades)}")
        print(f"Fator de exposição: {self.fator_exposicao()}")

    def adicionar_vulnerabilidade(self, vulnerabilidade):
        self.vulnerabilidades.append(vulnerabilidade)

    def adicionar_dependencia(self, id_quem_compartilha_risco, fator):
        dependencia = {
            "AtivoIdBaseRisco": id_quem_compartilha_risco,
            "Fator": fator
        }
        self.dependencias.append(dependencia)

    @abstractmethod
    def fator_exposicao(self):
        pass

class Notebook(Ativo):
    def __init__(self, id, nome, responsavel, setor, sistema_operacional="Não informado"):
        super().__init__(id, nome, responsavel, setor)
        self.sistema_operacional = sistema_operacional

    def retorna_dicionario(self):
        dict_mae = super().retorna_dicionario()
        dict_mae["Sistema operacional"] = self.sistema_operacional
        return dict_mae

    def exibir_detalhes(self):
        super().exibir_detalhes()
        print(f"Sistema operacional: {self.sistema_operacional}")

    def fator_exposicao(self):
        return 1.0

class Servidor(Ativo):
    def __init__(self, id, nome, responsavel, setor, tipo_servidor="Não informado"):
        super().__init__(id, nome, responsavel, setor)
        self.tipo_servidor = tipo_servidor

    def retorna_dicionario(self):
        dict_mae = super().retorna_dicionario()
        dict_mae["Tipo_servidor"] = self.tipo_servidor
        return dict_mae

    def exibir_detalhes(self):
        super().exibir_detalhes()
        print(f"Tipo do servidor: {self.tipo_servidor}")

    def fator_exposicao(self):
        return 1.3

class Roteador(Ativo):
    def __init__(self, id, nome, responsavel, setor, versao_firmware="Não informado"):
        super().__init__(id, nome, responsavel, setor)
        self.versao_firmware = versao_firmware

    def retorna_dicionario(self):
        dict_mae = super().retorna_dicionario()
        dict_mae["Versão Firmware"] = self.versao_firmware
        return dict_mae

    def exibir_detalhes(self):
        super().exibir_detalhes()
        print(f"Versão do Firmware: {self.versao_firmware}")

    def fator_exposicao(self):
        return 1.2
    
class Aplicativo(Ativo):
    def __init__(self, id, nome, responsavel, setor, versao="Não informado"):
        super().__init__(id, nome, responsavel, setor)
        self.versao = versao

    def retorna_dicionario(self):
        dict_mae = super().retorna_dicionario()
        dict_mae["Versão"] = self.versao
        return dict_mae

    def exibir_detalhes(self):
        super().exibir_detalhes()
        print(f"Versão: {self.versao}")

    def fator_exposicao(self):
        return 1.1