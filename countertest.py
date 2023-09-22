import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np
import time

# Initialize the webcam
cap = cv2.VideoCapture(0)  # 0 represents the default camera
#cap = cv2.VideoCapture("EyeMoving.mp4")  # 0 represents the default camera

# Initialize the face mesh detector
detector = FaceMeshDetector(maxFaces=1)

idList = [23, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)

# Timer settings
timer_duration = 20  # in seconds
start_time = time.time()
reset_counter = False

while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    if not ret:
        break

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)

        ratio = int((lengthVer / lengthHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0, 200, 0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255, 0, 255)

        cv2.putText(img, f'Blink Count: {blinkCounter}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Display the timer value on the console
    elapsed_time = time.time() - start_time
    timer_remaining = max(0, timer_duration - elapsed_time)
    print(f"Timer Remaining: {timer_remaining:.2f} seconds", end='\r')

    # Display the timer value on the video stream
    timer_text = f"Timer: {timer_remaining:.2f} sec"
    cv2.putText(img, timer_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Check if the timer duration has passed
    if elapsed_time >= timer_duration:
        reset_counter = True
        start_time = time.time()

    # Reset the blink counter if necessary
    if reset_counter:
        print(f"Timer Started: Blink Counter = {blinkCounter}")
        blinkCounter = 0
        reset_counter = False
        print("Timer Finished")

    # Display the resulting frame
    cv2.imshow('Real-Time Video Stream', img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()