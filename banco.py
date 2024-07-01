from flask import Flask, request, jsonify, render_template, request, redirect, url_for, flash
from Classes_auxiliares.classes_auxiliares_banco import * 


class Banco: 

    def __init__(self, nome): 
        self.nome = nome 
        self._clientes = [] 
        self._numero = 0 
        self._cliente_logado = None

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
    


        