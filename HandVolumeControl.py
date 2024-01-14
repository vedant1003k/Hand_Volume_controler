import cv2
import time
import numpy as np
import mediapipe
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

########### Basic Initialization
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# volume.GetMute()
# volume.GetMasterVolumeLevel()

volRange = volume.GetVolumeRange()    # is (-96.0 , 0.0 , 0.125)  (min,max,ignore)


minVol = volRange[0]
maxVol = volRange[1]
volBAR = 400
vol = 0
volPer=0

############# PARAMETER ################
wCam , hCam = 640, 480  #640,480


cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime=0
cTime=0

detector = htm.handDetector(detectionCon=0.7)

while True:
    success , img = cap.read()
    img = detector.findHands(img)  # to remove lm and connection draw=False
    PosList = detector.findPosition(img, draw=False)  # to remove custome drawing at landmarks add parameter

    if len(PosList) != 0:
        # print(PosList[4],PosList[8])  # 4 is thumb tip position and 8 index tip position

        x1,y1 = PosList[4][1],PosList[4][2]
        x2,y2 = PosList[8][1],PosList[8][2]

        # center of this two points
        cx,cy =(x1+x2)//2 , (y1+y2)//2

        cv2.circle(img,(x1,y1),14,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 14, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 14, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1) # getting length so that we can change volume according to it
        # print(length)

        # to change volume based on lenght we can do this using couple of libaraies like pycaw
        # Developed by Andre Miras
        # Hand Range 50-300
        # volum Range -96-0

        #converting the range
        vol = np.interp(length,[50,296],[minVol,maxVol])
        volBAR = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length),vol)

        #setting the value
        volume.SetMasterVolumeLevel(vol, None)


        if length < 50:
            cv2.circle(img, (cx, cy), 14, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(255, 0, 0),3)
    cv2.rectangle(img, (50, int(volBAR)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)

    cv2.imshow("WEB",img)
    if cv2.waitKey(1) == ord('q'):
        break