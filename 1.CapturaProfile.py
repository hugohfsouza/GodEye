from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from DBControl import DBControl
import configparser

Config = configparser.ConfigParser()
Config.read("./config.ini")

# CONFIGS
PATH            = Config.get('Selenium', 'folderDriveSelenium')
EMAIL           = Config.get('FacebookAccount', 'email')
PASSWORD        = Config.get('FacebookAccount', 'password')
NUMBSCROLL      = int(Config.get('Application', 'scroll'))
PERFIL_INICIAL  = Config.get('FacebookAccount', 'myPerfil')

# Conexao com Banco
conexaobancoDados = DBControl();

useScrollOnFriendsPage= True


if(PATH):
    driver = webdriver.Chrome(PATH)
else:
    driver = webdriver.Chrome()





def fazerLogin():
    elem = driver.find_element(By.NAME, 'email')
    elem.clear()
    elem.send_keys(EMAIL)
    elem = driver.find_element(By.NAME, 'pass')
    elem.clear()
    elem.send_keys(PASSWORD)
    elem.send_keys(Keys.RETURN)
    time.sleep(10)

def perfilJaExiste(linkPerfil):
    linhas = conexaobancoDados.cursor.execute("""SELECT 1 FROM pessoas where linkFacebook = %s limit 1;""", (linkPerfil,))
    item = conexaobancoDados.cursor.fetchone()
    
    if(item == None):
        return True
    else:
        return False
    


def recuperarPessoas(sourceCode):
    soup        = BeautifulSoup(sourceCode, 'html.parser')
    listaAmigos = soup.find_all("div", class_="x1iyjqo2 x1pi30zi")

    for htmlPessoa in listaAmigos:
        amigo       = BeautifulSoup(str(htmlPessoa), 'html.parser')
        
        linkPerfil   = amigo.select("a")[0]['href']
        nome        = amigo.select("span")[0].text

        if(perfilJaExiste(linkPerfil)):
            conexaobancoDados.cursor.execute("""INSERT INTO pessoas (nomePerfil, linkFacebook) VALUES (%s,%s)""", (nome, linkPerfil) )
            conexaobancoDados.conn.commit()
            print("adicionado " + nome)


def acessarPaginaAmigos(link):
    if('profile.php?id=' in link):
        driver.get(link+str("&sk=friends"))
    else:
        driver.get(link+str("/friends"))

    print(driver.current_url)
    time.sleep(3);

    if(useScrollOnFriendsPage):
        for x in range(0,NUMBSCROLL):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5);


def proximoPerfil():
    linhas = conexaobancoDados.cursor.execute("""SELECT id, linkFacebook FROM pessoas where status = 'novo' limit 1;""")
    item = conexaobancoDados.cursor.fetchone()
    
    if(item == None):
        return PERFIL_INICIAL
    else:
        return item['linkFacebook'], item['id']


def atualizaPerfil(id):
    conexaobancoDados.cursor.execute("""UPDATE pessoas set status='amigos-extraidos' where id = %s""", (id, ) )
    conexaobancoDados.conn.commit()

driver.get("http://www.facebook.com.br")
fazerLogin();

while True:
    link, id = proximoPerfil()
    acessarPaginaAmigos(link);
   

    # Capturando os amigos
    elem = driver.find_element(By.XPATH, '//*')
    source_code = elem.get_attribute("outerHTML")
    recuperarPessoas(source_code);

    atualizaPerfil(id)

    if not link:
        break

driver.close()
