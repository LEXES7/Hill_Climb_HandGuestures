import cv2
import mediapipe as mp
import time
from pynput.keyboard import Key, Controller

print("Starting Dual-Hand Gesture Detection for Subway Surfers...")
print("OpenCV version:", cv2.__version__)
print("Press 'q' to quit")

# Initialize keyboard controller
keyboard = Controller()

def initialize_camera():
    """Try to initialize camera with multiple attempts"""
    for attempt in range(3):
        print(f"Camera initialization attempt {attempt + 1}...")
        
        for camera_id in [0, 1, 2]:
            video = cv2.VideoCapture(camera_id)
            if video.isOpened():
                # Test if we can actually read a frame
                ret, test_frame = video.read()
                if ret and test_frame is not None:
                    print(f"Camera {camera_id} working! Frame shape: {test_frame.shape}")
                    return video, camera_id
                video.release()
        
        print(f"Attempt {attempt + 1} failed, waiting 2 seconds...")
        time.sleep(2)
    
    return None, None

def count_fingers(landmarks):
    """Count extended fingers for a hand"""
    tipIds = [4, 8, 12, 16, 20]
    fingers = []
    
    # Convert landmarks to list format
    lmList = []
    for id, lm in enumerate(landmarks):
        lmList.append([id, lm.x, lm.y])
    
    if len(lmList) < 21:
        return 0
    
    # Thumb (different logic for left/right hand)
    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # Right hand
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Other fingers
    for id in range(1, 5):
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers.count(1)

def get_hand_state(finger_count):
    """Determine if hand is open or closed"""
    if finger_count >= 4:  # 4 or 5 fingers = open palm
        return "OPEN"
    elif finger_count <= 1:  # 0 or 1 finger = closed fist
        return "CLOSED"
    else:
        return "PARTIAL"  # Some fingers extended

def classify_hands(results):
    """Classify left and right hands"""
    if not results.multi_hand_landmarks:
        return "NONE", "NONE"
    
    left_state = "NONE"
    right_state = "NONE"
    
    for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
        # Get hand classification (Left or Right)
        hand_label = results.multi_handedness[idx].classification[0].label
        
        # Count fingers for this hand
        finger_count = count_fingers(hand_landmarks.landmark)
        hand_state = get_hand_state(finger_count)
        
        if hand_label == "Left":  # MediaPipe's "Left" is actually right hand in flipped image
            right_state = hand_state
        else:  # MediaPipe's "Right" is actually left hand in flipped image
            left_state = hand_state
    
    return left_state, right_state

# Initialize camera
video, camera_id = initialize_camera()
if video is None:
    print("❌ Could not initialize camera!")
    exit()

print(f"✅ Using camera {camera_id}")

# Initialize MediaPipe
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

frame_count = 0
failed_reads = 0
last_action_time = 0

print("\n=== SUBWAY SURFERS DUAL-HAND CONTROLS ===")
print("🙌 Both palms OPEN = JUMP")
print("✊✊ Both hands CLOSED = SLIDE")
print("🤚✊ Left OPEN + Right CLOSED = MOVE LEFT")
print("✊🤚 Left CLOSED + Right OPEN = MOVE RIGHT")
print("===========================================\n")

print("Position both hands in front of camera!")
print("Starting in 5 seconds...")
time.sleep(5)

def send_key_tap(key):
    """Send a quick key tap"""
    global last_action_time
    current_time = time.time()
    
    if current_time - last_action_time > 0.2:
        keyboard.press(key)
        time.sleep(0.05)
        keyboard.release(key)
        last_action_time = current_time
        return True
    return False

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2) as hands:  # Detect up to 2 hands
    
    while True:
        ret, image = video.read()
        if not ret or image is None:
            failed_reads += 1
            if failed_reads > 5:
                print("❌ Camera connection lost")
                break
            continue
        
        failed_reads = 0
        frame_count += 1
        
        if frame_count % 60 == 0:
            print(f"✅ Frame {frame_count} - Dual-hand tracking active")
        
        # Flip image horizontally for mirror effect
        image = cv2.flip(image, 1)
        
        # Convert to RGB for MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = hands.process(image_rgb)
        image_rgb.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Get hand states
        left_state, right_state = classify_hands(results)
        
        # Determine action based on both hands
        action = "IDLE"
        
        if left_state == "OPEN" and right_state == "OPEN":
            action = "JUMP"
            cv2.rectangle(image, (200, 50), (450, 150), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "JUMP", (250, 110), cv2.FONT_HERSHEY_SIMPLEX,
                       2, (255, 255, 255), 3)
            if send_key_tap(Key.up):
                print("⬆️ JUMPING!")
        
        elif left_state == "CLOSED" and right_state == "CLOSED":
            action = "SLIDE"
            cv2.rectangle(image, (200, 400), (450, 500), (255, 0, 255), cv2.FILLED)
            cv2.putText(image, "SLIDE", (220, 460), cv2.FONT_HERSHEY_SIMPLEX,
                       2, (255, 255, 255), 3)
            if send_key_tap(Key.down):
                print("⬇️ SLIDING!")
        
        elif left_state == "OPEN" and right_state == "CLOSED":
            action = "MOVE_LEFT"
            cv2.rectangle(image, (20, 200), (250, 300), (255, 255, 0), cv2.FILLED)
            cv2.putText(image, "LEFT", (80, 260), cv2.FONT_HERSHEY_SIMPLEX,
                       2, (0, 0, 0), 3)
            if send_key_tap(Key.left):
                print("⬅️ MOVING LEFT!")
        
        elif left_state == "CLOSED" and right_state == "OPEN":
            action = "MOVE_RIGHT"
            cv2.rectangle(image, (400, 200), (630, 300), (0, 0, 255), cv2.FILLED)
            cv2.putText(image, "RIGHT", (440, 260), cv2.FONT_HERSHEY_SIMPLEX,
                       2, (255, 255, 255), 3)
            if send_key_tap(Key.right):
                print("➡️ MOVING RIGHT!")
        
        else:
            action = "IDLE"
            cv2.rectangle(image, (250, 250), (400, 350), (128, 128, 128), cv2.FILLED)
            cv2.putText(image, "READY", (270, 310), cv2.FONT_HERSHEY_SIMPLEX,
                       1.5, (255, 255, 255), 3)
        
        # Display hand states
        cv2.putText(image, f"Left: {left_state}", (10, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(image, f"Right: {right_state}", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(image, f"Action: {action}", (10, 130), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Instructions
        cv2.putText(image, "Show both hands to camera", (10, 550), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw hand position guides
        cv2.rectangle(image, (50, 150), (300, 450), (100, 100, 100), 2)  # Left hand area
        cv2.rectangle(image, (350, 150), (600, 450), (100, 100, 100), 2)  # Right hand area
        cv2.putText(image, "LEFT HAND", (60, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(image, "RIGHT HAND", (360, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Subway Surfers Dual-Hand Control - Press Q to quit', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

print("Closing camera...")
video.release()
cv2.destroyAllWindows()
print("Program ended successfully!")