from PyQt5 import uic,QtWidgets # Importando o módulo do PyQt5 uic para ler o arquivo ui e 
                                # QtWidgets para montar os elementos na tela
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0 # Global

#criando variável para receber uma instância do mysql connector do metodo connect fazendo a conexão com o banco
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql",
    database="cadastro_produtos"
)

def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute( "SELECT * FROM produtos WHERE id =" +  str ( valor_id ))
    produto = cursor.fetchall()
    tela_editar.show() 
    # retornando a linha que precisa , e na proxima linha de código -> retornando todos os produtos com id e valor
    # aparecendo a tela, após mudar o texto que foi inserido
    

    tela_editar.lineEdit.setText(str(produto[0][0])) # Colocando um texto que foi recuperado e convertendo no texto
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    numero_id = valor_id

def salvar_dados_editados():
    #pega o número da ID
    global numero_id # necessário par fazer a logica da função
    #valor digitado no lineEdit
    codigo = tela_editar.lineEdit_2.text() #ler o que foi passado
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    #Atualizar os dados no banco
    cursor = banco.cursor() # Declarando o cursor para excutar o banco de dados
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = {}".format(codigo, descricao, preco, categoria, numero_id)) # query para atualizar o banco, alterando e fazendo update, lendo tudo que foi digitado, e salvar no banco de dados

    # Atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    chama_tela() # atualizando em tempo real




def excluir_dados(): # excluindo os itens da tabela
    linha = segunda_tela.tableWidget.currentRow() #Selecionando a linha desejável a ser excluida
    segunda_tela.tableWidget.removeRow(linha) # excluindo a linha conforme selecionado

    cursor = banco.cursor() #Criando a variavel para manipular o bd
    cursor.execute("SELECT id FROM produtos") # pegando os IDS para salvar no vetor
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0] # retornar somente o ID que desejamos excluir no banco
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id)) # Excluir no banco de dados (converter o valor ID para string para o execute entender)
    print(valor_id) # Teste

def  gerar_pdf ():
    cursor  =  banco.cursor () # Iniciando o cursor do BD
    comando_SQL  =  "SELECT * FROM produtos" # ler todos  os produtos da tabela
    cursor.execute ( comando_SQL ) # executar a query no banco de dados
    dados_lidos  =  cursor.fetchall () # salvar na variavel dados lidos
    y  =  0 # Usar na hora de escrever no PDF 
    pdf  =  canvas.Canvas ( "cadastro_produtos.pdf" )# Iniciando o objeto do canvas (especificando para salvar na pasta)
    pdf.setFont ( "Times-Bold" , 25 ) # Definindo o titulo com tamanho e cor
    pdf.drawString ( 200 , 800 , "Produtos cadastrados:" )# Posição de escrita no PDF POSIÇÃO X E Y
    pdf.setFont ( "Times-Bold" , 18 ) # Diminuindo o tamanho

    pdf.drawString ( 10 , 750 , "ID" ) # Colocando descrição nas colunas
    pdf.drawString ( 110 , 750 , "CODIGO" )
    pdf.drawString ( 210 , 750 , "PRODUTO" )
    pdf.drawString ( 310 , 750 , "PREÇO" )
    pdf.drawString ( 410 , 750 , "CATEGORIA" )

    for  i  in  range( 0 , len ( dados_lidos )): # fazer o for no tamanho dos dados que tem
        y  =  y  +  50 # Escrevendo os dados e pulando as linhas
        pdf.drawString ( 10 , 750  -  y , str ( dados_lidos [ i ] [ 0 ])) # convertendo para string os dados lidos para posição y, 0 até 4 valores da coluna
        pdf.drawString ( 110 , 750  -  y , str ( dados_lidos [ i ] [ 1 ]))
        pdf.drawString ( 210 , 750  -  y , str ( dados_lidos [ i ] [ 2 ]))
        pdf.drawString ( 310 , 750  -  y , str ( dados_lidos [ i ] [ 3 ]))
        pdf.drawString ( 410 , 750  -  y , str ( dados_lidos [ i ] [ 4 ]))

    pdf.save() # PDF criado com sucesso
    print( "PDF FOI GERADO COM SUCESSO!" )

