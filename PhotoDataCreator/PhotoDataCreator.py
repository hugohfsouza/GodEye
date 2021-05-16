import face_recognition
from sklearn import svm
import os
from io import BytesIO
import datetime
import sys
from progress.bar import Bar
from flask import Flask
from flask import request
from PIL import Image
import uuid
import json
import base64, re
from flask import json
import time

# talvez
import sqlite3

import threading

# from flask_cors import CORS, cross_origin
from flask_cors import CORS


encodings   = []
names       = []

sys.path.append("../")
from DBControl import DBControl

# Conexao com Banco
bancoDados = DBControl();

PATHPERFIS  = '../CapturePhotos/perfis/'
train_dir   = os.listdir(PATHPERFIS)

countAtual           = 0
countEsperado   = 0


def codPerson(folder):
    return folder.split('-')[1]

def countTotalFolder():
    count = 0;
    for person in train_dir:
        count = count+1
    return count;

bar         = Bar('Analyzing photos from folders', max=countTotalFolder());


def analisarDiretorio(person):
    
    global countAtual
    
    folderPerfil = os.listdir(PATHPERFIS+person)
    
    for person_img in folderPerfil:
        print(person_img)
        try:
            if(person_img != ".DS_Store" and person_img != ".gitkeep" ):
                face = face_recognition.load_image_file(PATHPERFIS + person + "/" + person_img)

                try:
                    face_bounding_boxes = face_recognition.face_locations(face)

                    if len(face_bounding_boxes) == 1:
                        face_enc = face_recognition.face_encodings(face)[0]

                        encodings.append(face_enc)
                        names.append(codPerson(person))
                except Exception as e:
                    print(e)

                
        except Exception as e:
            print(e)
        
    countAtual = countAtual + 1

for person in train_dir:
    # print(person)
    if(person != ".DS_Store" and person != ".gitkeep" ):
        countEsperado = countEsperado + 1

for person in train_dir:
    bar.next()

    if(person != ".DS_Store" and person != ".gitkeep" ):
        x = threading.Thread(target=analisarDiretorio, args=(person,))
        x.start()

bar.finish()


clf = svm.SVC(gamma='scale')
clf.fit(encodings,names)


app = Flask(__name__)
CORS(app)

@app.route('/getinfo', methods=['GET'])
def getInfo():

    id = request.args.get('id', default = -1, type = int)

    print(id)
    if(id == -1):
        return app.response_class(
            response=json.dumps({}),
            status=404,
            mimetype='application/json'
        )

    bancoDados2 = DBControl();
    data = bancoDados2.getInformations(id)

    data = {"nome": data[0], "link": data[1]}

    return app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )


@app.route('/reconhecer', methods=['POST'])
def reconhecer():
    y = json.loads(request.data)

    filename    = str(uuid.uuid4())+".png" 
    
    base64_data = re.sub('^data:image/.+;base64,', '', y['file'])
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img.save(filename, "PNG")

    
    imageSearch = face_recognition.load_image_file(filename)

    face_locations = face_recognition.face_locations(imageSearch)
    no = len(face_locations)

    try:
        os.remove(filename)
    except:
        pass

 
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(imageSearch)[i]
        idPerfil = clf.predict([test_image_enc])
        return app.response_class(
            response=json.dumps({"data": {"id":idPerfil[0]}}),
            status=200,
            mimetype='application/json'
        )
    
    return app.response_class(
        response=json.dumps({}),
        status=404,
        mimetype='application/json'
    )


app.run(debug=True, port=5001)


