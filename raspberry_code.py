import cv2
import numpy as np
import time
import smbus
from picamera2 import Picamera2

# -----------------------------
# I2C setup
# -----------------------------
bus = smbus.SMBus(1)
arduino_address = 0x08

def send_command(command):
    try:
        bus.write_byte(arduino_address, command)
        print(f"Sent command: {command}")
        return True
    except Exception as e:
        print(f"I2C Error: {e}")
        return False

# -----------------------------
# Command determination
# -----------------------------
def determine_command(result, horizontal_line_detected):
    if horizontal_line_detected:
        return 7  # UTurn
    elif abs(result) < 15:
        return 0  # Forward
    elif result > 50:
        return 6  # Left3
    elif result > 25:
        return 5  # Left2
    elif result > 0:
        return 4  # Left1
    elif result < -50:
        return 3  # Right3
    elif result < -25:
        return 2  # Right2
    else:
        return 1  # Right1

# -----------------------------
# Camera setup
# -----------------------------
picam2 = Picamera2()
picam2.preview_configuration.main.size = (400, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
print("Connected to camera")

# -----------------------------
# Perspective points
# -----------------------------
source = np.float32([[40,135], [360,135], [0,185], [400,185]])
destination = np.float32([[100,0], [280,0], [100,240], [280,240]])

# -----------------------------
# STOP & OBSTACLE detectors
# -----------------------------
stop_cascade = cv2.CascadeClassifier("/home/robot/Desktop/Stop_cascade.xml")
if stop_cascade.empty():
    print("Error: STOP cascade not loaded!")

obstacle_cascade = cv2.CascadeClassifier("/home/robot/Desktop/Object_cascade.xml")
if obstacle_cascade.empty():
    print("Error: OBSTACLE cascade not loaded!")

# -----------------------------
# Helper functions
# -----------------------------
def capture():
    return picam2.capture_array()

def perspective(frame):
    matrix = cv2.getPerspectiveTransform(source, destination)
    return cv2.warpPerspective(frame, matrix, (400,240))

def threshold(frame_pers):
    frame_gray = cv2.cvtColor(frame_pers, cv2.COLOR_RGB2GRAY)
    frame_thresh = cv2.inRange(frame_gray, 230, 255)
    frame_edge = cv2.Canny(frame_gray, 100, 200)
    frame_final = cv2.add(frame_thresh, frame_edge)
    frame_final_rgb = cv2.cvtColor(frame_final, cv2.COLOR_GRAY2RGB)
    frame_final_bgr = cv2.cvtColor(frame_final_rgb, cv2.COLOR_RGB2BGR)
    frame_final_bgr1 = frame_final_bgr.copy()
    return frame_final_rgb, frame_final_bgr, frame_final_bgr1

def histogram(frame_final_bgr):
    hist_lane = []
    for i in range(400):
        roi = frame_final_bgr[140:240, i:i+1]
        roi_sum = np.sum(roi)
        hist_lane.append(int(255 * np.count_nonzero(roi) / roi.size) if roi_sum > 0 else 0)
    return hist_lane

def lane_finder(hist_lane):
    left_half = hist_lane[:150]
    left_pos = np.argmax(left_half) if max(left_half) > 10 else 75
    right_half = hist_lane[250:]
    right_pos = np.argmax(right_half) + 250 if max(right_half) > 10 else 325
    return left_pos, right_pos

def lane_center(frame_final, left_pos, right_pos):
    lane_center_pos = (right_pos + left_pos) // 2
    frame_center = 188
    cv2.line(frame_final, (left_pos, 0), (left_pos, 240), (255, 0, 0), 2)
    cv2.line(frame_final, (right_pos, 0), (right_pos, 240), (255, 0, 0), 2)
    cv2.line(frame_final, (lane_center_pos, 0), (lane_center_pos, 240), (0, 255, 0), 3)
    cv2.line(frame_final, (frame_center, 0), (frame_center, 240), (255, 0, 0), 3)
    result = lane_center_pos - frame_center
    return result

def detect_horizontal_line(frame_final_gray, min_line_length=50):
    lines = cv2.HoughLinesP(frame_final_gray, 1, np.pi/180, threshold=80, minLineLength=min_line_length, maxLineGap=10)
    if lines is not None:
        for x1, y1, x2, y2 in lines[:,0]:
            angle = np.abs(np.arctan2(y2-y1, x2-x1) * 180 / np.pi)
            if angle < 10:  # nearly horizontal
                return True
    return False

def detect_stop(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    stops = stop_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    for (x, y, w, h) in stops:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
        # Text positioning
        text = "STOP"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + text_size[1] + 5
        if text_y > frame.shape[0]:
            text_y = y + h - 5
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
    return len(stops) > 0

def detect_obstacle(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    obstacles = obstacle_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    for (x, y, w, h) in obstacles:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
        # Text positioning
        text = "OBSTACLE"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + text_size[1] + 5
        if text_y > frame.shape[0]:
            text_y = y + h - 5
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
    return len(obstacles) > 0

# -----------------------------
# Main loop
# -----------------------------
command_names = {
    0: "FORWARD", 1:"RIGHT1",2:"RIGHT2",3:"RIGHT3",
    4:"LEFT1",5:"LEFT2",6:"LEFT3",7:"UTURN",8:"STOP",9:"OBSTACLE"
}
print("Press Enter to start driving...")
input()

print("Starting line following...")
stop_triggered = False
last_command = -1

try:
    while True:
        frame = capture()
        frame_pers = perspective(frame)
        frame_final, frame_final_bgr, frame_final_bgr1 = threshold(frame_pers)

        hist_lane = histogram(frame_final_bgr)
        left_pos, right_pos = lane_finder(hist_lane)
        result = lane_center(frame_final, left_pos, right_pos)

        bottom_gray = cv2.cvtColor(frame_final, cv2.COLOR_RGB2GRAY)[180:240, :]
        horizontal_line_detected = detect_horizontal_line(bottom_gray)

        # STOP sign detection
        stop_found = detect_stop(frame)

        # OBSTACLE detection
        obstacle_found = detect_obstacle(frame)

        if stop_found:
            send_command(8)  # STOP
            print("STOP sign detected - stopping for 3 sec")
            time.sleep(3)
            continue

        if obstacle_found:
            send_command(9)  # OBSTACLE
            print("Obstacle detected - stopping for 2 sec")
            time.sleep(2)
            continue

        command = determine_command(result, horizontal_line_detected)
        if command != last_command:
            send_command(command)
            last_command = command

        action = command_names.get(command, "UNKNOWN")
        cv2.putText(frame, f"Result: {result}", (5,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1)
        cv2.putText(frame, f"Cmd: {command} ({action})", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),1)

        # Display windows
        cv2.imshow("Original + Detections", frame)
        cv2.imshow("Perspective", frame_pers)
        cv2.imshow("Final", frame_final)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            send_command(8)  # Stop
            break

        time.sleep(0.03)

except KeyboardInterrupt:
    print("\nShutting down...")
    send_command(8)

finally:
    cv2.destroyAllWindows()
    picam2.close()
    print("System shutdown complete")
