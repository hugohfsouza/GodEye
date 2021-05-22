
import numpy as np
import sys
from io import BytesIO
from DBControl import DBControl

from flask import Flask
from flask import request
from flask import json
from flask_cors import CORS

import face_recognition
from sklearn import svm
from PIL import Image
import base64, re
import numpy as np
import os
import uuid


bancoDados = DBControl();

encodings   = []
names       = []

lista = bancoDados.getFaceData();

for x in lista:
    encodings.append(np.fromstring(x[2], dtype=float))
    names.append(x[1])
    
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
    except Exception as inst:
        print(inst)
    
 
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(imageSearch)[i]
        idPerfil = clf.predict([test_image_enc])

        print(idPerfil[0])
        return app.response_class(
            response=json.dumps({"data": {"id":int(idPerfil[0])}}),
            status=200,
            mimetype='application/json'
        )
    
    return app.response_class(
        response=json.dumps({}),
        status=404,
        mimetype='application/json'
    )


app.run(debug=True, port=5001)


