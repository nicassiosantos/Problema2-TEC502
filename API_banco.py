from flask import Flask, request, jsonify, render_template, request, redirect, url_for, flash
from Classes_auxiliares.classes_auxiliares_banco import Historico, Conta, Conta_conjunta, Cliente, Pessoa_fisica, Pessoa_juridica

from banco import Banco
import random
import time
import requests
import os



app = Flask(__name__)


NUMERO_BANCO = os.getenv('NUMERO_BANCO', '1')

ip_banco1 = os.getenv('IP_BANCO3', '1')
IP_BANCO1 = f"127.0.0.{ip_banco1}"
NOME_BANCO1 = os.getenv('NOME_BANCO1', 'Banco 1') 
PORTA_BANCO1 = os.getenv('PORTA_BANCO1', '5000')
URL_BANCO1 = f"http://{IP_BANCO1}:{PORTA_BANCO1}"

ip_banco2 = os.getenv('IP_BANCO2', '1')
IP_BANCO2 = f"127.0.0.{ip_banco2}"
NOME_BANCO2 = os.getenv('NOME_BANCO2', 'Banco 2') 
PORTA_BANCO2 = os.getenv('PORTA_BANCO2', '5000')
URL_BANCO2 = f"http://{IP_BANCO2}:{PORTA_BANCO2}"


ip_banco3 = os.getenv('IP_BANCO3', '1')
IP_BANCO3 = f"127.0.0.{ip_banco3}"
NOME_BANCO3 = os.getenv('NOME_BANCO3', 'Banco 3') 
PORTA_BANCO3 = os.getenv('PORTA_BANCO3', '5000')
URL_BANCO3 = f"http://{IP_BANCO3}:{PORTA_BANCO3}"


banco = Banco(eval(f"NOME_BANCO{NUMERO_BANCO}"))

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
        banco.cadastro_cliente(pessoa_fisica) 
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
        banco.cadastro_cliente(pessoa_juridica)
        banco.atualizar_numero_contas()
        return jsonify({'message': 'Conta Para Pessoa Juridica criada com sucesso', 'cnpj': pessoa_juridica.identificador , 'Numero conta': conta_pessoa_juridica.numero
                        ,'Nome do Banco': conta_pessoa_juridica.nome_banco}), 201
    except Exception as e: 
        return jsonify({'message': f'Falha ao criar pessoa juridica, Exceção:{e}'}), 500

@app.route('/cadastro_conta_conjunta', methods=['POST'])
def cadastrar_conta_conjunta():
    data = request.get_json()
    identificador1 = data.get('identificador1', '')
    identificador2 = data.get('identificador2', '')
    senha = data.get('senha', '')

    if not identificador1 or not identificador2 or not senha:
        return jsonify({'message': 'Identificadores e senha são obrigatórios'}), 400

    try:
        cliente1 = banco.busca_cliente(identificador1)
        cliente2 = banco.busca_cliente(identificador2)

        if not cliente1 or not cliente2:
            return jsonify({'message': 'Um ou ambos os clientes não foram encontrados'}), 404

        conta_conjunta = Conta_conjunta(banco.numero, banco.nome, [cliente1, cliente2])
        cliente1.adicionar_conta(conta_conjunta)
        cliente2.adicionar_conta(conta_conjunta)
        banco.atualizar_numero_contas()
        
        return jsonify({
            'message': 'Conta conjunta criada com sucesso',
            'identificadores': [cliente1.identificador, cliente2.identificador],
            'numero_conta': conta_conjunta.numero,
            'nome_banco': conta_conjunta.nome_banco
        }), 201
    except Exception as e:
        return jsonify({'message': f'Falha ao criar conta conjunta, Exceção: {e}'}), 500

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

    cliente = banco.logar_cliente(identificador, senha)
    if cliente:
        return jsonify({'message': 'Login bem-sucedido', 'identificador': cliente.identificador, 'nome': cliente.nome}), 200
    else:
        return jsonify({'message': 'Identificador ou senha incorretos'}), 401

