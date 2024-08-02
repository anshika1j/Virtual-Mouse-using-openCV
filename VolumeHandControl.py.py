import mediapipe as mp
import cv2
import numpy as np
from math import sqrt
import win32api
import pyautogui

# Initialize Mediapipe hands module
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize click counter
click = 0

# Initialize video capture
video = cv2.VideoCapture(0)

# Initialize hands module with confidence thresholds
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        # Get image dimensions
        imageHeight, imageWidth, _ = image.shape

        # Process hand landmarks
        results = hands.process(image)

        # Convert image back to BGR for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw hand landmarks and connections
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                           mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
                                                                  circle_radius=2))

        # Check if hand landmarks are detected
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:
                    # Get pixel coordinates of hand landmarks
                    normalized_landmark = hand_landmarks.landmark[point]
                    pixel_coordinates_landmark = mp_drawing._normalized_to_pixel_coordinates(
                        normalized_landmark.x, normalized_landmark.y, imageWidth, imageHeight)

                    # Convert point to string
                    point = str(point)

                    # Check if the finger tip is detected
                    if point == 'HandLandmark.INDEX_FINGER_TIP':
                        try:
                            index_finger_tip_x = pixel_coordinates_landmark[0]
                            index_finger_tip_y = pixel_coordinates_landmark[1]
                        except:
                            pass

                    # Check if the thumb tip is detected
                    elif point == 'HandLandmark.THUMB_TIP':
                        try:
                            thumb_tip_x = pixel_coordinates_landmark[0]
                            thumb_tip_y = pixel_coordinates_landmark[1]
                        except:
                            pass

            try:
                # Calculate distance between thumb and index finger tips
                distance_x = abs(index_finger_tip_x - thumb_tip_x)
                distance_y = abs(index_finger_tip_y - thumb_tip_y)

                # Adjust the clicking threshold as needed
                if distance_x < 30 and distance_y < 30:
                    click += 1
                    if click % 5 == 0:
                        print("Single click")
                        pyautogui.click()

                # Move the cursor
                win32api.SetCursorPos((int(index_finger_tip_x * 4), int(index_finger_tip_y * 5)))

            except Exception as e:
                print("Error:", e)

        # Display the processed frame
        cv2.imshow('Hand Tracking', image)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
           break

# Release video capture
video.release()
