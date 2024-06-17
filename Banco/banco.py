from flask import Flask, request, jsonify, render_template, request, redirect, url_for, flash
from classes_auxiliares_banco import * 
import random
import time

app = Flask(__name__)

class Banco: 

    def __init__(self, nome): 
        self.nome = nome 
        self._clientes = [] 
        self._numero = 0 


    #Função responsável por verificar na lista de cliente do banco se existe o cliente passado 
    def busca_cliente(self, identificador):
        for cliente in self._clientes: 
            if cliente.identificador == identificador: 
                return cliente 
        return False
    
    #Função que recebe um cpf ou cnpj e retorna todas as contas atreladas ao cliente especifico
    def busca_contas(self,identificador): 
        if(self._clientes): 
            for cliente in self._clientes:
                 if cliente.identificador == identificador: 
                     return cliente.contas
        return False
    
    #Função que recebe o numero de uma conta e retorna uma conta que exista com o mesmo numero
    def busca_conta(self,numero): 
        try:
            if(self._clientes): 
                for cliente in self._clientes:
                    for conta in cliente.contas: 
                        if conta.numero == numero: 
                            return conta
            return False
        except Exception as e:
            print(f"Exceção: {e}")
            return False

    #Função responsável por cadastrar um cliente
    def cadastro_cliente_conta_unica(self, cliente):
        self._clientes.append(cliente)
        return True

    #Função responsável por criar um conta
    def criar_conta(self, conta, identificador): 
        cliente = self.busca_cliente(identificador)

        if cliente: 
            cliente.adicionar_conta(conta)
            return True
        
        return False

    def atualizar_numero_contas(self): 
        self._numero += 1

    @property
    def clientes(self):
        return self._clientes
    
    @property
    def numero(self):
        return self._numero
    

banco = Banco("ChainDesco")

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/cadastro_pessoa_fisica', methods=['POST'])
def cadastrar_conta_pessoa_fisica():
    data = request.get_json()
    nome = data.get('nome', '')
    cpf = data.get('cpf', '')
    senha = data.get('senha', '')

    if not nome or not cpf or not senha:
        return jsonify({'message': 'Nome, CPF e senha são obrigatórios'}), 400

    try: 
        pessoa_fisica = Pessoa_fisica(nome, cpf, senha)
        conta_pessoa_fisica = Conta(banco.numero, banco.nome, pessoa_fisica)
        pessoa_fisica.adicionar_conta(conta_pessoa_fisica)
        banco.cadastro_cliente_conta_unica(pessoa_fisica) 
        banco.atualizar_numero_contas()
        return jsonify({'message': 'Conta Para Pessoa fisica criada com sucesso', 'cpf': pessoa_fisica.identificador, 'Numero conta': conta_pessoa_fisica.numero
                        ,'Nome do Banco': conta_pessoa_fisica.nome_banco}), 201
    
    except Exception as e: 
        return jsonify({'message': f'Falha ao criar pessoa fisica, Exceção:{e}'}), 500


@app.route('/cadastro_pessoa_juridica', methods=['POST'])
def cadastrar_conta_pessoa_juridica():
    data = request.get_json()
    nome = data.get('nome', '')
    cnpj = data.get('cnpj', '')
    senha = data.get('senha', '')

    if not nome or not cnpj or not senha:
        return jsonify({'message': 'Nome, CNPJ e senha são obrigatórios'}), 400

    try:
        pessoa_juridica = Pessoa_juridica(nome, cnpj, senha)
        conta_pessoa_juridica = Conta(banco.numero, banco.nome, pessoa_juridica)
        pessoa_juridica.adicionar_conta(conta_pessoa_juridica)
        banco.cadastro_cliente_conta_unica(pessoa_juridica)
        banco.atualizar_numero_contas()
        return jsonify({'message': 'Conta Para Pessoa Juridica criada com sucesso', 'cnpj': pessoa_juridica.identificador , 'Numero conta': conta_pessoa_juridica.numero
                        ,'Nome do Banco': conta_pessoa_juridica.nome_banco}), 201
    except Exception as e: 
        return jsonify({'message': f'Falha ao criar pessoa juridica, Exceção:{e}'}), 500

