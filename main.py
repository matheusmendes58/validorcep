from model import Banco


class Main(Banco):
    print('***' * 10)
    print('Validação de cep')
    print('***' * 10)
    print('[1] Para verificar cep e cadatrar no banco')
    print('[2] Para ver dados no banco')
    opcao = int(input('Digite sua opcao:'))

    if opcao == 1:
        Banco.incercao(Banco)
    elif opcao == 2:
        Banco.ver_todos_os_dados(Banco)

