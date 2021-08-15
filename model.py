import sqlite3
import requests
import json
import datetime
class Banco:
    con = sqlite3.connect('cep.db')

    cursor = con.cursor()

    tabela = """
               create table if not exists endereco (indereco integer not null primary key autoincrement,
                                                    cep text,
                                                    logradouro text,
                                                    complemento text,
                                                    bairro text,
                                                    localidade text,
                                                    uf text,
                                                    ibge text, 
                                                    gia int,
                                                    ddd int,
                                                    siafi int,
                                                    validation text,
                                                    created text);"""
    cursor.execute(tabela)
    con.commit()
    con.close()

    def __init__(self, cep, logradouro, complemento, bairro, localidade, uf, ibge, gia, ddd, siafi, validation):
        self.cep = cep
        self.logradouro = logradouro
        self.complemento = complemento
        self.bairro = bairro
        self.localidade = localidade
        self.uf = uf
        self.ibge = ibge
        self.gia = gia
        self.ddd = ddd
        self.siafi = siafi
        self.validation = validation


    def incercao(self):
        try:
            # input para puxar o ceps da api
            input_cep = input('Digite o cep da sua rua com traço:')
            cidade_sugerida = input('Digite a cidade sugerida:').strip()

            if '-' not in input_cep:
                print('ERRO DE DIGITAÇÃO COLOQUE O TRAÇO')
                exit()
            elif len(input_cep) < 9 or len(input_cep) > 9:
                print('ERRO DE DIGITAÇÂO')
            requisicao = requests.get('https://viacep.com.br/ws/{}/json'.format(input_cep))

            # transformando o retorno em json em um dicionario
            jason = json.loads(requisicao.content)

            # manipulando json para fazer os inserts no banco de dados corretamente
            self.cep = jason['cep']
            self.logradouro = jason['logradouro']
            self.complemento = jason['complemento']
            self.bairro = jason['bairro']
            self.localidade = jason['localidade']
            self.uf = jason['uf']
            self.ibge = jason['ibge']
            self.gia = jason['gia']
            self.ddd = jason['ddd']
            self.siafi = jason['siafi']

            # validação se a cidade sugerida é igual a cidade do cep informado na busca para API
            if cidade_sugerida.upper() == self.localidade.upper():
                self.validation = 'TRUE'
                print('a cidade sugerida é igual a localidade na api')
            else:
                self.validation = 'FALSE'
                print('a cidade sugerida não é igual a localidade na api')

            # created
            data_atual = datetime.datetime.now()
            # convertendo em texto
            data_em_texto = data_atual.strftime('%d %m %Y %H:%M:%S')


            # inserts
            con = sqlite3.connect('cep.db')
            cursor = con.cursor()
            cursor.execute(""" insert into endereco (cep, logradouro, complemento, bairro, localidade , uf, ibge, gia, ddd, siafi, validation, created) 
                                values(?,?,?,?,?,?,?,?,?,?,?,?)""", (self.cep, self.logradouro, self.complemento, self.bairro, self.localidade, self.uf, self.ibge, self.gia, self.ddd, self.siafi, self.validation, data_em_texto))
            con.commit()
            con.close()

            return print('Sucesso todos os dados cadastrados no banco ')
        except:
            return print('ERRO NÂO FOI POSSIVEL CADASTRAR NO BANCO')


    def ver_todos_os_dados(self):
        con = sqlite3.connect('cep.db')
        cursor = con.cursor()
        cursor.execute("""select * from endereco""")
        for linha in cursor.fetchall():
            print(linha)
        cursor.close()


