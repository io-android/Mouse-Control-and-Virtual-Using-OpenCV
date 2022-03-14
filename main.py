import cv2
import mediapipe as mp
import time
import HandDetector as hd
import pyautogui as pag
import numpy as np

# Variables

frameWidth, frameHeight = 1280, 720
screenWidth, screenHeight = pag.size()
frameR = 0
smoothening = 10
pag.PAUSE = 0

pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0

showKeyBoard = False

# pag.FAILSAFE = False

# Capture Stream
stream = cv2.VideoCapture(0)
stream.set(3, frameWidth)
stream.set(4, frameHeight)

# Time Variables
pTime = 0
cTime = 0

# HandDetector Class Object Instance
detector = hd.DetectHands(mhands=1, dconf=0.8)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "/"]]

buttonList = []

def drawAll(rframe, btnList):
    for btn in btnList:
        x, y = btn.pos
        w, h = btn.size
        cv2.rectangle(rframe, btn.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        cv2.putText(rframe, btn.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    return rframe


class Button:
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos
        self.text = text
        self.size = size



for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
while True:
    success, frame = stream.read()

    # Flipping Stream
    rframe = cv2.flip(frame, 1)

    # Find Hands
    rframe = detector.findHands(rframe)

    # Get Hand Landmarks List i.e 21
    landmarks, bbox = detector.getLandMarks(rframe)


    if showKeyBoard:
        rframe = drawAll(rframe, buttonList)
        if landmarks:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                print(landmarks[8], button.pos, button.size)

                if x < landmarks[8][0] < x + w and y < landmarks[8][1] < y + h:
                    cv2.rectangle(rframe, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(rframe, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),
                                3)

    if len(landmarks) != 0:
        x1, y1 = landmarks[8][1:]
        x2, y2 = landmarks[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(rframe, (frameR, frameR), (frameWidth - frameR, frameHeight - frameR), (0, 255, 0), 2)

        if fingers[1] == 1 and fingers[2] == 0:

            x3 = np.interp(x1, (frameR, frameWidth - frameR), (0, screenWidth))
            y3 = np.interp(y1, (frameR, frameHeight - frameR), (0, screenHeight))

            cLocX = pLocX + (x3 - pLocX) / smoothening
            cLocY = pLocY + (y3 - pLocY) / smoothening

            pag.moveTo(cLocX, cLocY)
            cv2.circle(rframe, (x1,y1), 10, (0,0,0), cv2.FILLED)
            pLocX, pLocY = cLocX, cLocY

        if fingers[1] == 1 and fingers[2] == 1:

            # x3 = np.interp(x1, (frameR, frameWidth - frameR), (0, screenWidth))
            # y3 = np.interp(y1, (frameR, frameHeight - frameR), (0, screenHeight))
            #
            # cLocX = pLocX + (x3 - pLocX) / smoothening
            # cLocY = pLocY + (y3 - pLocY) / smoothening
            #
            # pag.moveTo(cLocX, cLocY)
            # cv2.circle(rframe, (x1, y1), 10, (0, 0, 0), cv2.FILLED)
            # pLocX, pLocY = cLocX, cLocY

            distance, img, line = detector.findDistance(8, 12, rframe)

            if distance < 40:
                cv2.circle(rframe, (line[4], line[5]), 10, (0, 255, 0), cv2.FILLED)
                pag.click(clicks=1, interval=1 )

        if fingers[4] == 1 and fingers[1] == 0 and fingers[2] == 0:
            if not showKeyBoard:
                showKeyBoard = True
            else:
                showKeyBoard = False



    # Calculate FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # Write FPS Text onto Frame
    cv2.putText(rframe, "{}{}".format("FPS : ", int(fps)), (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (70,230,170), 2)

    # Show Frame
    cv2.imshow("Cam Stream", rframe)
    cv2.waitKey(1)
