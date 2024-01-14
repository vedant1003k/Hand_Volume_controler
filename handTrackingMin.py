import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
# for Hands default parameter
#                static_image_mode=False,
#                max_num_hands=2,
#                model_complexity=1,
#                min_detection_confidence=0.5, 50%
#                min_tracking_confidence=0.5   50%
hands = mpHands.Hands()

# we have method provide by mediapipe to draw all the hand point 21 landmarks
mpDraw = mp.solutions.drawing_utils

# FPS
pTime = 0
Ctime = 0


while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)     # will process the frame for us
    # now how to extract and display
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # get information withing this hand , id number and landmark info  will give (x,y) coordiinate
            for id,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = img.shape # height width channel
                cx,cy = int(lm.x*w),int(lm.y*h) # center x and center y

                # print(lm,cx,cy) # id number and their respective center

                if id==0:
                    cv2.circle(img,(cx,cy),25,(255,255,0),cv2.FILLED) # circle at point 0

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)  # we can do the connection btween the point by adding on more parameter


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    # displaying fps
    cv2.putText(img,str(int(fps))+" fps",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)

    cv2.imshow("IMG", img)
    if cv2.waitKey(1) == ord('q'):
        break


# now we will creat a module of this so we can use it in any other project