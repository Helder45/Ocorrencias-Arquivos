from datetime import datetime

def transforma_str_ascii(nome_inserido, senha_inserida):
    lista_login = []
    lista_senha = []

    for letra_nome in nome_inserido:
        nome_inserido = ord(letra_nome)
        lista_login.append(str(nome_inserido))
        
    for letra_senha in senha_inserida:
        senha_inserida = ord(letra_senha)
        lista_senha.append(str(senha_inserida))

    return lista_login, lista_senha


def carrega_senha():
    with open(caminho_pass_key, "r", encoding="utf-8") as arquivo_senha:
        for linha in arquivo_senha:
            nome = linha
            senha = arquivo_senha.readline()

    return nome, senha
        

def autenticar(caminho_arq, lista_ocorrencias, count, nome_inserido, senha_inserida, lista_log):
    nome_arquivo, senha_arquivo = carrega_senha()
    lista_login, lista_senha = transforma_str_ascii(nome_inserido, senha_inserida)
    lista_nome_arquivo = nome_arquivo.split()
    lista_senha_arquivo = senha_arquivo.split()

    print("\nNome no arquivo: ", lista_nome_arquivo, "\nSenha no arquivo: ", lista_senha_arquivo , "\nNome digitado: ", lista_login, "\nSenha digitada: ", lista_senha)

    if lista_nome_arquivo == lista_login and lista_senha_arquivo == lista_senha:
        lista_ocorrencias, count = carregar_ocorrencias()
        lista_log = carrega_log(lista_log)
        menu_ocorrencias(caminho_arq, lista_ocorrencias, count, lista_log)
    else:
        print("Senha ou Login Incorreto(s)!")


def menu_ocorrencias(caminho_arq, lista_ocorrencias, count, lista_log):
    opcao = 1
    while opcao != 0:
        print("---Menu de Ocorrências---")
        print("1 - Cadastro de ocorrência")
        print("2 - Listar todas ocorrências")
        print("3 - Listar todas ocorrências ativas")
        print("4 - Buscar Ocorrência por título")
        print("5 - Alterar atividade da ocorrência")
        print("6 - Remover Ocorrência")
        print("7 - Listar Ocorrências por mês")
        print("8 - Listar Ocorrências contendo a palavra")
        print("9 - Mostrar Logs do sistema")
        print("0 - Sair")
        opcao = int(input("Entre com a opção>>"))
        if opcao == 1:
            print("---Cadastro---")
            cadastro(lista_ocorrencias, count)
            count += 1
        elif opcao == 2:
            print("---Listagem---")
            listagem(lista_ocorrencias)
        elif opcao == 3:
            print("Listagem[ATIVAS]")
            listagem_ativas(lista_ocorrencias)
        elif opcao == 4:
            print("Busca por título")
            titulo = input("Entre com o título da ocorrência:")
            posicao = buscar_ocorrencia(lista_ocorrencias, titulo)
            if posicao != -1:
                print("***Ocorrência Encontrada!***")
                carregar_ocorrencias()
            else:
                print("Ocorrência não encontrada!")
        elif opcao == 5:
            print("Alteração de Status de Atividade")
            titulo = input("Entre com o título da ocorrência:")
            posicao = buscar_ocorrencia(lista_ocorrencias, titulo)
            if posicao != -1:
                print("***Ocorrência Encontrada!***")
                impressao_ocorrencia(lista_ocorrencias[posicao], posicao)
                resp = input("Deseja alterar a situação da atividade " 
                      "da ocorrência? (sim|não)")
                if resp == "sim":
                    backup = str(lista_ocorrencias[posicao])
                    lista_ocorrencias[posicao]["status"] = not lista_ocorrencias[posicao]["status"]
                    regravar_arquivo(lista_ocorrencias)
                    grava_log(backup, "Alteração", lista_ocorrencias[posicao])
                    print("Alteração realizada com sucesso!")
                else:
                    print("Saindo sem alterações")
            else:
                print("Ocorrência não encontrada!")
        elif opcao == 6:
            print("Remoção de Ocorrência")
            titulo = input("Entre com o título da ocorrência:")
            posicao = buscar_ocorrencia(lista_ocorrencias, titulo)
            if posicao != -1:
                print("***Ocorrência Encontrada!***")
                impressao_ocorrencia(lista_ocorrencias[posicao], posicao)
                resp = input("Deseja remover a ocorrência? (sim|não)")
                if resp == "sim":
                    backup = str(lista_ocorrencias[posicao])
                    lista_ocorrencias.pop(posicao)
                    regravar_arquivo(lista_ocorrencias)
                    grava_log(backup, "Remoção", "")
                    print("Remoção realizada com sucesso!")
                else:
                    print("Saindo sem alterações")
            else:
                print("Ocorrência não encontrada!")
        elif opcao == 7:
            print("Listagem de Ocorrências por mês")
            mes = input("Entre com o mês de ocorrência:")
            lista_m = buscar_ocorrencia_mes(lista_ocorrencias, mes)
            if lista_m:
                print("***Ocorrência(s) Encontrada(s)!***")
                listagem(lista_m)
            else:
                print("Não existem ocorrências para o mês ", mes, "!")
        elif opcao == 8:
            print("Listagem de Ocorrências que contem a palavra:")
            titulo = input("Entre a palavra buscada na ocorrência:")
            lista_m = buscar_ocorrencia_palavra(lista_ocorrencias, titulo)
            if lista_m:
                print("***Ocorrência(s) Encontrada(s)!***")
                listagem(lista_m)
            else:
                print("Não existem ocorrências com a palavra ", titulo, "!")
        elif opcao == 9:
            print("Logs do Sistema!")
            lista_log = buscar_log(lista_log)
            if lista_log != None:
                print("***Logs Encontrados!***")
                print(buscar_log(lista_log))
            else:
                print("Log não encontrado!")
        elif opcao == 0:
            print("Saindo do programa!!!")
        else:
            print("Opção Inválida!")


