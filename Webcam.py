import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui

wcam, hcam = 640, 480
frameR = 100
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0
smoothening = 5
plocx, plocy = 0, 0
clocx, clocy = 0, 0
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # print(lmList)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
        cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 0, 255), 0)
        fingers = detector.fingersUp()
        print(fingers)
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wcam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hcam - frameR), (0, hScr))
            clocx = plocx + (x3 - plocx)/ smoothening
            clocy = plocy + (y3 - plocy)/ smoothening
            autopy.mouse.move(wScr - clocx, clocy)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocx, plocy = clocx, clocy
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineinfo = detector.findDistance(8, 12, img)
            # print(length)
            if length < 25:
                autopy.mouse.click()
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            pyautogui.scroll(30)

        if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            pyautogui.scroll(-30)
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1:
            pyautogui.rightClick()
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            pyautogui.press('left')
        if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            pyautogui.press('right')

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)