@app.route('/deposito', methods=['POST'])
def deposito():
    data = request.get_json()
    numero_conta = data.get('numero_conta', '')
    nome_banco = data.get('nome_banco', '')
    valor = data.get('valor', 0)

    if nome_banco is None or not numero_conta or valor <= 0:
        return jsonify({'message': 'Nome do banco, número da conta e valor válido são obrigatórios'}), 400

    numero_conta = int(numero_conta)

    if nome_banco == banco.nome:
    
        conta = banco.busca_conta(numero_conta)
        if not conta:
            return jsonify({'message': 'Conta não encontrada'}), 404

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
                    return jsonify({'message': mensagem}), 500
            except Exception as e:
                if tentativa == tentativas - 1:
                    print(f'Erro durante a transação após {tentativas} tentativas: {str(e)}')

        conta.finalizar_transacao()
        return jsonify({'message': 'Todas as tentativas de depósito falharam'}), 500
    else: 
        if nome_banco == NOME_BANCO1: 
            try:
                response = requests.post(
                    URL_BANCO1 + '/deposito',
                    json={'numero_conta':numero_conta, 'nome_banco': nome_banco, 'valor': valor}
                ) 
                if response.status_code == 200:
                    return jsonify({'message': response.json().get('message')}), 200
                elif response.status_code == 500 or response.status_code == 404: 
                    return jsonify({'message': response.json().get('message')}), 500
            except Exception as e: 
                print(f"Exceção: {e}")
        elif nome_banco == NOME_BANCO2: 
            try:
                response = requests.post(
                    URL_BANCO2 + '/deposito',
                    json={'numero_conta':numero_conta, 'nome_banco': nome_banco, 'valor': valor}
                ) 
                if response.status_code == 200:
                    return jsonify({'message': response.json().get('message')}), 200
                elif response.status_code == 500: 
                    return jsonify({'message': response.json().get('message')}), 500
            except Exception as e: 
                print(f"Exceção: {e}")
        elif nome_banco == NOME_BANCO3: 
            try:
                response = requests.post(
                    URL_BANCO3 + '/deposito',
                    json={'numero_conta':numero_conta, 'nome_banco': nome_banco, 'valor': valor}
                ) 
                if response.status_code == 200:
                    return jsonify({'message': response.json().get('message')}), 200
                elif response.status_code == 500: 
                    return jsonify({'message': response.json().get('message')}), 500
            except Exception as e: 
                print(f"Exceção: {e}") 
        else: 
            return jsonify({'message': 'Banco inexistente'}), 500

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

@app.route('/contas_cliente', methods=['GET'])
def contas_cliente():
    data = request.get_json()
    identificador = data.get('identificador', '')

    if not identificador:
        return jsonify({'message': 'Identificador (CPF/CNPJ) é obrigatório'}), 400

    cliente = banco.busca_cliente(identificador)
    if not cliente:
        return jsonify({'message': 'Cliente não encontrado'}), 404

    contas_cliente = banco.busca_contas(identificador)
    if not contas_cliente:
        return jsonify({'message': 'Cliente não possui contas cadastradas'}), 404

    contas_info = []
    for conta in contas_cliente:
        contas_info.append({
            'numero_conta': conta.numero,
            'saldo': conta.saldo,
            'clientes': [cliente.nome for cliente in conta.clientes],
            'historico_transacoes': conta.historico.transacoes,
            'nome_banco': conta.nome_banco
        })

    return jsonify({'contas': contas_info}), 200 

@app.route('/iniciar_transacao', methods=['POST'])
def iniciar_transacao():
    data = request.get_json()
    identificador = data.get('identificador', '')
    numero_conta = data.get('numero_conta', '')

    if not identificador or not numero_conta:
        return jsonify({'message': 'Identificador e número da conta são obrigatórios'}), 400

    conta = banco.busca_conta(numero_conta)
    if not conta:
        return jsonify({'message': 'Conta não encontrada'}), 404

    try:
        codigo_execucao = conta.iniciar_transacao()
        return jsonify({'codigo_execucao': codigo_execucao}), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao iniciar transação: {e}'}), 500

