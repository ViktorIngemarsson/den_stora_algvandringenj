# %%
import datetime
import os
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from ultralytics import YOLO
import shutil

N_IMAGES = 20
TRIGGER_ANIMALS = set(["horse", "elephant", "cow", "bear"])
N_IMAGES_WITH_TRIGGER_ANIMALS_TO_TRIGGER = 3


def predict():
    model = YOLO("models/yolov8x.pt")
    while True:
        input_images = os.listdir("./input_algar/")
        if len(input_images) == 0:
            time.sleep(2)
            continue
        input_images = ["input_algar/" + image_name for image_name in input_images]
        results = model(input_images)
        for image_index, result in enumerate(results):
            found_moose = False
            for box in result.boxes:
                name_index = int(box.cls[0].item())
                if result.names[name_index] in TRIGGER_ANIMALS:
                    new_file_location = input_images[image_index].replace(
                        "input_algar", "result"
                    )
                    shutil.move(input_images[image_index], f"{new_file_location}.png")
                    found_moose = True
                    break
            if not found_moose:
                os.remove(input_images[image_index])
        time.sleep(2)


def capture_frames(interval, stream_url):
    driver = webdriver.Chrome()
    driver.get(stream_url)
    time.sleep(5)
    accept_button = driver.find_element(By.CLASS_NAME, "c6ead1144")
    driver.execute_script("arguments[0].click();", accept_button)
    play_button = driver.find_element(By.CLASS_NAME, "sc-6bf77590-2")
    driver.execute_script("arguments[0].click();", play_button)
    t1 = threading.Thread(target=predict)
    t1.start()
    while True:
        driver.save_screenshot(
            f"./input_algar/{str(int(datetime.datetime.now().timestamp()))}.png"
        )
        time.sleep(interval)


stream_url = (
    "https://www.svtplay.se/video/jN3XL2B/den-stora-algvandringen/idag-00-00?id=jN3XL2B"
)
interval = 5  # Interval in seconds
capture_frames(interval, stream_url)

# %%
