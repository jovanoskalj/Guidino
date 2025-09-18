from picamera2 import Picamera2
import cv2
import time
import os

# Set path where you want to save images
save_path = "/home/robot/Desktop/SamplesObject"

# Make sure the directory exists
if not os.path.exists(save_path):
    os.makedirs(save_path)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (400, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

time.sleep(2)

print("Press 's' to take a photo, 'q' to quit.")

image_count = 0
max_images = 299

while image_count < max_images:
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    cv2.imshow("Camera Preview", gray)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = f"{save_path}/Positive{image_count}.jpg"
        success = cv2.imwrite(filename, gray)
        if success:
            print(f"Saved: {filename}")
            image_count += 1
        else:
            print(f"Failed to save: {filename}")

    elif key == ord('q'):
        print("Quitting.")
        break

cv2.destroyAllWindows()
print("Done.")