@app.route('/finalizar_transacao', methods=['POST'])
def finalizar_transacao():
    data = request.get_json()
    identificador = data.get('identificador', '')
    numero_conta = data.get('numero_conta', '')

    if not identificador or not numero_conta:
        return jsonify({'message': 'Identificador e número da conta são obrigatórios'}), 400

    conta = banco.busca_conta(numero_conta)
    if not conta:
        return jsonify({'message': 'Conta não encontrada'}), 404

    try:
        conta.finalizar_transacao()
        return jsonify({'message': 'Transação finalizada com sucesso'}), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao finalizar transação: {e}'}), 500

@app.route('/deposito_transferencia', methods=['POST'])
def deposito_transferencia():
    data = request.get_json()
    numero_conta = data.get('numero_conta', '')
    valor = data.get('valor', 0)
    codigo_execucao = data.get('codigo_execucao', '')

    if not numero_conta or valor <= 0 or not codigo_execucao:
        return jsonify({'message': 'Número da conta, valor e código de execução são obrigatórios'}), 400

    numero_conta = int(numero_conta)
    conta = banco.busca_conta(numero_conta)
    if not conta:
        return jsonify({'message': 'Conta não encontrada'}), 404

    sucesso, mensagem = conta.depositar(valor, codigo_execucao)
    if sucesso:
        return jsonify({'message': mensagem}), 200
    else:
        return jsonify({'message': mensagem}), 500

@app.route('/retirada_transferencia', methods=['POST'])
def retirada_transferencia():
    data = request.get_json()
    numero_conta = data.get('numero_conta', '')
    valor = data.get('valor', 0)
    codigo_execucao = data.get('codigo_execucao', '')

    if not numero_conta or valor <= 0 or not codigo_execucao:
        return jsonify({'message': 'Número da conta, valor e código de execução são obrigatórios'}), 400

    numero_conta = int(numero_conta)
    conta = banco.busca_conta(numero_conta)
    if not conta:
        return jsonify({'message': 'Conta não encontrada'}), 404

    sucesso, mensagem = conta.retirar(valor, codigo_execucao)
    if sucesso:
        return jsonify({'message': mensagem}), 200
    else:
        return jsonify({'message': mensagem}), 500

