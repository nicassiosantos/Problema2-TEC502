from flask import Flask, request, jsonify, render_template, request, redirect, url_for, flash
from Classes_auxiliares.classes_auxiliares_banco import * 
import requests

class Banco: 

    def __init__(self, nome, bancos): 
        self.nome = nome 
        self._clientes = [] 
        self._numero = 0 
        self._cliente_logado = None
        self.bancos = bancos

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
    def cadastro_cliente(self, cliente):
        self._clientes.append(cliente)
        return True

    #Função responsável por criar um conta
    def criar_conta(self, conta, identificador): 
        cliente = self.busca_cliente(identificador)

        if cliente: 
            cliente.adicionar_conta(conta)
            return True
        
        return False

    #Função responsável por atualizar o número de contas
    def atualizar_numero_contas(self): 
        self._numero += 1

    #Função para logar cliente
    def logar_cliente(self, identificador, senha): 
        cliente = self.busca_cliente(identificador)  
        if cliente and cliente.senha == senha: 
            self.cliente_logado = cliente
            return cliente
        else: 
            return False

    #Função para buscar URL do banco a patir do nome
    def buscar_url(self, nome_banco): 
        bancos = self.bancos
        if nome_banco in bancos:
            return bancos[nome_banco]
        else:
            return None  

    #Função para fazer a requisição de deposito par um banco externo
    def deposito_outro_banco(self, url, numero_conta, nome_banco, valor): 
        try:
            dados = {'numero_conta':numero_conta, 'nome_banco': nome_banco, 'valor': valor}
            response = requests.post(f'{url}/deposito', json=dados)
            if response.status_code == 200:
                return jsonify({'message': response.json().get('message')}), 200
            elif response.status_code == 500: 
                return jsonify({'message': response.json().get('message')}), 500
        except Exception as e: 
            print(f"Exceção: {e}")

    #Função para pegar uma conta de um banco externo
    def busca_conta_externa(self, url, nome_banco, numero_conta): 
        try:
            response = requests.get(f'{url}/get_conta/{nome_banco}/{numero_conta}')
            if response.status_code == 200:
                return jsonify(response.json()), 200
            elif response.status_code == 500: 
                return jsonify({'message': response.json().get('message')}), 500
        except Exception as e: 
            print(f"Exceção: {e}")
    
    #Função que recebe uma conta e a prepara para realizar uma transferência
    def preparacao_contas(self, banco, transferencias, preparados, preparacao):
        
        for transferencia in transferencias:
            numero_conta_origem = transferencia['numero_conta_origem']
            nome_banco_origem = transferencia['nome_banco_origem']
            valor = transferencia['valor']

            # Encontrar a conta de origem
            if nome_banco_origem == banco.nome:
                conta_origem = banco.busca_conta(numero_conta_origem)
                if not conta_origem:
                    preparados = False
                    break
    
                # Preparar a transferência na conta de origem
                conta_origem.lock.acquire(blocking=True)
                preparados = conta_origem.preparar_transferencia(valor)
                conta_origem.lock.release()
                preparacao.append((nome_banco_origem, conta_origem, valor))
            else: 
                for nome_banco, info in banco.bancos.items(): 
                    if nome_banco == nome_banco_origem: 
                        response = self.busca_conta_externa(info['url'],nome_banco_origem,numero_conta_origem)
                        
                        if response.status_code == 200: 
                            pass
                        else: 
                            preparados = False 
                            break
                if preparados == False: 
                    break
                       
    @property
    def clientes(self):
        return self._clientes
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente_logado(self):
        return self._cliente_logado
    
    @cliente_logado.setter
    def cliente_logado(self, valor):
        self._cliente_logado = valor
    


        