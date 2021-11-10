import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math

# volume's imports
import osascript

##################################
wCam, hCam = 640, 480
##################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

vol = 0
volBar = 400
volPerc = 0

detector = htm.HandDetector()

while True:
    success, img = cap.read()
    # Find hand
    img = detector.find_hands(img)
    lmList, bbox = detector.find_positions(img)

    if lmList:
        # Filter based on size
        area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1]) // 1000
        print(area)
        if 10 <= area <= 250:

            # Find distance between index and Thumb
            length, img, info = detector.find_distance(4, 8, img)

            # Convert volume
            vol = np.interp(length, [10, 150], [0, 100])
            volBar = np.interp(length, [10, 150], [400, 150])
            osascript.osascript("set volume output volume {}".format(vol))

            # Reduce revolution to make it smoother



            # set new volume level

    cv2.rectangle(img, (50,150), (85,400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(vol)} %', (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)
