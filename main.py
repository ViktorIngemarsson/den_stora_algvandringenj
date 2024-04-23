# %%
import cv2
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# Function to capture frames from the livestream at intervals
def capture_frames(interval, stream_url):
    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()  # You need to have chromedriver installed
    driver.get(stream_url)
    # Wait for the play button to appear and click it
    driver.implicitly_wait(2)
    time.sleep(5)  # Adjust as needed

    accept_button = driver.find_element(By.CLASS_NAME, "c6ead1144")
    driver.execute_script("arguments[0].click();", accept_button)

    # accept_button.click()
    time.sleep(5)  # Adjust as needed

    play_button = driver.find_element(
        By.CLASS_NAME, "sc-6bf77590-2"
    )  # Use the class name of the play button
    driver.execute_script("arguments[0].click();", play_button)

    # Allow some time for the livestream to start
    time.sleep(5)  # Adjust as needed
    driver.save_screenshot("ss.png")
    # Initialize OpenCV capture
    current_url = driver.current_url

    cap = cv2.VideoCapture(current_url, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("Error: Failed to open video stream")
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()

        # Check if the frame is captured successfully
        if not ret:
            print("Error: Failed to capture frame")
            break

        # Save the frame
        frame_count += 1
        filename = f"frame_{frame_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved frame {frame_count}")

        # Wait for the specified interval
        time.sleep(interval)

    cap.release()
    cv2.destroyAllWindows()
    driver.quit()


# Example usage

stream_url = (
    "https://www.svtplay.se/video/jN3XL2B/den-stora-algvandringen/idag-00-00?id=jN3XL2B"
)
interval = 3  # Interval in seconds
capture_frames(interval, stream_url)

# %%
#### Identify moose

from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("models/yolov8x.pt")
# %%
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
results = model.predict(source="0")
results = model.predict(
    source="folder", show=True
)  # Display preds. Accepts all YOLO predict arguments

# %%
# from PIL
im1 = Image.open(f"./input_algar/10.png")
results = model.predict(source=im1, save=True)

# %%
results = model("./input_algar/10.png")
# %%
for r in results:
    for box in r.boxes:
        print(box.cls[0])
# %%
