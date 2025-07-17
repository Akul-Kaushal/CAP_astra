import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands # type: ignore
mp_drawing = mp.solutions.drawing_utils # type: ignore

def detect_gesture(hand_landmarks) -> str:
    lm = hand_landmarks.landmark


    is_thumb_up = lm[4].y < lm[3].y < lm[2].y

    # All other fingers curled
    fingers_curled = all(lm[tip].y > lm[tip - 2].y for tip in [8, 12, 16, 20])

    if is_thumb_up and fingers_curled:
        return "THUMBS_UP"

    # Open palm
    if all(lm[tip].y < lm[tip - 2].y for tip in [8, 12, 16, 20]):
        return "OPEN_PALM"

    # Fist
    if all(lm[tip].y > lm[tip - 2].y for tip in [8, 12, 16, 20]):
        return "FIST"

    return "UNKNOWN"



def start_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot access webcam.")
        return

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    ) as hands:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    gesture = detect_gesture(hand_landmarks)
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )
                    cv2.putText(frame, f"Gesture: {gesture}", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print(f"Detected: {gesture}")

            cv2.imshow("ASTRA Vision", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera()
