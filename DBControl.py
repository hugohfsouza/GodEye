import sqlite3
import configparser


Config = configparser.ConfigParser()
Config.read("./../config.ini")

class DBControl():

    def __init__(self):
        self.nomeArquivo = Config.get('DataBase', 'filename') 
        self.conn = sqlite3.connect(self.nomeArquivo)
        self.cursor = self.conn.cursor();

    def criarBanco(self):
        self.cursor.execute("""
        CREATE TABLE pessoas (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                linkFacebook TEXT NOT NULL,
                novo boolean DEFAULT TRUE
        );
        """)
        self.novoPerfil(Config.get('FacebookAccount', 'myName') ,  Config.get('FacebookAccount', 'myPerfil') )
        

    def novoPerfil(self, nome, link):
        if(not self.verificaPerfilExistente(link)):
            self.cursor.execute("""INSERT INTO pessoas (nome, linkFacebook) VALUES (?,?)""", (nome, link) )
            self.conn.commit()
            # self.conn.close()


    def getProximoPerfil(self):
        retorno = "";
        linhas = self.cursor.execute("""SELECT linkFacebook FROM pessoas where novo = 1 limit 1;""")
        for linha in self.cursor.fetchall():
            retorno = linha[0]

        return retorno;



    def getProximoPerfilReconhecimento(self):
        retorno = "";
        # linhas = self.cursor.execute("""SELECT linkFacebook FROM pessoas where novo = 1; """)
        # for linha in self.cursor.fetchall():
        #     retorno = linha[0]

        return retorno;

    def verificaPerfilExistente(self, link):
        linhas = self.cursor.execute("""
        SELECT 1 FROM pessoas where linkFacebook = ? 
        """, (link,))

        if(self.cursor.fetchall() == []):
            return False
        else:
            return True

    def atualizarParaBuscando(self, link):
        self.cursor.execute("""UPDATE pessoas SET novo = 0 WHERE linkFacebook = ? """, [link] )
        self.conn.commit()




# gerenciador = DBControl();
# gerenciador.criarBanco();
# print(gerenciador.verificaPerfilExistente("https://www.facebook.com/hugohfsouza"))


        

