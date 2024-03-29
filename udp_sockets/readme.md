# O Protocolo UDP

> Neste trabalho iremos explorar a implementação de uma aplicação rodando sobre UDP através da programação com sockets. Este trabalho tem a finalidade de trazer o conhecimento de programação e funcionamento básico do protocolo UDP, principalmente comparando o UDP com os serviços que o TCP fornece para a camada de aplicação. Baseado no primeiro trabalho, mas agora transformando o anterior em um Servidor UDP simplificado.

## Fluxo do trabalho:

1. **Servidor UDP** (deve executar antes do cliente)
   1. Escolher um porta para comunicação (maior que 1024)
   2. Na recepção de dados:
      1. Tratar esses dados (requisição necessária - **propor o seu próprio protocolo** para substituir o **HTTP** )
         1. Ex.: GET /arquivo
         1. Transmitir o arquivo requisitado pelo cliente (deve ser grande)
            1. Dividir o arquivo em pedaços (tamanho do buffer)
               1. Qual o tamanho do buffer?
               1. Buffer cliente e servidor devem ser iguais?
               1. O valor do MTU influencia?
               1. Para que colocar checksum?
               1. Preciso numerar os pedaços?
               1. Se o arquivo não existir, como aviso o cliente?
1. **Cliente UDP** (deve executar depois do servidor)
   1. Colocar o endereço da máquina e porta escolhida para o servidor
      1. @ip do servidor:(Porta servidor)/arquivo
   1. Requisitar um arquivo
   1. Dar a opção ao usuário (Professor) para descartar uma parte do arquivo
      1. Para simular a perda de dados e testar o mecanismo de recuperação de dados proposto pelo aluno.
   1. Receber, montar e conferir (checksums) o arquivo recebido do servidor
   1. Se arquivo OK:
      1. Apresentar o arquivo requisitado
   1. Se arquivo não OK
      1. Verificar quais pedaços faltam e pedir para re-enviar.
   1. Interpretar ERROS.
      1. Ex.: Arquivo não encontrado etc.