@app.route('/clientes', methods=['GET'])
def get_clientes(): 
    if banco.clientes: 
        return jsonify({ 'message': f'Lista de clientes: {banco.clientes}'}), 201 
    else: 
        return jsonify({ 'message': 'Não existem clientes cadastrados'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identificador = data.get('identificador', '')
    senha = data.get('senha', '')

    if not identificador or not senha:
        return jsonify({'message': 'Identificador (CPF/CNPJ) e senha são obrigatórios'}), 400

    cliente = banco.busca_cliente(identificador)
    if cliente and cliente.senha == senha:
        return jsonify({'message': 'Login bem-sucedido', 'identificador': cliente.identificador, 'nome': cliente.nome}), 200
    else:
        return jsonify({'message': 'Identificador ou senha incorretos'}), 401

@app.route('/deposito', methods=['POST'])
def deposito():
    data = request.get_json()
    identificador = data.get('identificador', '')
    numero_conta = data.get('numero_conta', '')
    valor = data.get('valor', 0)

    if not identificador or not numero_conta or valor <= 0:
        return jsonify({'message': 'Identificador, número da conta e valor válido são obrigatórios'}), 400

    numero_conta = int(numero_conta)

    cliente = banco.busca_cliente(identificador)
    if not cliente:
        return jsonify({'message': 'Cliente não encontrado'}), 404

    conta = banco.busca_conta(numero_conta)
    if not conta or cliente not in conta.clientes:
        return jsonify({'message': 'Conta não encontrada ou cliente não autorizado'}), 404

    tentativas = 5
    for tentativa in range(tentativas):
        if tentativa > 0:
            # Espera um tempo aleatório entre 1 e 3 segundos antes de tentar novamente
            tempo_espera = random.randint(1, 3)
            time.sleep(tempo_espera)

        try:
            codigo_execucao = conta.iniciar_transacao()
            sucesso, mensagem = conta.depositar(valor, codigo_execucao)
            if sucesso:
                conta.finalizar_transacao()
                return jsonify({'message': mensagem}), 200
            else:
                conta.finalizar_transacao()
                return jsonify({'message': mensagem}), 500
        except Exception as e:
            if tentativa == tentativas - 1:
                print(f'Erro durante a transação após {tentativas} tentativas: {str(e)}')

    conta.finalizar_transacao()
    return jsonify({'message': 'Todas as tentativas de depósito falharam'}), 500

@app.route('/saque', methods=['POST'])
def saque():
    data = request.get_json()
    identificador = data.get('identificador', '')
    numero_conta = data.get('numero_conta', '')
    valor = data.get('valor', 0)

    if not identificador or not numero_conta or valor <= 0:
        return jsonify({'message': 'Identificador, número da conta e valor válido são obrigatórios'}), 400

    numero_conta = int(numero_conta)

    cliente = banco.busca_cliente(identificador)
    if not cliente:
        return jsonify({'message': 'Cliente não encontrado'}), 404

    conta = banco.busca_conta(numero_conta)
    if not conta or cliente not in conta.clientes:
        return jsonify({'message': 'Conta não encontrada ou cliente não autorizado'}), 404

    tentativas = 5
    for tentativa in range(tentativas):
        if tentativa > 0:
            # Espera um tempo aleatório entre 1 e 3 segundos antes de tentar novamente
            tempo_espera = random.randint(1, 3)
            time.sleep(tempo_espera)

        try:
            codigo_execucao = conta.iniciar_transacao()
            sucesso, mensagem = conta.retirar(valor, codigo_execucao)
            if sucesso:
                conta.finalizar_transacao()
                return jsonify({'message': mensagem}), 200
            else:
                return jsonify({'message': mensagem}), 500
        except Exception as e:
            if tentativa == tentativas - 1:
                print(f'Erro durante a transação após {tentativas} tentativas: {str(e)}')
    conta.finalizar_transacao()
    return jsonify({'message': 'Todas as tentativas de saque falharam'}), 500 

if __name__ == '__main__':
    app.run(port=5000, debug=True)
        