def cadastro(lista_ocorrencias, count):
    id = count
    titulo = input("Entre com o título da ocorrência:")
    descricao = input("Entre com a descrição da ocorrência:")
    implicacoes = input("Entre com as implicações da ocorrência:")
    em_atividade = input("Está em atividade? (sim|não)")
    status = True if em_atividade == "sim" else False
    data = input("Entre com a data de inclusão:")
    prazo = int(input("Entre com a estimativa de prazo em dias:"))

    ocorrencia = dict(id = id, titulo = titulo, descricao = descricao, implicacoes = implicacoes, status = status, data = data, prazo = prazo)

    lista_ocorrencias.append(ocorrencia)
    grava_ocorrencia(ocorrencia)
    grava_log( "" , "Cadastro", ocorrencia)
    print("Ocorrência cadastrada com sucesso!")


def listagem(lista_ocorrencias):
    tamanho = len(lista_ocorrencias)
    if tamanho > 0:
        print("---Listagem de todas as ocorrências---")
        for i in range(tamanho):
           impressao_ocorrencia(lista_ocorrencias[i], i)  
    else:
        print("Não existem ocorrências cadastradas.")
    

def listagem_ativas(lista_ocorrencias):
    tamanho = len(lista_ocorrencias)
    if tamanho > 0:
        print("---Listagem de todas as ocorrências ativas---")
        existem_ativas = False
        for i in range(tamanho):
            if lista_ocorrencias[i]["status"] == True:
                impressao_ocorrencia(lista_ocorrencias[i], i)
                existem_ativas = True
        if not existem_ativas:
            print("Não existem ocorrências ativas")
                
    else:
        print("Não existem ocorrências cadastradas.")


def impressao_ocorrencia(ocorrencia, i):
    print("###Ocorrência ", i + 1, "###")
    print("Id:", ocorrencia["id"])
    print("Título:",ocorrencia["titulo"])
    print("Descrição:",ocorrencia["descricao"])
    print("Implicações:",ocorrencia["implicacoes"])
    print("Em atividade:", "sim" if ocorrencia["status"] == True else "não")
    print("Data de inclusão: ", ocorrencia["data"])
    print("Prazo (em dias):",ocorrencia["prazo"])


def buscar_ocorrencia(lista_ocorrencias, titulo):
    tamanho = len(lista_ocorrencias)
    if tamanho > 0:
        for i in range(tamanho):
            if lista_ocorrencias[i]["titulo"] == titulo:
                return i
        return -1
    else:
        return -1


