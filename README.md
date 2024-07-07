# Problema 2 - Transações Bancárias Distribuídas 

1. [Utilizando a Aplicação](#utilizando-a-aplicação)
2. [Introdução](#introdução)
3. [Produto Desenvolvido](#produto-desenvolvido)
    - [Arquitetura Implementada](#arquitetura-implementada)
    - [Módulos do Sistema](#módulos-do-sistema)
    - [Protocolo Two-Phase Commit (2PC)](#protocolo-two-phase-commit-2pc)
    - [Rotas principais](#rotas-principais)
4. [Conclusão](#conclusão)

## Utilizando A Aplicação 
Para Utilizar a aplicação desenvolvida é necessário seguir uma sequência de comandos através através do docker:

### Baixar a imagem do docker Hub 

    docker pull antnicassio/bank 

  Através desse comando a imagem será baixada em seu computador com todas as dependências para ser executada
  
### Executar a imagem 

  O sistema desenvolvido comporta até 3 ativos, é necessario rodar esse comando em 3 máquinas/IPS diferentes para que se tenha o ambiente da aplicação em todo seu suporte 

<p align="center">
    <img src="img\env.png" alt="app_ft1">
</p>
<p align="center">Variáveis de ambiente.</p> 

  Para executar a imagem é necessário entender as variáveis de ambiente: 

  - NUMERO_BANCO: Responsável por indicar qual banco você vai escolher para executar sendo números de 1 a 3 
  - IP_BANCO{1-3}: Responsável por indicar qual irá ser o IP do Banco sendo de 1 a 3 
  - NOME_BANCO{1 - 3}: Responsável por indicar o nome do banco escolhido a partir do número 
  - PORTA_BANCO{1 - 3}: Responsável por indicar a porta do ip escolhido 

  Exemplo de comando para subir um banco ao ar executando a imagem:

    docker run --rm --network=host -it -e NUMERO_BANCO=1 -e IP_BANCO2=127.0.0.2 -e IP_BANCO3=127.0.0.3 antnicassio/bank

  Como pode ser visto no exemplo acima, as variáveis ambiente podem ser modificadas na execução da imagem com a flag -e antes da variável. Nesse comando eu executo e subo o BANCO 1 com as seguintes caracteristicas: 

  - Nome: "Banco 1"
  - IP: "127.0.0.1"(Estou fazendo uma suposição que maquina que executei este comando tenha esse IP)
  - Porta: 4578
    
  Para obter o ip da maquina posso passar o IP "0.0.0.0" que desta forma consigo o ip atual da máquina, as outras informações que não passei permanecem com o mesmo padrão, o importante desse comando é identificar qual é o banco da imagem e quais são os ips dos outros bancos para que eles possam se comunicar. 

  Desta forma para subir os outros bancos para utilização seguiria com estes comandos em outras máquinas: 

  Banco 2: 

      docker run --rm --network=host -it -e NUMERO_BANCO=2 -e IP_BANCO1=127.0.0.1 -e IP_BANCO3=127.0.0.3 antnicassio/bank

  Banco 3: 

      docker run --rm --network=host -it -e NUMERO_BANCO=3 -e IP_BANCO1=127.0.0.1 -e IP_BANCO2=127.0.0.2 antnicassio/bank

  Vale destacar que as variavéis de ambiente estão disponiveis para serem utilizadas a depender da sua situação. 

### Telas e rotas 

<p align="center">
    <img src="img\Login.png" alt="app_ft1">
</p>
<p align="center">Login</p> 

Rota atual:"{url}/"

Ao entrar na url você passada entrar nessa pagina onde pode fazer o login ou cadastrar uma conta.

<p align="center">
    <img src="img\tiposcadastro.png" alt="app_ft1">
</p>
<p align="center">Escolha de cadastro</p> 

Rota atual:"{url}/cadastro"

Na tela de cadastro poderá escolher entre se cadastrar como pessoa fisica, juridica ou fazer uma conta conjunta. 

<p align="center">
    <img src="img\cadastrofis.png" alt="app_ft1">
</p>
<p align="center">Cadastro pessoa Física</p> 

Rota atual:"{url}/cadastro"

Escolhendo pessoa fisica poderá se cadastrar, e assim ganhando uma conta a partir disso, pessoa jurídica possui a mesma formatação, modificando apenas o CPF por CNPJ. 

<p align="center">
    <img src="img\Cadastroconj.png" alt="app_ft1">
</p>
<p align="center">Cadastro conta conjunta</p>  

Rota atual:"{url}/cadastro"

Pode-se criar uma conta conjunta a partir do identificador de duas contas existentes.

<p align="center">
    <img src="img\Home.png" alt="app_ft1">
</p>
<p align="center">Home</p>  

Rota atual:"{url}/home"

Após realizar o login terá a tela de home contendo todas as suas contas em todos os bancos em que possui conta, permitindo fazer depósito, transferência e saque.È válido lembrar que o saque só pode ser realizado em contas que do banco no qual você realizou o login.

<p align="center">
    <img src="img\Saque.png" alt="app_ft1">
</p>
<p align="center">Saque</p>  

Rota atual:"{url}/saque_page?numero_conta=x"

Ao clicar no botão saque, é redirecionado para pagina de Saque em que é possivel retirar um valor da conta escolhida

<p align="center">
    <img src="img\deposito.png" alt="app_ft1">
</p>
<p align="center">Depósito</p> 

Rota atual:"{url}/deposito_page"

Ao clicar no botão depósito é possivel realizar um depósito, passando o valor, numero da conta e o nome do banco  

<p align="center">
    <img src="img\Transfpt1.png" alt="app_ft1">
</p>
<p align="center">Transferência parte 1</p> 

Rota atual:"{url}/transferencia_page"

Ao clicar no botão de transferência é redirecionado para essa pagina em que pode tranferir o dinheiro para uma conta informando o nome do banco, o numero da conta e valor, este que é definido por outro campos que serão explicados abaixo 

<p align="center">
    <img src="img\Transfpt2.png" alt="app_ft1">
</p>
<p align="center">Transferência parte 2</p> 

Rota atual:"{url}/transferencia_page" 

Em transferência o valor a ser transferido para uma conta é definido a partir da soma dos valores que irão ser inseridos para serem retirados de cada conta, pelo campo valor a transferir.Após preencher os dados só basta clicar em realizar transferência.

## Introdução 
Este projeto é uma solução para um problema proposto para disciplina de Concorrência e Conectividade, da Universidade Estadual de Feira de Santana(UEFS).O contexto foi baseado na ideia de que o governo de um país onde não existe banco central deseja implementar um sistema semelhante ao Pix do Brasil para permitir transações financeiras entre clientes de diferentes bancos. Devido à ausência de um banco central, o sistema não pode utilizar recursos centralizados para controlar as transações, exigindo uma solução distribuída. 

A partir disso, utilizando o python 3.11, foi implementado um sistema bancário distríbuido, em que é possivel fazer operações de contas de diferentes bancos de um mesmo cliente em um único banco,para este propósito, foram utilizadas rotas HTTP, com o auxilio do framework flask, aliado ao javascript, html e css, para construção das telas para utilização.O relatório será dividido em 3 seções, Introdução, Solução Proposta e e Conclusão, além da seção de que explica como utilizar o produto. 

## Produto Desenvolvido

A solução implementada resultou em um sistema distriubuído de bancos, que conseguem realizar todas as operações, sem a necessidade de um intermediador para essa finalidade.Para melhor explicar este tópico essa seção foi divida em Arquitetura Implementada. 


### Arquitetura Implementada 

O sistema bancário desenvolvido adota uma arquitetura que permite que cada banco integrante opere de forma autônoma e também realiza consulta com outros através de protcolos HTTP com outros bancos conforme necessário para certas operações.

<p align="center">
    <img src="img\Arquitetura1.png" alt="app_ft1">
</p>
<p align="center">Arquitetura</p>  

Características Principais:

- Autonomia: Cada banco dentro do sistema é independente, podendo realizar suas operações sem a necessidade de interagir constantemente com outros bancos.

- Interoperabilidade: Embora os bancos sejam autônomos, eles podem se comunicar e trocar informações quando necessário. Essa interoperabilidade é alcançada através de interfaces e protocolos de comunicação padronizados, garantindo que os dados possam ser compartilhados de maneira eficiente e segura.

- Solicitação por demanda: A solicitação entre bancos ocorre somente quando necessário. Para certas operações,o sistema realiza consultas específicas ou trocas de mensagens utilizando o protocolo HTTP. Esse mecanismo garante que as operações sejam concluídas de maneira consistente e precisa.


### Módulos do Sistema 

O sistema foi dividido em 5 módulos/arquivos principais para que garantem sue funcionamento, sendo eles Classes auxiliares, Banco, API banco, templates e static, estes que serão melhor descritos nos tópicos abaixo.

#### Classes auxiliares 

Este arquivo contém funcionalidades básicas para contas e transações, incluindo depósitos, saques e transferências realizadas em uma única conta. Ele suporta contas individuais e conjuntas, bem como clientes individuais e corporativos, utilizando classes como ContaBase, Conta, Conta_conjunta, Cliente, Pessoa_fisica e Pessoa_juridica. O sistema garante segurança em operações concorrentes através de bloqueios (threading.Lock).Nesse arquivo contém a forma como o saldo de uma conta é modificado diretamente tanto para retirar algum valor, quanto para colocar. 

#### Banco
O arquivo contém a classe Banco que gerencia clientes, contas e operações bancárias. A classe possui métodos para cadastrar clientes, criar contas, realizar login e logout de clientes, buscar contas por identificador, buscar contas conjuntas, além de métodos para preparar e confirmar transferências tanto internas quanto para bancos externos via requisições HTTP. A integração com outros bancos é feita através de URLs definidas externamente. A classe também inclui métodos para desfazer transferências e para buscar informações de contas em bancos externos.

O código faz uso de concorrência através de bloqueios (lock.acquire() e lock.release()) para garantir a consistência durante operações críticas, como transferências entre contas. Além disso, ele utiliza a biblioteca requests para realizar requisições HTTP para serviços externos, como outros bancos, para operações como depósitos, preparação e confirmação de transferências.

### API Banco 
Este arquivo contem as rotas para o funcionamento do banco em si. Inicialmente, os usuários podem se cadastrar como pessoas físicas, pessoas jurídicas ou optar por contas conjuntas. Após o cadastro, é possível realizar login  e efetuar operações como depósitos, saques e transferências entre contas.

O arquivo também tem mecanismo de consulta, onde os clientes podem verificar informações detalhadas sobre suas contas. A interface de usuário é intuitiva, permitindo uma experiência fluida desde o login até a execução de operações financeiras complexas. Para garantir a integridade das transações, o aplicativo utiliza o protocolo Two-Phase Commit (2PC) para coordenação de transações distribuídas entre múltiplas instâncias bancárias, assegurando que as operações sejam concluídas de forma consistente e segura que será mais profundamente explicada em um tópico abaixo.

Além das funcionalidades principais, o aplicativo inclui rotas para gerenciamento de sessões de usuário, permitindo o logout seguro e protegendo informações sensíveis durante a navegação.

#### Templates e static 
Estas pastas são utilizadas para disponibilizadas os recursos que são utilizados para moldar a interface.A pasta template armazena os arquivos HTML que constituem as páginas da interface do usuário. Por outro lado, a pasta static contém arquivos estáticos como CSS, JavaScript que são servidos diretamente para o navegador do usuário.

### Protocolo Two-Phase Commit (2PC) 
Para implementação da operação de transferência que é um conjuto de de operações, foi escolhido o protocolo two-phase commit(2PC), através dele é possível garantir a atomicidade da transação, fazendo que uma transação só seja concluída se feita po inteiro. O algoritmo é baseado em duas fases:  

#### Fase de Preparação:

- A rota começa ao receber dados de uma solicitação POST, contendo informações sobre a transferência, como banco e conta de destino, valor e lista de transferências.
- As contas que terão dinheiro retirados na transferências são preparadas para a operação. Uma verificação inicial (preparados) determina se todas as contas podem prosseguir com a transação e o dinheiro que vai ser enviado é retirado da conta. 
- Se a preparação falha em qualquer ponto, a função `desfazer_alterações` é chamada para reverter quaisquer alterações feitas durante a preparação, assegurando que nenhum estado intermediário inconsistente permaneça.

#### Fase de Confirmação:

- Se a fase de preparação for bem-sucedida, a transação é confirmada. Isso envolve atualizar o saldo das contas conforme necessário.
- A confirmação é feita com uma chamada à função `confirmacao_contas`, que aplica as mudanças de maneira definitiva, fazendo com que a conta destino finalmente receba o dinheiro.
- Se a confirmação é bem-sucedida, uma mensagem de sucesso é retornada. Caso contrário, a função `desfazer_alterações` é novamente chamada para reverter quaisquer mudanças, garantindo que o sistema retorne ao estado inicial antes da tentativa de transferência.

