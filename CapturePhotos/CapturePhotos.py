from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import os
import requests
import shutil
from bs4 import BeautifulSoup

sys.path.append("../")
from DBControl import DBControl

from PIL import Image
import face_recognition
import uuid
import configparser


Config = configparser.ConfigParser()
Config.read("./../config.ini")



# CONFIGS
PATH        = Config.get('Selenium', 'folderDriveSelenium')
EMAIL       = Config.get('FacebookAccount', 'email')
PASSWORD    = Config.get('FacebookAccount', 'password')
NUMBSCROLL  = int(Config.get('Application', 'scroll'))

FOLDER = Config.get('Application', 'folderAllPerfil')

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


def acessarPaginaFotos(link):
    driver.get(link+str("/photos_all"))
    bancoDados.atualizarParaBuscando(link)

    for x in range(0,NUMBSCROLL):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1);

    # time.sleep(30000);


def criarPastaPerfil(nome, id):
    pasta = FOLDER+str(id)

    if not  os.path.isdir(pasta):
        os.mkdir(pasta)


def capturarFotos(nome, id):
    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    soup        = BeautifulSoup(source_code, 'html.parser')
    imageList = soup.find_all("img")

    for foto in imageList:
        filename                = str(uuid.uuid4())+".jpg"
        try:
            r                       = requests.get(foto.get('src'), stream = True)
            r.raw.decode_content    = True

            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)

            image           = face_recognition.load_image_file(filename)
            face_locations  = face_recognition.face_locations(image)

            criarPastaPerfil(nome, id)

            # time.sleep(3000000)
            pasta = FOLDER+str(id)
            for face_location in face_locations:
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                
                
                pasta = pasta+"/"+filename
                pil_image.save(pasta, "PNG")


            

        except:
            print("error")
            pass
            
        try:
            os.remove(filename)
        except:
            pass
        




driver = webdriver.Chrome(PATH)
driver.get("http://www.facebook.com.br")
fazerLogin();


while True:
    people = bancoDados.getProximoPerfilReconhecimento()
    acessarPaginaFotos(people[0]);
    capturarFotos(people[2], people[1]);

    if not people[0]:
        break