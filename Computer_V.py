import cv2
import mediapipe as mp
import webbrowser
import time
import os
import urllib.request

model_path = 'hand_landmarker.task'
if not os.path.exists(model_path):
    print("Downloading hand tracking model (this only happens once)...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, model_path)
    print("Download complete!")

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.5
)
landmarker = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

tipIds = [4, 8, 12, 16, 20]

last_action_time = 0
cooldown_seconds = 3 

print("System Ready! Show your gestures to the camera.")

while True:
    success, img = cap.read()
    if not success:
        continue
        
    img = cv2.flip(img, 1)
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    
    detection_result = landmarker.detect(mp_image)

    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            lmList = []
            h, w, c = img.shape
            
            for id, lm in enumerate(hand_landmarks):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                cv2.circle(img, (cx, cy), 6, (0, 255, 0), cv2.FILLED)

            if len(lmList) != 0:
                fingers = []

                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = fingers.count(1)

                current_time = time.time()
                
                if current_time - last_action_time > cooldown_seconds:
                    if total_fingers == 1:
                        print("1 Finger: Opening Gemini")
                        webbrowser.open('https://gemini.google.com')
                        last_action_time = current_time
                        
                    elif total_fingers == 2:
                        print("2 Fingers: Opening ChatGPT")
                        webbrowser.open('https://chatgpt.com')
                        last_action_time = current_time
                        
                    elif total_fingers == 3:
                        print("3 Fingers: Opening Claude")
                        webbrowser.open('https://claude.ai')
                        last_action_time = current_time
                        
                    elif total_fingers == 5:
                        print("5 Fingers: Opening Codex")
                        webbrowser.open('https://platform.openai.com/codex')
                        last_action_time = current_time
                        
                    elif total_fingers == 0:
                        print("Fist: Closing Browser!")
                        os.system("taskkill /im chrome.exe /f") 
                        last_action_time = current_time

    cv2.imshow("AI Hand Controller", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()