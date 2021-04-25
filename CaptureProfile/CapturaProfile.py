from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import sys

sys.path.append("../")
from DBControl import DBControl

import configparser
Config = configparser.ConfigParser()
Config.read("./../config.ini")

# CONFIGS
PATH        = Config.get('Selenium', 'folderDriveSelenium')
EMAIL       = Config.get('FacebookAccount', 'email')
PASSWORD    = Config.get('FacebookAccount', 'password')
NUMBSCROLL  = int(Config.get('Application', 'scroll'))

# Conexao com Banco
bancoDados = DBControl();

def fazerLogin():
    elem = driver.find_element_by_name("email")
    elem.clear()
    elem.send_keys(EMAIL)
    elem = driver.find_element_by_name("pass")
    elem.clear()
    elem.send_keys(PASSWORD)
    elem.send_keys(Keys.RETURN)
    time.sleep(10)

def recuperarPessoas(sourceCode):
    soup        = BeautifulSoup(sourceCode, 'html.parser')
    listaAmigos = soup.find_all("div", class_="bp9cbjyn ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi n1f8r23x rq0escxv j83agx80 bi6gxh9e discj3wi hv4rvrfc ihqw7lf3 dati1w0a gfomwglr")

    print("Achei "+str(len(listaAmigos))+" pessoas a mais ")
    for htmlPessoa in listaAmigos:
        try:
            amigo       = BeautifulSoup(str(htmlPessoa), 'html.parser')
            nomeELink   = amigo.find("a", class_="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8")

            bancoDados.novoPerfil(
                nomeELink.get_text(),
                nomeELink.get('href')
            )

        except:
            print("error");

def acessarPaginaAmigos(link):
    driver.get(link+str("/friends"))

    print(driver.current_url)

    bancoDados.atualizarParaAmigosAnalisados(link)
    time.sleep(3);

    for x in range(0,NUMBSCROLL):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5);

driver = webdriver.Chrome(PATH)
driver.get("http://www.facebook.com.br")
fazerLogin();

while True:
    link = bancoDados.getProximoPerfil()
    acessarPaginaAmigos(link);

    # Capturando os amigos
    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    recuperarPessoas(source_code);
    
    if not link:
        break

driver.close()
