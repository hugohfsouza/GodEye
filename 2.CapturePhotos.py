from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
import shutil
from bs4 import BeautifulSoup

from DBControl import DBControl

from PIL import Image
import face_recognition
from sklearn import svm
import uuid
import configparser

import threading

Config = configparser.ConfigParser()
Config.read("./config.ini")

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

    if('profile.php?id=' in link):
        driver.get(link+str("&sk=photos"))
    else:
        driver.get(link+str("/photos_all"))
    bancoDados.atualizarParaBuscando(link)
    
    time.sleep(1);
    for x in range(0,NUMBSCROLL):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1);

def criarPastaPerfil(nome, id):
    pasta = FOLDER+str(id)

    if not  os.path.isdir(pasta):
        os.mkdir(pasta)

def saveImages(imageList, id, nome, tagLink):
    criarPastaPerfil(nome, id)
    total = 0;

    try:
        for foto in imageList:
            if(total <= 100):
                total = total+1
                if(foto.get('preserveaspectratio') == "xMidYMid slice" and foto.get('style') == "height: 168px; width: 168px;"):
                    filename                = "main.jpg"
                else:
                    filename                = str(uuid.uuid4())+".jpg"
            
                try:
                    r                       = requests.get(foto.get(tagLink), stream = True)
                    r.raw.decode_content    = True

                    with open(filename,'wb') as f:
                        shutil.copyfileobj(r.raw, f)

                    image           = face_recognition.load_image_file(filename)
                    face_locations  = face_recognition.face_locations(image)

                    for face_location in face_locations:
                        pasta = FOLDER+str(id)+"/"+filename

                        top, right, bottom, left = face_location
                        face_image = image[top:bottom, left:right]
                        pil_image = Image.fromarray(face_image)
                        
                        
                        pil_image.save(pasta, "PNG")
                except Exception as e:
                    print("error")
                    pass
                    
                try:
                    os.remove(filename)
                except Exception as e:
                    print("error")
                    pass

    except Exception as e:
        print("error")
        pass

def capturarFotos(nome, id):
    time.sleep(3)
    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    soup        = BeautifulSoup(source_code, 'html.parser')
    
    mageListImg = soup.find_all("img")
    print(len(mageListImg))

    saveImages(mageListImg, id, nome, "src")


    
driver = webdriver.Chrome(PATH)
driver.get("http://www.facebook.com.br")
fazerLogin();

while True:
    people = bancoDados.getProximoPerfilReconhecimento()
    
    if not people[0]:
        time.sleep(10)
    else:
        acessarPaginaFotos(people[0]);
        capturarFotos(people[2], people[1]);
        print(str(people[2])+" Concluido")



    

