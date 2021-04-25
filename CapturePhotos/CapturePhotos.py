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
from sklearn import svm
import uuid
import configparser

import threading

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
    
    time.sleep(1);
    for x in range(0,NUMBSCROLL):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1);

def criarPastaPerfil(nome, id):
    pasta = FOLDER+str(id)

    if not  os.path.isdir(pasta):
        os.mkdir(pasta)

def deletarFotosErradas(folder):
    encodings   = []
    names       = []
    
    enderecoFotoMain = folder+"/main.jpg"

    if( not os.path.isfile(enderecoFotoMain)):
        return;


    face = face_recognition.load_image_file(enderecoFotoMain)
    face_bounding_boxes = face_recognition.face_locations(face)
    if len(face_bounding_boxes) == 1:
        face_enc = face_recognition.face_encodings(face)[0]
        encodings.append(face_enc)
        names.append("1")


    face = face_recognition.load_image_file(enderecoFotoMain)
    face_bounding_boxes = face_recognition.face_locations(face)
    if len(face_bounding_boxes) == 1:
        face_enc = face_recognition.face_encodings(face)[0]
        encodings.append(face_enc)
        names.append("2")

    clf = svm.SVC(gamma='scale')
    clf.fit(encodings,names)

    train_dir   = os.listdir(folder)
    for photo in train_dir:
        imageSearch = face_recognition.load_image_file(folder+"/"+photo)
        face_locations = face_recognition.face_locations(imageSearch)
        no = len(face_locations)
        for i in range(no):
            test_image_enc = face_recognition.face_encodings(imageSearch)[i]
            idPerfil = clf.predict([test_image_enc])
            # print(str(idPerfil[0])+ "   "+ str(photo) )


def saveImages(imageList, id, nome, tagLink):
    criarPastaPerfil(nome, id)

    for foto in imageList:
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
            print(e)
            pass
            
        try:
            os.remove(filename)
        except Exception as e:
            print(e)
            pass

    

def capturarFotos(nome, id):
    time.sleep(3)
    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    soup        = BeautifulSoup(source_code, 'html.parser')
    
    mageListImg = soup.find_all("img")
    print(len(mageListImg))

    x = threading.Thread(target=saveImages, args=(mageListImg, id, nome, "src"))
    x.start()
    time.sleep(10)


    
driver = webdriver.Chrome(PATH)
driver.get("http://www.facebook.com.br")
fazerLogin();

while True:
    people = bancoDados.getProximoPerfilReconhecimento()
    acessarPaginaFotos(people[0]);
    capturarFotos(people[2], people[1]);

    if not people[0]:
        break

