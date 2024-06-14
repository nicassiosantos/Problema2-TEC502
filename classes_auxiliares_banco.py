#Classe responsável por registrar a lista de transações de uam conta 
class Historico: 
    def __init__(self, transacoes=[]): 
        self._transacoes = transacoes
    #Função responsável por adicionar uma transação ao historico 
    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao) 
    #Função responsável por retornar a lista de transações de uma conta
    @property
    def transacoes(self): 
        return self._transacoes

#Classe de conta de uma pessoa
class Conta: 
    def __init__(self, numero, agencia, cliente, **kw):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()  

    #Função responsavel por retornar o saldo atual de uma conta
    @property
    def saldo(self): 
        return self._saldo 
    
    #Função responsavel por retornar o numero atual de uma conta
    @property
    def numero(self): 
        return self._numero
    
    #Função responsavel por retornar a agencia atual de uma conta
    @property
    def agencia(self): 
        return self._agencia
    
    #Função responsavel por retornar o cliente responsavel por uma conta
    @property
    def cliente(self): 
        return self._cliente
    
    #Função responsavel por retornar o historico atual de uma conta
    @property
    def historico(self): 
        return self._historico
    

class Conta_conjunta: 
    def __init__(self, numero, agencia, clientes, **kw):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._clientes = clientes
        self._historico = Historico()  

    #Função responsavel por retornar o saldo atual de uma conta
    @property
    def saldo(self): 
        return self._saldo 
    
    #Função responsavel por retornar o numero atual de uma conta
    @property
    def numero(self): 
        return self._numero
    
    #Função responsavel por retornar a agencia atual de uma conta
    @property
    def agencia(self): 
        return self._agencia
    
    #Função responsavel por retornar o cliente responsavel por uma conta
    @property
    def cliente(self): 
        return self._clientes
    
    #Função responsavel por retornar o historico atual de uma conta
    @property
    def historico(self): 
        return self._historico

#Classe pessoa fisica onde é armazenado suas contas e seu endereço
class Pessoa_fisica:
    def __init__(self, nome, cpf, senha, contas = [], **kw): 
        self._contas = contas 
        self._cpf = cpf
        self._nome = nome  
        self._senha = senha

    #Função responsavel por realizar uma transação em uma conta especifica de uma pessoa fisica
    def realizar_transacao(self, conta, transacao, **kw): 
        transacao.registrar(conta)

    #Função responsavel por adicionar uma nova conta no perfil da pessoa fisica
    def adicionar_conta(self, conta, **kw): 
        self._contas.append(conta)
    
    #Função responsavel por  obter o atributo das contas da pessoa fisica
    @property
    def contas(self):
        return self._contas
    
    #Função responsavel por  obter o atributo do cpf da pessoa fisica
    @property
    def cpf(self): 
        return self._cpf
    
    #Função responsavel por  obter o atributo do cpf da pessoa fisica
    @property
    def nome(self): 
        return self._nome
    
    #Função responsavel por  obter o atributo do senha da pessoa fisica
    @property
    def senha(self): 
        return self._senha
    
#Classe pessoa juridica onde é armazenado suas contas e seu endereço
class Pessoa_juridica:
    def __init__(self, nome, cnpj, senha, contas = [], **kw): 
        self._contas = contas 
        self._cnpj = cnpj
        self._nome = nome  
        self._senha = senha

    #Função responsavel por realizar uma transação em uma conta especifica de uma pessoa juridica
    def realizar_transacao(self, conta, transacao, **kw): 
        transacao.registrar(conta)

    #Função responsavel por adicionar uma nova conta no perfil da pessoa juridica
    def adicionar_conta(self, conta, **kw): 
        self._contas.append(conta)
    
    #Função responsavel por  obter o atributo das contas da pessoa juridica
    @property
    def contas(self):
        return self._contas
    
    #Função responsavel por  obter o atributo do cpf da pessoa juridica
    @property
    def cnpj(self): 
        return self._cnpj
    
    #Função responsavel por  obter o atributo do cpf da pessoa juridica
    @property
    def nome(self): 
        return self._nome
    
    #Função responsavel por  obter o atributo do senha da pessoa juridica
    @property
    def senha(self): 
        return self._senha