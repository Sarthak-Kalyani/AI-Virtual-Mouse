import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# 🔊 volume control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

smoothening = 7
frameR = 100
prev_x, prev_y = 0, 0

click_delay = 0
click_cooldown = 0.4

# drag system
dragging = False

# scroll system
scroll_velocity = 0
scroll_decay = 0.92
scroll_speed = 8

# ==== MediaPipe ====
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

detector = HandLandmarker.create_from_options(options)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    cv2.rectangle(img, (frameR, frameR), (w - frameR, h - frameR), (255, 0, 255), 2)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

    results = detector.detect_for_video(mp_image, int(time.time() * 1000))

    if results.hand_landmarks:
        lm_list = []

        for hand_landmarks in results.hand_landmarks:
            for id, lm in enumerate(hand_landmarks):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))
                cv2.circle(img, (cx, cy), 4, (255, 0, 255), cv2.FILLED)

        if len(lm_list) >= 21:
            x1, y1 = lm_list[8][1:]
            x2, y2 = lm_list[4][1:]

            # finger states
            index_up = lm_list[8][2] < lm_list[6][2]
            middle_up = lm_list[12][2] < lm_list[10][2]
            ring_up = lm_list[16][2] < lm_list[14][2]
            pinky_up = lm_list[20][2] < lm_list[18][2]

            # 👍 FIST → STOP
            if not index_up and not middle_up and not ring_up and not pinky_up:
                scroll_velocity = 0
                cv2.putText(img, "PAUSED", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

            # ✌️ SCROLL UP
            elif index_up and middle_up and not ring_up:
                scroll_velocity = scroll_speed
                cv2.putText(img, "UP", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)

            # 🖖 SCROLL DOWN
            elif index_up and middle_up and ring_up:
                scroll_velocity = -scroll_speed
                cv2.putText(img, "DOWN", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)

            # 🎯 MOVE
            elif index_up and not middle_up:
                screen_x = np.interp(x1, (frameR, w - frameR), (0, screen_w))
                screen_y = np.interp(y1, (frameR, h - frameR), (0, screen_h))

                curr_x = prev_x + (screen_x - prev_x) / smoothening
                curr_y = prev_y + (screen_y - prev_y) / smoothening

                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

            # 🤏 CLICK + DRAG
            distance = np.hypot(x2 - x1, y2 - y1)

            # start drag
            if distance < 25 and not dragging:
                pyautogui.mouseDown()
                dragging = True

            # release drag
            elif distance > 40 and dragging:
                pyautogui.mouseUp()
                dragging = False

            # single click
            if distance < 30 and (time.time() - click_delay) > click_cooldown:
                pyautogui.click()
                click_delay = time.time()
                cv2.putText(img, "CLICK", (20, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

            # 🖱️ RIGHT CLICK (3 fingers + pinch)
            if index_up and middle_up and ring_up:
                if distance < 35:
                    pyautogui.rightClick()
                    cv2.putText(img, "RIGHT CLICK", (20, 160),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 3)

            # 🔊 VOLUME CONTROL (distance based)
            vol = np.interp(distance, [20, 200], [0.0, 1.0])
            volume.SetMasterVolumeLevelScalar(vol, None)

            cv2.putText(img, f"VOL {int(vol*100)}%", (20, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)

    # smooth scroll
    if abs(scroll_velocity) > 0.5:
        pyautogui.scroll(int(scroll_velocity))
        scroll_velocity *= scroll_decay

    cv2.imshow("AI Virtual Mouse PRO", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()