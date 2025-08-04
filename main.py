import cv2
import mediapipe as mp
import time
from pynput.keyboard import Key, Controller

def initialize_camera(attempts=3, camera_ids=[0, 1, 2]):
    for attempt in range(attempts):
        print(f"Camera initialization attempt {attempt + 1}...")
        for camera_id in camera_ids:
            video = cv2.VideoCapture(camera_id)
            if video.isOpened():
                ret, test_frame = video.read()
                if ret and test_frame is not None:
                    print(f"Camera {camera_id} working! Frame shape: {test_frame.shape}")
                    return video, camera_id
                video.release()
        print(f"Attempt {attempt + 1} failed, waiting 2 seconds...")
        time.sleep(2)
    return None, None

def get_landmarks(image, hands):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False
    results = hands.process(image_rgb)
    image_rgb.flags.writeable = True
    image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    lmList = []
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmark, mp.solutions.hands.HAND_CONNECTIONS)
    return lmList, image

def count_fingers(lmList, tipIds):
    fingers = []
    if len(lmList) == 0:
        return -1, fingers
    if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    for id in range(1, 5):
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers.count(1), fingers

def perform_action(total, current_action, keyboard):
    if total == 0:
        if current_action != "BRAKE":
            keyboard.press(Key.left)
            print("BRAKE activated!")
        return "BRAKE"
    elif total == 5:
        if current_action != "GAS":
            keyboard.press(Key.right)
            print("GAS activated!")
        return "GAS"
    elif total == 1:
        if current_action != "LEAN_FORWARD":
            keyboard.press(Key.up)
            print("LEAN FORWARD activated!")
        return "LEAN_FORWARD"
    elif total == -1:
        if current_action is not None:
            release_all_keys(keyboard)
            print("Idle (no hand detected)")
        return "IDLE"
    else:
        return "NONE"

def release_all_keys(keyboard):
    keyboard.release(Key.left)
    keyboard.release(Key.right)
    keyboard.release(Key.up)
    keyboard.release(Key.down)

def main():
    print("Starting Hand Gesture Detection...")
    print("OpenCV version:", cv2.__version__)
    print("Press 'q' to quit")
    keyboard = Controller()
    video, camera_id = initialize_camera()
    if video is None:
        print("❌ Could not initialize any camera after 3 attempts!")
        print("🔧 Try:")
        print("1. Reconnect your iPhone camera")
        print("2. Check camera permissions in System Preferences")
        print("3. Restart your Mac")
        return
    print(f"✅ Using camera {camera_id}")
    tipIds = [4, 8, 12, 16, 20]
    frame_count = 0
    current_action = None
    failed_reads = 0
    print("\n=== HILL CLIMB RACING CONTROLS ===")
    print("✊ Fist (0 fingers) = BRAKE")
    print("✋ Open hand (5 fingers) = GAS")
    print("☝️ Point up (1 finger) = LEAN FORWARD")
    print("=====================================\n")
    print("Switch to Hill Climb Racing now! You have 5 seconds...")
    time.sleep(5)
    with mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while True:
            ret, image = video.read()
            if not ret or image is None:
                failed_reads += 1
                print(f"❌ Failed to read from camera (attempt {failed_reads})")
                if failed_reads > 5:
                    print("🔄 Too many failed reads, trying to reinitialize camera...")
                    video.release()
                    video, camera_id = initialize_camera()
                    if video is None:
                        print("❌ Could not reinitialize camera, exiting...")
                        break
                    failed_reads = 0
                    continue
                else:
                    time.sleep(0.1)
                    continue
            failed_reads = 0
            frame_count += 1
            if frame_count % 60 == 0:
                print(f"✅ Frame {frame_count} - System running smoothly")
            image = cv2.flip(image, 1)
            lmList, image = get_landmarks(image, hands)
            total, fingers = count_fingers(lmList, tipIds)
            cv2.putText(image, f"Fingers: {total if total != -1 else 'No hand'}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
            action = perform_action(total, current_action, keyboard)
            if action == "BRAKE":
                cv2.rectangle(image, (20, 300), (270, 425), (0, 0, 255), cv2.FILLED)
                cv2.putText(image, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
            elif action == "GAS":
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "GAS", (60, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
            elif action == "LEAN_FORWARD":
                cv2.rectangle(image, (300, 300), (550, 425), (255, 0, 0), cv2.FILLED)
                cv2.putText(image, "LEAN FWD", (310, 375), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            elif action == "IDLE":
                cv2.putText(image, "IDLE", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (200, 200, 200), 4)
            if action != current_action:
                if current_action is not None:
                    release_all_keys(keyboard)
                current_action = action if action not in ["NONE", "IDLE"] else None
            if action in ["NONE", "IDLE"] and current_action is not None:
                release_all_keys(keyboard)
                current_action = None
                print("🔄 All controls released")
            cv2.putText(image, f"Action: {action}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.imshow('Hand Tracking - Press Q to quit', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                release_all_keys(keyboard)
                break
    print("Closing camera...")
    video.release()
    cv2.destroyAllWindows()
    print("Program ended successfully!")

if __name__ == "__main__":
    main()