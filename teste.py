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

train_dir = os.listdir('./perfis/')

for person in train_dir:
    if person != ".gitkeep":
        pix = os.listdir("./perfis/" + person)

        for person_img in pix:
            if person_img != ".gitkeep":

                # Get the face encodings for the face in each image file
                face = face_recognition.load_image_file("./perfis/" + person + "/" + person_img)
                face_bounding_boxes = face_recognition.face_locations(face)

                #If training image contains exactly one face
                if len(face_bounding_boxes) == 1:
                    face_enc = face_recognition.face_encodings(face)[0]
                    encodings.append(face_enc)
                    names.append(person)
                else:
                    print(person + "/" + person_img + " was skipped and can't be used for training")




clf = svm.SVC(gamma='scale')
clf.fit(encodings,names)

test_image = face_recognition.load_image_file('teste_satin.jpg')

face_locations = face_recognition.face_locations(test_image)
no = len(face_locations)
print("Number of faces detected: ", no)

print("Found:")
for i in range(no):
    test_image_enc = face_recognition.face_encodings(test_image)[i]
    name = clf.predict([test_image_enc])
    print(*name)