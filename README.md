# Mouse-Control-and-Virtual-Using-OpenCV
In this project i tried to control the mouse pointer and opening virtual keyboard using webcam with the help of OpenCV library in python.

import cv2, numpy, time, mediapipe, pyautogui

1. Read the stream from webcam
2. Flip the frame
3. Detect Hands in the frame
4. Get hand landmarks from the frame
5. Check if fore-finger is up then move pointer
6. To perform click we 'll check is middle finger is up or not then we 'll measure distance between fingers if it is below 40 than we ll perform click.
7. To display our virtual keyboard it checks if pinky finger is up or not. Then it repeats the click procedure for controlling it.
