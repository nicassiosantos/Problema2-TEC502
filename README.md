# Problema 2 - Transações Bancárias Distribuídas 

1. [Utilizando a Aplicação](#utilizando-a-aplicação)
2. [Solução Proposta](#solução-proposta)
    - [Arquitetura Distribuída](#arquitetura-distribuída)
    - [Módulos do Sistema](#módulos-do-sistema)
    - [Tecnologias Utilizadas](#tecnologias-utilizadas)
    - [Protocolo Two-Phase Commit (2PC)](#protocolo-two-phase-commit-2pc)
    - [Fluxo de Transações](#fluxo-de-transações)
3. [Conclusão](#conclusão)

## Utilizando A Aplicação 
Para Utilizar a aplicação desenvolvida é necessário seguir uma sequência de comandos através através do docker:

### Baixar a imagem do docker Hub 

    docker pull antnicassio/bank 

  - Através desse comando a imagem será baixada em seu computador com todas as dependências para ser executada
  
### Executar a imagem 

    docker run  --rm --network=host -it -e SERVER_IP=ip -e SERVER_PORT_TCP=porta_tcp -e SERVER_PORT_UDP=porta_udp -e HTTP_PORT=porta_http  antnicassio/redes-broker
