import face_recognition
from sklearn import svm
import os
import datetime
import sys

sys.path.append("../")
from DBControl import DBControl

encodings   = []
names       = []

PATHPERFIS = '../CapturePhotos/perfis/'
train_dir = os.listdir(PATHPERFIS)

# Conexao com Banco
bancoDados = DBControl();


def codPerson(folder):
    return folder.split('-')[1]

for person in train_dir:
    if(person != ".DS_Store" and person != ".gitkeep" ):
        folderPerfil = os.listdir(PATHPERFIS+person)

        for person_img in folderPerfil:
            if(person_img != ".DS_Store" and person_img != ".gitkeep" ):
                face = face_recognition.load_image_file(PATHPERFIS + person + "/" + person_img)
                face_bounding_boxes = face_recognition.face_locations(face)

                if len(face_bounding_boxes) == 1:
                    face_enc = face_recognition.face_encodings(face)[0]
                    encodings.append(face_enc)
                    names.append(codPerson(person))


print(face_enc)

# clf = svm.SVC(gamma='scale')
# clf.fit(encodings,names)

# print("Finish" + str(datetime.datetime.now()))

# test_image = face_recognition.load_image_file('foto.jpg')


# face_locations = face_recognition.face_locations(test_image)
# no = len(face_locations)


# for i in range(no):
#     test_image_enc = face_recognition.face_encodings(test_image)[i]
#     idPerfil = clf.predict([test_image_enc])
#     print(idPerfil)