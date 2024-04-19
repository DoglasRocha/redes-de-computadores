# O Protocolo de Controle de Transmissão - TCP

> Neste trabalho iremos explorar a implementação de uma aplicação rodando sobre TCP através da programação com sockets. Este trabalho tem a finalidade de trazer o conhecimento de programação e funcionamento básico do protocolo TCP, principalmente demonstrando os serviços que o TCP fornece para a camada de aplicação.

## Fluxo do trabalho:

1. Procurar um código “Hello word” usando servidor TCP multi thread e seu cliente.
   1. Este trabalho pode ser realizado em qualquer linguagem de programação, a escolha do aluno, mas lembre-se: não pode ser usado bibliotecas que manipulem o TCP, e sim usar o TCP diretamente através da criação e manipulação dos sockets.
1. **No servidor TCP** (deve executar antes do cliente)
   1. Escolher um porta para receber as conexões (maior que 1024)
   1. Aceitar a conexão do cliente
   1. Criar uma thread com a conexão do cliente (para cada cliente). Na thread:
      1. Receber requisições enviadas pelo cliente:
         1. “**Sair**”
            1. se sim: fechar a conexão.
            1. Finalizar a thread.
         1. “**Arquivo**” + NOME.EXT (Deve poder tratar arquivo maior que 10M):
            1. Abrir o arquivo solicitado.
            1. Calcular o (Hash) do arquivo com SHA (Procure um exemplo de uso do SHA), que serve como verificador de integridade.
            1. Escolher a ordem/como enviar (Atenção! Este será o seu protocolo, você define.)
               1. Nome do arquivo
               1. Tamanho
               1. Hash
               1. Dados
               1. Status (ok, nok, etc…)
                  1. Ex.: arquivo inexistente.
         1. “**Chat**”
            1. Imprimir os dados recebidos na tela do servidor.
            1. Tudo digitado no servidor será enviado para o Cliente como “Chat”
1. **No Cliente TCP** (deve executar depois do servidor)
   1. Fazer a conexão para o endereço da máquina e porta escolhida para o servidor
      1. Abrir socket
   1. Enviar uma das opções tratadas no servidor (**requisições**), escolhida pelo usuário.
   1. Receber os dados do servidor: (**Resposta**)
      1. “**Sair**”
         1. se sim: fechar a conexão.
         1. Finalizar a thread.
      1. “**Arquivo**”:
         1. Receber os dados de acordo com a ordem escolhida. (Acabou de criar um protocolo!)
         1. Abrir o arquivo.
         1. Verificar o Hash
         1. Gravar o arquivo no cliente.
      1. “**Chat**”:
         1. Imprimir os dados recebidos na tela do cliente.

## O trabalho deve:

1.  Usar Sockets TCP Multi-thread
    1. Cliente e Servidor
1.  **No cliente**:
    1. O usuário escolher a requisição para se comunicar com o servidor.
    1. Enviar as requisições para o servidor.
    1. Receber as respostas do servidor e fazer o esperado.
    1. Fazer verificação de integridade do arquivo recebido (Verificar se Hash é igual).
1.  **No Servidor**:
    1. Receber requisições do Cliente
    1. Tratar corretamente as requisições e fazer o esperado.
