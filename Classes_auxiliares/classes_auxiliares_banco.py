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
        self._saldo_anterior = 0
        self._numero = numero
        self.modificado = False
        self._clientes = clientes if clientes else []
        self._historico = Historico()
        self.lock = threading.Lock()

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

    #Função que deposita um valor em uma conta
    def depositar(self, valor):

        if valor <= 0:
            return False, 'Valor do depósito deve ser maior que zero'  # Retorna uma tupla com False e mensagem de erro
        self._saldo_anterior = self._saldo
        self._saldo += valor
        self._historico.adicionar_transacao({
            "tipo": "Deposito",
            "valor": valor, 
            "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),

        })
        return True, f'Depósito de {valor} na conta {self._numero} realizado com sucesso'
    
    #Função que retira um valor em uma conta
    def retirar(self, valor, cliente_logado):
        if valor <= 0:
            return False, 'Valor do saque deve ser maior que zero'  # Retorna uma tupla com False e mensagem de erro
        if self._saldo < valor:
            return False, 'Saldo insuficiente para realizar o saque'  # Retorna uma tupla com False e mensagem de erro

        if cliente_logado == None: 
            return False, 'Realize o login para fazer o saque'

        if self.clientes[0].identificador != cliente_logado.identificador: 
            return False, 'Cliente sem  autorização para realizar o saque' # Retorna uma tupla com False e mensagem de erro

        self._saldo_anterior = self._saldo
        self._saldo -= valor
        self._historico.adicionar_transacao({
            "tipo": "Saque",
            "valor": valor, 
            "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        })
        return True, f'Saque de {valor} realizado com sucesso'

    #Função que prepara uma conta para uma transferência
    def preparar_transferencia(self, valor):
        if self._saldo >= valor: 
            return True 
        return False

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
