# %%
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from ultralytics import YOLO
import shutil

N_IMAGES = 20
TRIGGER_ANIMALS = set(["horse", "elephant", "cow", "bear"])
N_IMAGES_WITH_TRIGGER_ANIMALS_TO_TRIGGER = 3


def predict(model):
    results = model(["./input_algar/{i}.png" for i in range(N_IMAGES)])
    total_results = []
    for result in results:
        result_animal = 0
        for box in result.boxes:
            name_index = int(box.cls[0].item())
            if result.names[name_index] in TRIGGER_ANIMALS:
                result_animal = 1
        total_results.append(result_animal)
    if total_results > 3:
        return True
    return False


def delete_old_images():
    for file in os.listdir("runs/detect/predict"):
        os.remove(file)


def move_possible_moose_files():
    possible_moose_images = os.listdir("result/")
    for index, file in enumerate(os.listdir("runs/detect/predict")):
        shutil.move(file, f"result/{len(possible_moose_images)+index+1}.png")


def capture_frames(interval, stream_url):
    model = YOLO("models/yolov8x.pt")
    driver = webdriver.Chrome()
    driver.get(stream_url)
    time.sleep(5)
    accept_button = driver.find_element(By.CLASS_NAME, "c6ead1144")
    driver.execute_script("arguments[0].click();", accept_button)
    time.sleep(5)
    play_button = driver.find_element(By.CLASS_NAME, "sc-6bf77590-2")
    driver.execute_script("arguments[0].click();", play_button)
    time.sleep(5)
    while True:
        for i in range(N_IMAGES):
            driver.save_screenshot(f"/input_algar/{i}.png")
            time.sleep(interval)
        should_email = predict(model=model)
        if should_email:
            print("Animal JaoI")
            move_possible_moose_files()
        if not should_email:
            delete_old_images()


stream_url = (
    "https://www.svtplay.se/video/jN3XL2B/den-stora-algvandringen/idag-00-00?id=jN3XL2B"
)
interval = 3  # Interval in seconds
capture_frames(interval, stream_url)
