import face_recognition
from sklearn import svm
import os
import datetime
import sys
import json
from json import JSONEncoder
import numpy

sys.path.append("../")
from DBControl import DBControl

# Conexao com Banco
bancoDados = DBControl();

PATHPERFIS = '../CapturePhotos/perfis/perfil-'

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def getDataFromPhotos(id):
    folder      = PATHPERFIS+str(id)
    encodings   = []
    names       = []
    
    if(os.path.exists(folder)):
        train_dir = os.listdir(folder)
        try:
            for person_img in train_dir:
                if(person_img != ".DS_Store" and person_img != ".gitkeep" ):
                    face = face_recognition.load_image_file(folder + "/" + person_img)
                    face_bounding_boxes = face_recognition.face_locations(face)

                    if len(face_bounding_boxes) == 1:
                        face_enc = face_recognition.face_encodings(face)[0]
                        encodings.append(face_enc)
                        names.append(str(id))
        except:
            print("erro processamento das imagens")
            pass
    

    return encodings,names


while True:
    registro = bancoDados.getNextPerfilForAnalyzer()

    if not registro:
        break


    bancoDados.updateFieldPhotoData(registro[0]);

    (encodings, names)  = getDataFromPhotos(registro[0]);
    jsonEncodings       = json.dumps(encodings, cls=NumpyArrayEncoder)
    jsonNames           = json.dumps(names);

    bancoDados.registerEncodingsAndName(registro[0], jsonEncodings, jsonNames);

    print("Perfil Analized: "+str(registro[0]))