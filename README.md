# Problema 2 - Transações Bancárias Distribuídas 

1. [Utilizando a Aplicação](#utilizando-a-aplicação)
2. [Introdução](#introdução)
3. [Solução Proposta](#solução-proposta)
    - [Arquitetura Distribuída](#arquitetura-distribuída)
    - [Módulos do Sistema](#módulos-do-sistema)
    - [Tecnologias Utilizadas](#tecnologias-utilizadas)
    - [Protocolo Two-Phase Commit (2PC)](#protocolo-two-phase-commit-2pc)
    - [Fluxo de Transações](#fluxo-de-transações)
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

## Introdução 
Este projeto é uma solução para um problema proposto para disciplina de Concorrência e Conectividade, da Universidade Estadual de Feira de Santana(UEFS).O contexto foi baseado na ideia de que o governo de um país onde não existe banco central deseja implementar um sistema semelhante ao Pix do Brasil para permitir transações financeiras entre clientes de diferentes bancos. Devido à ausência de um banco central, o sistema não pode utilizar recursos centralizados para controlar as transações, exigindo uma solução distribuída. 

A partir disso, utilizando o python 3.11, foi implementado um sistema bancário distríbuido, em que é possivel fazer operações de contas de diferentes bancos de um mesmo cliente em um único banco,para este propósito, foram utilizadas rotas HTTP, com o auxilio do framework flask, aliado ao javascript, html e css, para construção das telas para utilização.O relatório será dividido em 3 seções, Introdução, Solução Proposta e e Conclusão, além da seção de que explica como utilizaro produto. 
    
