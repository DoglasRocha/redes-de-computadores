# O Protocolo de Controle de Transmissão - TCP

Neste trabalho iremos continuar explorando a implementação de uma aplicação rodando sobre TCP através da programação com sockets. Este trabalho tem a finalidade de trazer o conhecimento de programação e funcionamento básico do protocolo TCP, principalmente demonstrando os serviços que o TCP fornece para a camada de aplicação. Baseado no primeiro trabalho, mas agora transformando o anterior em um **Servidor HTTP simplificado**.

## Fluxo do trabalho:

1.  Procurar um código “Hello word” usando servidor TCP multi thread e seu cliente.
    1.  Este trabalho pode ser realizado em qualquer linguagem de programação, a escolha do aluno, mas lembre-se: não pode ser usado bibliotecas que manipulem o TCP, e sim usar o TCP diretamente através da criação e manipulação dos sockets.
1.  No servidor TCP (deve executar antes do cliente)
    1. Escolher um porta para receber as conexões (maior que 1024)
    1. Aceitar a conexão do cliente
    1. Criar uma thread com a conexão do cliente (para cada cliente). Na thread:
       1. Receber dados recebidos pelo cliente
       1. Tratar esses dados (requisição HTTP)
          1. Ex.: GET /pagina.html HTTP/1.0
1.  No Cliente TCP (deve executar depois do servidor)
    1. Usar o Browser de sua preferência
    1. Colocar o endereço da máquina e porta escolhida para o servidor
       1. URL : @ip do servidor:(Porta servidor)/pagina.html
    1. O Browser deve apresentar o arquivo requisitado na URL
       1. O Browser deve mostrar ao menos arquivos HTML + JPEG
       1. O Browser deve interpretar ERROS.
          1. Ex.: Resposta com 404.

## O trabalho deve:

1. Usar Sockets TCP Multi-thread
   1. Servidor
1. No Servidor (Nesta Fase não é necessário implementar o cliente, pois será usado um Browser como cliente.)
   1. Receber requisições do Cliente
   1. Tratar corretamente as requisições HTMP e fazer o esperado.
1. O Browser deve funcionar apresentando o arquivo requisitado na URL
   1. O Browser deve mostrar ao menos arquivos HTML + JPEG
   1. O Browser deve interpretar ERROS.
      1. Ex.: Resposta com 404.
