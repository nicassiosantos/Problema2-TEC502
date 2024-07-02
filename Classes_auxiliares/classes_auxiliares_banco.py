import secrets 
from datetime import datetime
import threading 

class Historico:
    def __init__(self, transacoes=None):
        self._transacoes = transacoes if transacoes else []
        self._codigo_transacao = 0

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)
        self._codigo_transacao += 1

    @property
    def transacoes(self):
        return self._transacoes
    
    @property
    def codigo_transacoes(self):
        return self._codigo_transacao

class ContaBase:
    def __init__(self, numero, nome_banco, clientes=None):
        self._nome_banco = nome_banco
        self._saldo = 0
        self._numero = numero
        self._clientes = clientes if clientes else []
        self._historico = Historico()
        self._codigo_execucao = None

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def clientes(self):
        return self._clientes

    @property
    def historico(self):
        return self._historico
    
    @property
    def nome_banco(self):
        return self._nome_banco

    @property
    def codigo_execucao(self):
        return self._codigo_execucao

    def iniciar_transacao(self):
        if self._codigo_execucao is not None:
            raise Exception('Conta já está em uma transação')

        # Gerar um código aleatório seguro de 16 caracteres
        self._codigo_execucao = secrets.token_hex(8)
        return self._codigo_execucao

    def finalizar_transacao(self, codigo_execucao):
        if codigo_execucao == self._codigo_execucao:
            self._codigo_execucao = None
        else: 
            raise Exception('Código de execução inválido para finalizar essa transação')

    def depositar(self, valor, codigo_execucao):
        if self._codigo_execucao != codigo_execucao:
            return False, 'Código de execução inválido'  # Retorna uma tupla com False e mensagem de erro
        if valor <= 0:
            return False, 'Valor do depósito deve ser maior que zero'  # Retorna uma tupla com False e mensagem de erro
        
        self._saldo += valor
        self._historico.adicionar_transacao({
            "tipo": "Deposito",
            "valor": valor, 
            "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),

        })
        return True, f'Depósito de {valor} na conta {self._numero} realizado com sucesso'
    
    def retirar(self, valor, codigo_execucao):
        if self._codigo_execucao != codigo_execucao:
            return False, 'Código de execução inválido'  # Retorna uma tupla com False e mensagem de erro
        if valor <= 0:
            return False, 'Valor do saque deve ser maior que zero'  # Retorna uma tupla com False e mensagem de erro
        if self._saldo < valor:
            return False, 'Saldo insuficiente para realizar o saque'  # Retorna uma tupla com False e mensagem de erro

        self._saldo -= valor
        self._historico.adicionar_transacao({
            "tipo": "Saque",
            "valor": valor
        })
        return True, f'Saque de {valor} realizado com sucesso'

class Conta(ContaBase):
    def __init__(self, numero, nome_banco, cliente, **kw):
        super().__init__(numero, nome_banco, [cliente], **kw)

class Conta_conjunta(ContaBase):
    def __init__(self, numero, nome_banco, clientes, **kw):
        super().__init__(numero, nome_banco, clientes, **kw)

class Cliente:
    def __init__(self, nome, identificador, senha, contas=None):
        self._contas = contas if contas else []
        self._identificador = identificador
        self._nome = nome
        self._senha = senha

    def realizar_transacao(self, conta, transacao, **kw):
        transacao.registrar(conta)

    def adicionar_conta(self, conta, **kw):
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas

    @property
    def identificador(self):
        return self._identificador

    @property
    def nome(self):
        return self._nome

    @property
    def senha(self):
        return self._senha

class Pessoa_fisica(Cliente):
    def __init__(self, nome, cpf, senha, contas=None, **kw):
        super().__init__(nome, cpf, senha, contas, **kw)

class Pessoa_juridica(Cliente):
    def __init__(self, nome, cnpj, senha, contas=None, **kw):
        super().__init__(nome, cnpj, senha, contas, **kw)
