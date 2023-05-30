import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
from sms import send_sms

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://your-project-id.firebaseio.com/",
        "storageBucket": "your-storage-bucket.appspot.com",
    },
)

bucket = storage.bucket()

# Your Twilio account SID, auth token and phone number
account_sid = 'YOUR_ACCOUNT_SID' 
auth_token = 'YOUR_AUTH_TOCKEN'
from_number = 'YOUR_TWILIO_PHONE_NUMBER'  


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/background.png")

# Importing the mode images into a list
folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, victimIds = encodeListKnownWithIds
# print(victimIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgVictim = []
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162 : 162 + 480, 55 : 55 + 640] = img
    imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(victimIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = victimIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Missing Person", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Get the Data
                victimInfo = db.reference(f"Victims/{id}").get()
                print(victimInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f"Images/{id}.png")
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgVictim = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # Update last seen of victim
                ref = db.reference(f"Victims/{id}")
                ref.child("last_seen_time").set(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(
                        imgBackground,
                        str(victimInfo["father_name"]),
                        (1006, 550),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                    )
                    cv2.putText(
                        imgBackground,
                        #str(id),
                        str(victimInfo["age"]),
                        (1006, 493),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                    )
                    cv2.putText(
                        imgBackground,
                        str(victimInfo["last_seen_time"]),
                        (910, 650),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.6,
                        (255, 255, 255),
                        1,
                    )
                    cv2.putText(
                        imgBackground,
                        str(victimInfo["contact_no"]),
                        (1000, 610),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                    )
                    cv2.putText(
                        imgBackground,
                        str(victimInfo["location"]),
                        (913, 146),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.5,
                        (0, 174, 239),
                        1,
                    )

                    (w, h), _ = cv2.getTextSize(
                        victimInfo["name"], cv2.FONT_HERSHEY_DUPLEX, 1, 1
                    )
                    offset = (414 - w) // 2
                    cv2.putText(
                        imgBackground,
                        str(victimInfo["name"]),
                        (808 + offset, 445),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1,
                        (225, 225, 225),
                        1,
                    )

                    imgBackground[175 : 175 + 216, 909 : 909 + 216] = imgVictim
                    
                    
                    to_number = '+91' + str(victimInfo["contact_no"])
                    victimName= str(victimInfo["name"])
                    victimLoc = str(victimInfo["location"])
                    message = f'Your {victimName} is currently located at {victimLoc}'
                    send_sms(account_sid, auth_token, from_number, to_number, message)

                
                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    victimInfo = []
                    imgVictim = []
                    imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[
                        modeType
                    ]
    else:
        modeType = 0
        counter = 0
    cv2.imshow("Missing Person", imgBackground)
    cv2.waitKey(1)
    c = 0