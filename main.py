import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)
with mp_hands.Hands(static_image_mode=False, max_num_hands=1) as hands:
    while cap.isOpened():

        success, image = cap.read()

        if not success:
            break

        image = cv2.flip(image, 1)

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        isRight = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_handedness:
                isRight = hand_landmarks.classification[0].label == 'Right'
                isLeft = hand_landmarks.classification[0].label == 'Left'
            for hand_landmarks in results.multi_hand_landmarks:
                if isRight:
                    isThumbRightUp = hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y
                    if isThumbRightUp:
                        pyautogui.press('right')
                    mp_drawing.draw_landmarks(image,
                                              hand_landmarks,
                                              mp_hands.HAND_CONNECTIONS,
                                              mp_drawing_styles.get_default_hand_landmarks_style(),
                                              mp_drawing_styles.get_default_hand_connections_style())
                elif isLeft:
                    isThumbLeftUp = hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y
                    if isThumbLeftUp :
                        pyautogui.press('left')
                    mp_drawing.draw_landmarks(image,
                                              hand_landmarks,
                                              mp_hands.HAND_CONNECTIONS)
                else:
                    print("No hands")

        image = cv2.flip(image, 1)
        cv2.imshow("Handtracking PPT Slider",image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()