@app.route('/transferencia', methods=['POST'])
def transferencia():
    data = request.get_json()
    identificador_origem = data.get('identificador_origem', '')
    numero_conta_origem = data.get('numero_conta_origem', '')
    numero_conta_destino = data.get('numero_conta_destino', '')
    valor = data.get('valor', 0)
    url_banco_origem = data.get('url_banco_origem', '')
    url_banco_destino = data.get('url_banco_destino', '')

    if not numero_conta_origem or not numero_conta_destino or valor <= 0:
        return jsonify({'message': 'Número da conta de origem, conta de destino e valor válido são obrigatórios'}), 400

    numero_conta_origem = int(numero_conta_origem)
    numero_conta_destino = int(numero_conta_destino)

    transferencia_interna = (not url_banco_origem and not url_banco_destino)
    transferencia_externa_saida = (not url_banco_origem and url_banco_destino)
    transferencia_externa_entrada = (url_banco_origem and not url_banco_destino)
    transferencia_externa_total = (url_banco_origem and url_banco_destino)

    if transferencia_interna:
        # Transferência interna
        conta_origem = banco.busca_conta(numero_conta_origem)
        conta_destino = banco.busca_conta(numero_conta_destino)
        
        if not conta_origem or not conta_destino:
            return jsonify({'message': 'Conta origem ou destino não encontrada'}), 404

        try:
            codigo_execucao_origem = conta_origem.iniciar_transacao()
            sucesso_retirada, mensagem_retirada = conta_origem.retirar(valor, codigo_execucao_origem)
            if not sucesso_retirada:
                return jsonify({'message': mensagem_retirada}), 500

            codigo_execucao_destino = conta_destino.iniciar_transacao()
            sucesso_deposito, mensagem_deposito = conta_destino.depositar(valor, codigo_execucao_destino)
            if not sucesso_deposito:
                conta_origem.depositar(valor, codigo_execucao_origem)
                return jsonify({'message': mensagem_deposito}), 500

            conta_origem.finalizar_transacao()
            conta_destino.finalizar_transacao()

            return jsonify({'message': 'Transferência interna realizada com sucesso'}), 200
        except Exception as e:
            return jsonify({'message': f'Erro ao realizar transferência interna: {e}'}), 500
    
    elif transferencia_externa_saida:
        # Transferência de uma conta do banco intermediário para um banco externo
        conta_origem = banco.busca_conta(numero_conta_origem)
        if not conta_origem:
            return jsonify({'message': 'Conta origem não encontrada'}), 404

        try:
            codigo_execucao_origem = conta_origem.iniciar_transacao()
            sucesso_retirada, mensagem_retirada = conta_origem.retirar(valor, codigo_execucao_origem)
            if not sucesso_retirada:
                return jsonify({'message': mensagem_retirada}), 500

            response_destino = requests.post(
                url_banco_destino + '/iniciar_transacao',
                json={'numero_conta': numero_conta_destino}
            )
            if response_destino.status_code != 200:
                conta_origem.depositar(valor, codigo_execucao_origem)
                return jsonify({'message': 'Falha ao iniciar transação no banco destino', 'detalhes': response_destino.json()}), 500

            codigo_execucao_destino = response_destino.json().get('codigo_execucao')

            response_deposito = requests.post(
                url_banco_destino + '/deposito_transferencia',
                json={'numero_conta': numero_conta_destino, 'valor': valor, 'codigo_execucao': codigo_execucao_destino}
            )
            if response_deposito.status_code != 200:
                conta_origem.depositar(valor, codigo_execucao_origem)
                return jsonify({'message': 'Falha ao realizar depósito no banco destino', 'detalhes': response_deposito.json()}), 500

            conta_origem.finalizar_transacao()

            
            if response_finalizar_destino.status_code != 200:
                return jsonify({'message': 'Falha ao finalizar transação no banco destino', 'detalhes': response_finalizar_destino.json()}), 500

            return jsonify({'message': 'Transferência realizada com sucesso'}), 200
        except Exception as e:
            return jsonify({'message': f'Erro ao realizar transferência: {e}'}), 500

    elif transferencia_externa_entrada:
        # Transferência de um banco externo para uma conta do banco intermediário
        conta_destino = banco.busca_conta(numero_conta_destino)
        if not conta_destino:
            return jsonify({'message': 'Conta destino não encontrada'}), 404

        try:
            response_origem = requests.post(
                url_banco_origem + '/iniciar_transacao',
                json={'identificador': identificador_origem, 'numero_conta': numero_conta_origem}
            )
            if response_origem.status_code != 200:
                return jsonify({'message': 'Falha ao iniciar transação no banco de origem', 'detalhes': response_origem.json()}), 500

            codigo_execucao_origem = response_origem.json().get('codigo_execucao')

            response_retirada = requests.post(
                url_banco_origem + '/retirada_transferencia',
                json={'numero_conta': numero_conta_origem, 'valor': valor, 'codigo_execucao': codigo_execucao_origem}
            )
            if response_retirada.status_code != 200:
                return jsonify({'message': 'Falha ao realizar retirada no banco de origem', 'detalhes': response_retirada.json()}), 500

            codigo_execucao_destino = conta_destino.iniciar_transacao()
            sucesso_deposito, mensagem_deposito = conta_destino.depositar(valor, codigo_execucao_destino)
            if not sucesso_deposito:
                requests.post(
                    url_banco_origem + '/deposito_transferencia',
                    json={'numero_conta': numero_conta_origem, 'valor': valor, 'codigo_execucao': codigo_execucao_origem}
                )
                return jsonify({'message': mensagem_deposito}), 500

            response_finalizar_origem = requests.post(
                url_banco_origem + '/finalizar_transacao',
                json={'identificador': identificador_origem, 'numero_conta': numero_conta_origem}
            )
            if response_finalizar_origem.status_code != 200:
                conta_destino.retirar(valor, codigo_execucao_destino)
                return jsonify({'message': 'Falha ao finalizar transação no banco de origem', 'detalhes': response_finalizar_origem.json()}), 500

            conta_destino.finalizar_transacao()

            return jsonify({'message': 'Transferência realizada com sucesso'}), 200
        except Exception as e:
            return jsonify({'message': f'Erro ao realizar transferência: {e}'}), 500

    elif transferencia_externa_total:
        # Transferência de um banco externo para outro banco externo
        try:
            response_origem = requests.post(
                url_banco_origem + '/iniciar_transacao',
                json={'identificador': identificador_origem, 'numero_conta': numero_conta_origem}
            )
            if response_origem.status_code != 200:
                return jsonify({'message': 'Falha ao iniciar transação no banco de origem', 'detalhes': response_origem.json()}), 500

            codigo_execucao_origem = response_origem.json().get('codigo_execucao')

            response_retirada = requests.post(
                url_banco_origem + '/retirada_transferencia',
                json={'numero_conta': numero_conta_origem, 'valor': valor, 'codigo_execucao': codigo_execucao_origem}
            )
            if response_retirada.status_code != 200:
                return jsonify({'message': 'Falha ao realizar retirada no banco de origem', 'detalhes': response_retirada.json()}), 500

            response_destino = requests.post(
                url_banco_destino + '/iniciar_transacao',
                json={'numero_conta': numero_conta_destino}
            )
            if response_destino.status_code != 200:
                requests.post(
                    url_banco_origem + '/deposito_transferencia',
                    json={'numero_conta': numero_conta_origem, 'valor': valor, 'codigo_execucao': codigo_execucao_origem}
                )
                return jsonify({'message': 'Falha ao iniciar transação no banco destino', 'detalhes': response_destino.json()}), 500

            codigo_execucao_destino = response_destino.json().get('codigo_execucao')

            response_deposito = requests.post(
                url_banco_destino + '/deposito_transferencia',
                json={'numero_conta': numero_conta_destino, 'valor': valor, 'codigo_execucao': codigo_execucao_destino}
            )
            if response_deposito.status_code != 200:
                requests.post(
                    url_banco_origem + '/deposito_transferencia',
                    json={'numero_conta': numero_conta_origem, 'valor': valor, 'codigo_execucao': codigo_execucao_origem}
                )
                return jsonify({'message': 'Falha ao realizar depósito no banco destino', 'detalhes': response_deposito.json()}), 500

            response_finalizar_origem = requests.post(
                url_banco_origem + '/finalizar_transacao',
                json={'identificador': identificador_origem, 'numero_conta': numero_conta_origem}
            )
            if response_finalizar_origem.status_code != 200:
                requests.post(
                    url_banco_destino + '/retirada_transferencia',
                    json={'numero_conta': numero_conta_destino, 'valor': valor, 'codigo_execucao': codigo_execucao_destino}
                )
                return jsonify({'message': 'Falha ao finalizar transação no banco de origem', 'detalhes': response_finalizar_origem.json()}), 500

            response_finalizar_destino = requests.post(
                url_banco_destino + '/finalizar_transacao',
                json={'numero_conta': numero_conta_destino}
            )
            if response_finalizar_destino.status_code != 200:
                return jsonify({'message': 'Falha ao finalizar transação no banco destino', 'detalhes': response_finalizar_destino.json()}), 500

            return jsonify({'message': 'Transferência realizada com sucesso'}), 200
        except Exception as e:
            return jsonify({'message': f'Erro ao realizar transferência: {e}'}), 500

    return jsonify({'message': 'Tipo de transferência não suportada'}), 400

if __name__ == '__main__':
    app.run(host=eval(f"IP_BANCO{NUMERO_BANCO}"), port=eval(f"PORTA_BANCO{NUMERO_BANCO}"))