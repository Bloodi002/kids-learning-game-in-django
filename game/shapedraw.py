import cv2 as cv
import time as t
import os
import random
import numpy as np  # Added for using np.zeros for a solid background
import mediapipe as mp

# Set camera dimensions
wCam, hCam = 1680, 900

# Initialize the webcam
cap = cv.VideoCapture(0)
cap.set(3, wCam)  # Set width
cap.set(4, hCam)  # Set height

# Load finger images for overlay
folderpath = "G:/SHLOK/Swinburne University of Tech/Sem 1/Technology Inquiry Project/kids-learning-game-in-django/game/Fingerimages"
myList = os.listdir(folderpath)
print(myList)
overlayList = []
for imp in myList:
    image = cv.imread(f'{folderpath}/{imp}')  # Importing the images
    overlayList.append(image)
print(len(overlayList))

# Initialize MediaPipe hands model
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mpDraw = mp.solutions.drawing_utils

# Tip landmarks for the fingers
tipIds = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

pt = 0  # Previous time for FPS calculation

# Math problems
math_problems = [
    ("I am a two-digit number. My tens digit is three times my ones digit. The sum of my digits is 12. What number am I?", "93"),
    ("You have a chocolate bar that is divided into 12 squares. What is the fewest number of breaks needed to separate all the squares?", "11"),
    ("Fill the triangle with numbers 1 to 6 so that the sum on each side is the same.", "Solve on paper!"),
    ("There are 20 people in a room. Each person shakes hands with every other person exactly once. How many handshakes are there?", "190"),
    ("How can you make the number 100 using only the buttons 1, 2, 3, +, and = on a calculator?", "Try: 33 + 33 + 34"),
    ("A frog jumps 3 meters up but slips 2 meters down. How many days to climb a 10-meter well?", "8"),
    ("There are chickens and cows on a farm. In total, there are 30 heads and 100 legs. How many chickens and cows?", "20 chickens, 10 cows"),
    ("If you are given a penny today, two pennies tomorrow, four pennies the next day, and so on, how much after 30 days?", "$10,737,418.23"),
    ("Two trains are 200 kilometers apart, one traveling 80 km/h, the other 120 km/h. How long until they meet?", "1 hour")
]

# Mode: 0 = Finger Counting, 1 = Math Challenge
mode = 0
current_problem = None
user_answer = ""

def get_new_problem():
    return random.choice(math_problems)

while True:
    # Capture frame-by-frame
    success, img = cap.read()
    if not success:
        break  # In case the frame is not captured, break the loop

    # Display the menu for switching modes
    cv.putText(img, 'Press F for Finger Counting, M for Math Challenge', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    if mode == 0:  # Finger Counting Mode
        # Convert image to RGB (required by MediaPipe)
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        # If hand landmarks are detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # Draw hand landmarks on the image
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                # List to store landmarks
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    # Get height, width of the image and calculate pixel values
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

                # Finger Counting
                if len(lmList) != 0:
                    fingers = []

                    # Thumb
                    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # Right hand
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    # Other 4 Fingers (Index, Middle, Ring, Pinky)
                    for id in range(1, 5):
                        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                            fingers.append(1)  # Finger is open
                        else:
                            fingers.append(0)  # Finger is closed

                    # Count fingers
                    totalFingers = fingers.count(1)

                    # Display corresponding overlay image
                    h, w, c = overlayList[totalFingers].shape  # Get the shape of the overlay image
                    img[0:h, 0:w] = overlayList[totalFingers]  # Display corresponding finger count image

                    # Display the total finger count on the screen
                    cv.putText(img, f'Fingers: {totalFingers}', (50, 400), cv.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)

    elif mode == 1:  # Math Challenge Mode
        # Replace camera feed with a solid background (light gray)
        img = np.zeros((hCam, wCam, 3), dtype=np.uint8)
        img[:] = (200, 200, 200)  # Light gray background

        if current_problem is None:
            current_problem = get_new_problem()

        # Display the current math problem
        cv.putText(img, 'Math Problem:', (10, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv.putText(img, current_problem[0], (10, 150), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  # Yellow color

        # Show the user's input answer
        cv.putText(img, f'Your answer: {user_answer}', (10, 400), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Move FPS counter to bottom-right corner to avoid overlap
    ct = t.time()
    fps = 1 / (ct - pt)
    pt = ct
    cv.putText(img, f'FPS: {int(fps)}', (wCam - 150, hCam - 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display the resulting frame
    cv.imshow("Image", img)

    # Wait for 1 ms and check for key presses
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('v') or key == ord('V'):
        mode = 0  # Switch to Finger Counting
        current_problem = None
        user_answer = ""
    elif key == ord('m') or key == ord('M'):
        mode = 1  # Switch to Math Challenge
        current_problem = None
        user_answer = ""
    elif key >= ord('0') and key <= ord('9'):
        user_answer += chr(key)  # Add digit to the answer
    elif key == ord('\r'):  # Enter key
        if user_answer == current_problem[1]:
            print("Correct!")
        else:
            print("Incorrect.")
        current_problem = None  # Load a new problem
        user_answer = ""

# Release the webcam and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