def carrega_log(lista_log):
    with open(log_file_path, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            lista_log.append(linha[:len(linha)-1])

    return lista_log


def buscar_log(lista_log):
    tamanho_log = len(lista_log)
    if tamanho_log > 0:
        return lista_log
    else:
        return None

def buscar_ocorrencia_mes(lista_ocorrencias, mes):
    tamanho = len(lista_ocorrencias)
    lista_mes = []
    if tamanho > 0:
        for i in range(tamanho):
            corte_mes = lista_ocorrencias[i]["data"]
            if corte_mes[3:5] == mes:
                lista_mes.append(lista_ocorrencias[i])
        return lista_mes
    else:
        return lista_mes


def buscar_ocorrencia_palavra(lista_ocorrencias, titulo):
    tamanho = len(lista_ocorrencias)
    lista_occ = []
    if tamanho > 0:
        for i in range(tamanho):
            if titulo in lista_ocorrencias[i]["titulo"]:
                lista_occ.append(lista_ocorrencias[i])
        return lista_occ
    else:
        return lista_occ


def grava_ocorrencia(ocorrencia):
    with open(caminho_arq, "a", encoding="utf-8") as arquivo:
        arquivo.write("Id:" + str(ocorrencia["id"]) + "\n")
        arquivo.write("Título:" + ocorrencia["titulo"] + "\n")
        arquivo.write("Descrição:" + ocorrencia["descricao"] + "\n")
        arquivo.write("Implicações:" + ocorrencia["implicacoes"] + "\n")
        status = "sim" if ocorrencia["status"] == True else "não"
        arquivo.write("Status:"+ status + "\n" )
        arquivo.write("Data de inclusão:" + ocorrencia["data"] + "\n")
        arquivo.write("Prazo (em dias):" + str(ocorrencia["prazo"]) + "\n")


def regravar_arquivo(lista_ocorrencias):
    with open(caminho_arq, "w", encoding="utf-8") as arquivo:
        for ocorrencia in lista_ocorrencias:
            grava_ocorrencia(ocorrencia)


def carregar_ocorrencias():
    count = 1
    with open(caminho_arq, "r", encoding="utf-8") as arquivo:
        lista_ocorrencias = []
        for linha in arquivo:
            id = linha # int(linha[3:len(linha)-1])
            titulo = arquivo.readline()
            descricao = arquivo.readline()
            implicacoes = arquivo.readline()
            status = arquivo.readline()
            data = arquivo.readline()
            prazo = arquivo.readline()

            ocorrencia = dict(id = id[3:len(id)-1], titulo = titulo[7: len(titulo)-1], descricao = descricao[10:len(descricao)-1], implicacoes = implicacoes[12:len(implicacoes)-1], status = True if status[7:len(status)] == "sim\n" else False, data = data[17:len(data)-1], prazo = prazo[16:len(prazo)-1])

            count += int(ocorrencia["id"]) + 1
            lista_ocorrencias.append(ocorrencia)

    return lista_ocorrencias, count


def grava_log(backup, log_msg, ocorrencia):
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        if log_msg == "Cadastro":
            log_file.write("Log - " + data_e_hora_em_texto + " - [" + log_msg + "] Foi cadastrado a ocorrência: " + str(ocorrencia) + "\n")
        elif log_msg == "Remoção":
            log_file.write("Log - " + data_e_hora_em_texto + " - [" + log_msg + "] Foi removida a ocorrência: " + str(ocorrencia) + "\n")
        elif log_msg == "Alteração":
            log_file.write("Log - " + data_e_hora_em_texto + " - [" + log_msg + "] Foi alterada a ocorrência, de" + backup + " para: " + str(ocorrencia) + "\n")

################execução################

count = 0
lista_ocorrencias = []
lista_log = []
caminho_pass_key = "pass_keys.txt"
caminho_arq = "ocorrencias.txt"
log_file_path = "log.txt"

print("\nSeja bem-vindo ao Galaxy News!")
print("\n<<<Para que possa entrar no sistema, faça o login abaixo>>>")
print("\n##########Login##########")
meu_nome = input("Digite seu e-mail: ")
minha_senha = input("Digite sua senha: ")
print("##########################")
autenticar(caminho_arq, lista_ocorrencias, count, meu_nome, minha_senha, lista_log)