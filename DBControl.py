import sqlite3
import configparser

Config = configparser.ConfigParser()
Config.read("./../config.ini")

class DBControl():

    def __init__(self):
        self.nomeArquivo = Config.get('DataBase', 'filename') 
        self.conn = sqlite3.connect(self.nomeArquivo)
        self.cursor = self.conn.cursor();

        self.verifyDatabase();

        self.verifyAlterDatabase();

    def verifyAlterDatabase(self):
        pass

    def verifyDatabase(self):
        exist = False
        linhas = self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='pessoas';""")
        
        for linha in self.cursor.fetchall():
            exist = True
        
        if(not exist):
            self.criaTabelaPessoas();


    def criaTabelaPessoas(self):
        self.cursor.execute("""
        CREATE TABLE pessoas (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                linkFacebook TEXT NOT NULL,
                novo boolean DEFAULT TRUE,
                fotoPerfilAnalisada boolean DEFAULT FALSE
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
        linhas = self.cursor.execute("""SELECT linkFacebook, id, nome FROM pessoas where fotoPerfilAnalisada = 0 limit 1; """)
        for linha in self.cursor.fetchall():
            retorno = linha

        return retorno;

    def verificaPerfilExistente(self, link):
        linhas = self.cursor.execute("""
        SELECT 1 FROM pessoas where linkFacebook = ? 
        """, (link,))

        if(self.cursor.fetchall() == []):
            return False
        else:
            return True
        
    def atualizarParaAmigosAnalisados(self, link):
        self.cursor.execute("""UPDATE pessoas SET novo = 0 WHERE linkFacebook = ? """, [link] )
        self.conn.commit()

    def atualizarParaBuscando(self, link):
        self.cursor.execute("""UPDATE pessoas SET fotoPerfilAnalisada = 1 WHERE linkFacebook = ? """, [link] )
        self.conn.commit()

    def getInformations(self, id):
        result = []
        peoples = self.cursor.execute("""
        SELECT nome, linkfacebook FROM pessoas where id = ? 
        """, (id,))

        for people in self.cursor.fetchall():
            result = people
        
        return result;
