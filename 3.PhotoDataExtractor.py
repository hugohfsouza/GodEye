import face_recognition
from sklearn import svm
import os
import numpy as np
import configparser
from DBControl import DBControl
import mysql.connector

Config = configparser.ConfigParser()
Config.read("./config.ini")

FOLDER      = Config.get('Application', 'folderAllPerfil')
FOLDER = './'+FOLDER+'/'
conexaobancoDados = DBControl();

encodings = []
names = []

train_dir = os.listdir(FOLDER)

for idPessoa in train_dir:
    if idPessoa != ".gitkeep":
        pix = os.listdir(FOLDER + idPessoa)

        for person_img in pix:
            if person_img != ".gitkeep":

                face = face_recognition.load_image_file(FOLDER + idPessoa + "/" + person_img)
                face_bounding_boxes = face_recognition.face_locations(face)

                #If training image contains exactly one face
                if len(face_bounding_boxes) == 1:
                    face_enc = face_recognition.face_encodings(face)[0]
                    bf = face_enc.tostring()

                    conexaobancoDados.cursor.execute("""INSERT INTO rosto (pessoa_id, byte) VALUES (%s,%s)""", (idPessoa,bf) )
                    conexaobancoDados.conn.commit()

                    # teste2 = np.fromstring(bf, dtype=int)
                    # print(type(face_enc.tostring()))
                    # print(type(bf))
                    # exit()
                    # encodings.append(teste2)
                    # names.append(person)
                else:
                    print(idPessoa + "/" + person_img + " was skipped and can't be used for training")
