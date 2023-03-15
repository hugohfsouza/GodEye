from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import requests
import shutil
from bs4 import BeautifulSoup
from DBControl import DBControl
from PIL import Image
import uuid
import configparser


Config = configparser.ConfigParser()
Config.read("./config.ini")

# CONFIGS
PATH        = Config.get('Selenium', 'folderDriveSelenium')
EMAIL       = Config.get('FacebookAccount', 'email')
PASSWORD    = Config.get('FacebookAccount', 'password')
NUMBSCROLL  = int(Config.get('Application', 'scroll'))
FOLDER      = Config.get('Application', 'folderAllPerfil')

# Conexao com Banco
conexaobancoDados = DBControl();

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


def proximoPerfil():
    linhas = conexaobancoDados.cursor.execute("""SELECT id, linkFacebook FROM pessoas where status = 'amigos-extraidos' limit 1;""")
    item = conexaobancoDados.cursor.fetchone()
    
    return item['linkFacebook'], item['id']

def acessarPaginaFotos(link):

    if('profile.php?id=' in link):
        driver.get(link+str("&sk=photos"))
    else:
        driver.get(link+str("/photos_albums"))

    elem        = driver.find_element(By.XPATH, '//*')
    sourceCode  = elem.get_attribute("outerHTML")
    soup        = BeautifulSoup(sourceCode, 'html.parser')
    albuns       = soup.find_all("div", class_="x9f619 x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6")
    linkAlbumPessoal = ""
    for album in albuns:
        tagA = album.select("a")
        achouAlbumPerfil = 0
        if len(tagA) > 0:
            tagsSpan = album.select("span")
            for tagSpan in tagsSpan:
                if(tagSpan.text == "Fotos do perfil"):
                    achouAlbumPerfil = 1
                    linkAlbumPessoal = tagA[0]['href']

    if linkAlbumPessoal != "":
        driver.get(linkAlbumPessoal)

    
        time.sleep(1);
        for x in range(0,NUMBSCROLL):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1);

def criarPastaPerfil(id):
    pasta = FOLDER+"/"+str(id)

    if not os.path.isdir(pasta):
        os.mkdir(pasta)

def saveImages(imageList, idPessoa):
    criarPastaPerfil(idPessoa)

    for foto in imageList:
        tagImage = foto.find_all("img")
        if len(tagImage) > 0:
            filename = FOLDER+"/"+str(idPessoa)+"/"+str(uuid.uuid4())+".jpg"
            r = requests.get(tagImage[0].get("src"), stream = True)
            r.raw.decode_content    = True

            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)

    atualizaPerfil(idPessoa)



def atualizaPerfil(id):
    conexaobancoDados.cursor.execute("""UPDATE pessoas set status='fotos-extraidas' where id = %s""", (id, ) )
    conexaobancoDados.conn.commit() 
 

def capturarFotos(idPessoa):
    time.sleep(6)
    elem        = driver.find_element(By.XPATH, '//*')
    sourceCode  = elem.get_attribute("outerHTML")
    soup        = BeautifulSoup(sourceCode, 'html.parser')
    imageListImg = soup.find_all("div", class_="x1vtvx1t x6ffb70 x1e56ztr x1emribx x1n2onr6")
    
    saveImages(imageListImg, idPessoa)

    # atualizaPerfil(idPessoa)


    
driver.get("http://www.facebook.com.br")
fazerLogin();

while True:
    linkFacebook, idPessoa = proximoPerfil()

    if not linkFacebook:
        exit()
    else:
        acessarPaginaFotos(linkFacebook);
        capturarFotos(idPessoa);
        