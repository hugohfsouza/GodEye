import face_recognition
from sklearn import svm
import os
import numpy as np
import configparser
from DBControl import DBControl
import mysql.connector

Config = configparser.ConfigParser()
Config.read("./config.ini")


conexaobancoDados = DBControl();

encodings = []
names = []


conexaobancoDados.cursor.execute("""
    select pessoas.nomePerfil, rosto.byte
	from rosto
    inner join pessoas on (pessoas.id = rosto.pessoa_id)
    where pessoas.id in (1,2,3,4)   
    order by pessoas.nomePerfil""")

itens = conexaobancoDados.cursor.fetchall()

for x in itens:
    foto = np.fromstring(x['byte'], dtype=int)
    encodings.append(foto)
    names.append(x['nomePerfil'])

clf = svm.SVC(gamma='scale')
clf.fit(encodings,names)

# print(names)
# exit()


test_image = face_recognition.load_image_file('teste_satin.jpg')

face_locations = face_recognition.face_locations(test_image)
no = len(face_locations)

for i in range(no):
    test_image_enc = face_recognition.face_encodings(test_image)[i]
    name = clf.predict([test_image_enc])
    print(*name)