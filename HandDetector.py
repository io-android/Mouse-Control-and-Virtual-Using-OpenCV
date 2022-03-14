import math

import cv2
import mediapipe as mp
import time

class DetectHands:

    def __init__(self, mode=False, mhands=2, complexity=1, dconf=0.5, tconf=0.5):

        # Self Object Initialization
        self.mode = mode
        self.mhands = mhands
        self.complexity = complexity
        self.dconf = dconf
        self.tconf = tconf

        # Media Pipe Landmark Drawing Utility
        self.mpDraw = mp.solutions.drawing_utils

        # Media Pipe Hand Detection Utility
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.mhands, self.complexity,
                                        self.dconf, self.tconf)

        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, frame, draw=True):

        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgbFrame)
        # print(results.multi_hand_landmarks)

        # Drawing LandMarks
        if self.results.multi_hand_landmarks:
            for landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, landmarks, self.mpHands.HAND_CONNECTIONS)

        return frame

    def getLandMarks(self, frame, handNum=0, draw=True):

        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            cHand = self.results.multi_hand_landmarks[handNum]

            # Highlighting Specific LandMark
            for idx, landmark in enumerate(cHand.landmark):

                rows, cols, axis = frame.shape
                cx = int(landmark.x * cols)
                cy = int(landmark.y * rows)

                xList.append(cx)
                yList.append(cy)

                self.lmList.append([idx, cx, cy])

                cv2.circle(frame, (cx, cy), 7, (0, 255, 255), cv2.FILLED)

            xMin, xMax = min(xList), max(xList)
            yMin, yMax = min(yList), max(yList)

            bbox = xMin,yMin, xMax, yMax

            if draw:
                cv2.rectangle(frame, (xMin - 20, yMin-20), (xMax + 20, yMax + 20), (240,0,0), 2)

        return self.lmList, bbox

    def findDistance(self, p1, p2, frame, draw=True, r=10, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (0,0,0), t)
            cv2.circle(frame, (x1, y1), r, (0, 0, 0), cv2.FILLED)
            cv2.circle(frame, (x2, y2), r, (0, 0, 0), cv2.FILLED)
            cv2.circle(frame, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)

        return length, frame, [x1, x2, y1, y2, cx, cy]

    def fingersUp(self):
        fingers = []

        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(0)
        else:
            fingers.append(1)

        for i in range(1,5):
            if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

def main():

    # Time Variables
    pTime = 0
    cTime = 0

    # Capture Stream
    stream = cv2.VideoCapture(0)

    while True:
        success, frame = stream.read()

        img = DetectHands.findHands(frame)
        landmarks = DetectHands.getLandMarks(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (20, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

        cv2.imshow("Frame", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()