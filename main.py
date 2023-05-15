import os
import pickle
import face_recognition
import cv2 as cv
import numpy as np
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "",
    "storageBucket": ""
})

bucket = storage.bucket()

cap = cv.VideoCapture(0)
adress = "http://192.168.1.2:8080/video"
cap.open(adress)
background = cv.imread("Resources/background.png")
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv.imread(os.path.join(folderModePath, path)))

file = open("Encodedfile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, IDs = encodeListKnownWithIds
print(IDs)
modeType = 0
counter = 0
id = -1
imgData = []

while True:
    success, img = cap.read()
    imgS = cv.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)
    faceCurentFrame = face_recognition.face_locations(imgS)
    encodeCurentFrame = face_recognition.face_encodings(imgS, faceCurentFrame)
    resized_img = cv.resize(img, (640, 480))  # resize the img to match the dimensions of the background
    background[162:162+480,55:55+640] = resized_img
    background[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    #cv.imshow("Camera", img)

    if faceCurentFrame:
        for encodeface, faceLoc in zip(encodeCurentFrame, faceCurentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeface)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeface)
            # print("matches", matches)
            # print("faceDis", faceDis)
            matchIndex = np.argmin(faceDis)
            #print("matchindex", matchIndex)
            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                id = IDs[matchIndex]
                if counter == 0:
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                info = db.reference(f'Data/{id}').get()
                blob = bucket.get_blob(f'images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgData = cv.imdecode(array, cv.COLOR_BGRA2BGR)
                imgData = cv.resize(imgData, (216, 216))
                # Update data of attendance
                datetimeObject = datetime.strptime(info['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Data/{id}')
                    info['total_days_attendance'] += 1
                    ref.child('total_days_attendance').set(info['total_days_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    background[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                background[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv.putText(background, str(info['total_days_attendance']), (861, 125),
                                cv.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
                    cv.putText(background, str(info['Department']), (1006, 550),
                                cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    cv.putText(background, str(id), (1006, 493),
                                cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                    cv.putText(background, str(info['standing']), (910, 625),
                                cv.FONT_HERSHEY_DUPLEX, 0.6, (100, 100, 100), 1)
                    cv.putText(background, str(info['year']), (1025, 625),
                                cv.FONT_HERSHEY_DUPLEX, 0.6, (100, 100, 100), 1)
                    cv.putText(background, str(info['starting_year']), (1125, 625),
                                cv.FONT_HERSHEY_DUPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv.getTextSize(info['name'], cv.FONT_HERSHEY_DUPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv.putText(background, str(info['name']), (808 + offset, 445),
                                cv.FONT_HERSHEY_DUPLEX, 1, (50, 50, 50), 1)

                    background[175:175 + 216, 909:909 + 216] = imgData

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    info = []
                    imgData = []
                    background[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    else:
        modeType = 0
        counter = 0
    cv.imshow("Face Attendance", background)
    cv.waitKey(1)
