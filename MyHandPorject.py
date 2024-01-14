import cv2
import  time
import HandTrackingModule as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()   # changing detection condience we want to be very sure that it is hand

while True:
    success, img = cap.read()
    img = detector.findHands(img)  # to remove lm and connection draw=False
    PosList = detector.findPosition(img,draw=False)  # to remove custome drawing at landmarks add parameter

    if len(PosList) != 0:
        print(PosList[4])  # 4 is thumb tip position

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)) + "fps", (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 0), 3)

    cv2.imshow("IMG", img)
    if cv2.waitKey(1) == ord('q'):
        break