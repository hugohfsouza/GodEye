import face_recognition
# from sklearn import svm
import os
# import sys
from PIL import Image
# import uuid
# import json
# import base64, re
import numpy as np


encodings   = []
names       = []

from DBControl import DBControl

# Conexao com Banco
bancoDados = DBControl();

PATHPERFIS  = './perfis/'
train_dir   = os.listdir(PATHPERFIS)


def codPerson(folder):
    return folder.split('-')[1]

def analisarDiretorio(person):
    
    folderPerfil = os.listdir(PATHPERFIS+person)
    
    for person_img in folderPerfil:
        try:
            if(person_img != ".DS_Store" and person_img != ".gitkeep" ):
                print(person_img)

                face = face_recognition.load_image_file(PATHPERFIS + person + "/" + person_img)

                try:
                    face_bounding_boxes = face_recognition.face_locations(face)

                    if len(face_bounding_boxes) == 1:
                        face_enc = face_recognition.face_encodings(face)[0]

                        dadoEmByte = face_enc.tobytes()

                        encodingInString = face_enc.tostring()

                        # TO-DO -> Bloquear para que nao seja salvo duas vezes a mesma foto
                        bancoDados.salvarInformacoesFoto(codPerson(person), encodingInString)

                        # print(np.fromstring(string, dtype=float))
                        
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    



for person in train_dir:
    if(person != ".DS_Store" and person != ".gitkeep" ):
        analisarDiretorio(person)




