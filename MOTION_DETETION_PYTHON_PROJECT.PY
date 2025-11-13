# ...existing code...
import mediapipe as mp
import cv2
import time

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Failed to read frame")
            break

        # RECOLOR IMAGE TO RGB for Mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # MAKE DETECTIONS
        results = holistic.process(image)

        # CONVERT BACK TO BGR for OpenCV rendering
        annotated = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # DRAW LANDMARKS (only if present)
        if results.face_landmarks:
            mp_drawing.draw_landmarks(
                annotated, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)

        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(
                annotated, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(
                annotated, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                annotated, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

# FPS calculation (fpc)
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time) if prev_time else 0.0
        prev_time = curr_time
        cv2.putText(annotated, f'FPS: {int(fps)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Raw Webcam Feed', annotated)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# RELEASE THE WEBCAM AND DESTROY ALL OPENCV WINDOWS
cap.release()
cv2.destroyAllWindows()
# ...existing code...