#Criando a função principal

def funcao_principal():  # função principal para ler os campos, disparada pelo botão

    linha1 = formulario.lineEdit.text() #Ler o que foi digitado no formulário ( pegar o primeiro campo)
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    categoria=""

    if formulario.radioButton.isChecked(): #Verificando se o radio button foi clicando retornando true or false
        print("Categoria Informática foi selecionado ")
        categoria="Informática"
    
    elif formulario.radioButton_2.isChecked():
        print("Categoria Alimentos foi selecionado ")
        categoria="Alimentos"

    else:
        print("Categoria Eletrônicos foi selecionado ")
        categoria="Eletrônicos" # cada vez que o push button for clicado ele vai entrar na função principal sendo zerada por receber a string vazia
                                # verificando qual foi selecionada e salvando a string certa dentro da variável

    

    print("Código do Produto : ",linha1) # Verificando se esta funcionando
    print("Descrição do Produto : ",linha2)
    print("Preço do Produto : ",linha3)

    cursor = banco.cursor() #Criando um cursor para usar a insância da variavel banco
    comando_SQL = " INSERT INTO produtos (CODIGO, descricao, preco, categoria) VALUES (%s, %s, %s,%s) " #String definindo o  comando que vai ser utilizado no banco
    dados = (str(linha1), str(linha2), str(linha3), categoria) #str convertendo a variavel para string para passar para a variavel dados
    cursor.execute(comando_SQL, dados) # recebendo o comando SQL que vai ser digitado, substituindo por uma string no segundo parametro
    banco.commit() # para final ir para o banco

    formulario.lineEdit.setText("") #Limpando o campo de digitação
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")


def chama_tela():
    segunda_tela.show() #Apresentando nova tela

    cursor = banco.cursor() # Ler os dados do BD
    comando_SQL = "SELECT * FROM produtos" # Ler a tabela produtos criada
    cursor.execute(comando_SQL) # Executando o comando criado na variavel
    dados_lidos = cursor.fetchall() # pegar o que foi feito na ultima linha do cursor, leu todos os dados do banco salvando na variavel dados_lidos
    #print(dados_lidos[0][0]) # verificando se ocorreu tudo certo

    segunda_tela.tableWidget.setRowCount(len(dados_lidos)) # pegando a segunda tela com a tabela usando o setRowCount 
                                                           #para saber quantas linhas vai ter a tabela(parametro tudo que ele leu e recuperou pegando o tamanho para saber a quantidade de linhas)
    segunda_tela.tableWidget.setColumnCount(5) # Definindo o número de colunas(são sempre fixas), fazendo aparecer a tabela na janela do windows

    #Salvando o elemento

    for i in range(0, len(dados_lidos)): # de 0 até o tamanho de numero de linhas
        for j in range(0, 5): # de 0 a 5 pois o número de colunas é sempre fixo
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) # padrão por percorrer a matriz passando por todas linhas e colunas
                                                                                                       # passando a posição para inserir esse elemento na tabela, depois passando o elemento que queremos que seja inserido na tabela (elemento I J para percorrer todas posições novamente )
                                                                                                       # colocando str para converter pois só aceita string e contém elementos inteiros sendo necessário a conversão

    



app=QtWidgets.QApplication([]) # Objeto app utilizando a classe widgets e criando a aplicação
formulario=uic.loadUi("formulario.ui") # Carregando o arquivo(importando o formulario)
segunda_tela=uic.loadUi("listar_dados.ui") # Carregando a nova tela( usando o modulo UIC do metodo LOAD de PyQt5)
tela_editar=uic.loadUi("menu_editar.ui")
formulario.pushButton.clicked.connect(funcao_principal) # referência de objeto(clicando no botão chama a função)
formulario.pushButton_2.clicked.connect(chama_tela) # Ao ser clicado vai chamar a segunda tela
segunda_tela.pushButton.clicked.connect(gerar_pdf) # Criando o botão para gerar o PDF da segunda dela de tabelas
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados) # botão salvar para incluir e editar



formulario.show() # chamando o aplicativo para apresentar na tela
app.exec() #executando o mesmo para teste ou utilização

