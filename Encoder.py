import cv2 as cv
import os
import dlib
import face_recognition
import glob
import numpy as np
import pickle
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "",
    "storageBucket": ""
})



folderPath = 'images'
imgPathList = os.listdir(folderPath)
print(imgPathList)
imgList = []
IDs = []
for path in imgPathList:
    imgList.append(cv.imread(os.path.join(folderPath, path)))
    IDs.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
print(IDs)


def face_encodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Start Encoding ...")
encodeListKnown = face_encodings(imgList)
encodeListKnownWithIds = [encodeListKnown, IDs]
print("Encoding Complete")

file = open("Encodedfile.p", "wb")
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")