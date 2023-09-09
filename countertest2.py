import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import time

cap = cv2.VideoCapture('Video.mp4')
detector = FaceMeshDetector(maxFaces=1)

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)

# Timer settings
timer_duration = 20  # in seconds
start_time = time.time()
reset_counter = False

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img = cv2.resize(img, (590, 350))
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5,color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)

        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0,200,0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255,0, 255)

        cv2.putText(img, f'Blink Count: {blinkCounter}', (8, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

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

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()