import mysql.connector
import configparser

Config = configparser.ConfigParser()
Config.read("./config.ini")

class DBControl():

    def __init__(self):
        self.conn = mysql.connector.connect(
            user        = Config.get('MYSQL', 'user'), 
            password    = Config.get('MYSQL', 'password'),
            host        = Config.get('MYSQL', 'host'),
            database    = Config.get('MYSQL', 'database')
        )
        self.cursor = self.conn.cursor();

        # self.novoPerfil(Config.get('FacebookAccount', 'myName') ,  Config.get('FacebookAccount', 'myPerfil') )

    # PASSO 1
    def novoPerfil(self, nome, link):
        try:
            self.cursor.execute("""INSERT INTO pessoas (nome, linkFacebook) VALUES (%s,%s)""", (nome, link) )
            self.conn.commit()  
        except:
            print("erro ao inserir novo perfil")

    def atualizarParaAmigosAnalisados(self, link):
        self.cursor.execute("""UPDATE pessoas SET novo = 0 WHERE linkFacebook = %s """, (link, ) )
        self.conn.commit()

    def getProximoPerfilReconhecimento(self):
        linhas = self.cursor.execute("""SELECT linkFacebook FROM pessoas where novo = 1 limit 1;""")
        return self.cursor.fetchone()



    # PASSO 2
    def getProximoPerfilReconhecimento(self):
        linhas = self.cursor.execute("""SELECT linkFacebook, id, nome FROM pessoas where fotoPerfilAnalisada = 0 limit 1; """)
        return self.cursor.fetchone()

    def atualizarParaBuscando(self, link):
        self.cursor.execute("""UPDATE pessoas SET fotoPerfilAnalisada = 1 WHERE linkFacebook = %s """, (link,) )
        self.conn.commit()


    # PASSO 3
    def salvarInformacoesFoto(self, pessoa_id, dataInString):
        self.cursor.execute("""INSERT INTO reconhecimentos (pessoa_id, dados_imagem) VALUES (%s,%s)""", (pessoa_id, dataInString) )
        self.conn.commit()  


    # PASSO 4
    def getFaceData(self):
        arrayRetorno = [];
        linhas = self.cursor.execute("""SELECT id, pessoa_id, dados_imagem FROM reconhecimentos; """)
        for linha in self.cursor.fetchall():
            arrayRetorno.append(linha)

        return arrayRetorno;

    def getInformations(self, id):
        people = self.cursor.execute("""SELECT nome, linkfacebook FROM pessoas where id = %s """, (id,))
        return self.cursor.fetchone();