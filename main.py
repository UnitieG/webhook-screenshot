import time
import pyautogui
import requests
from PIL import ImageGrab
import os
import json

def load_the_config_pls():
    with open("config.json", "r") as f:
        return json.load(f)
    
def take_screenshot_and_send(webhook_url):
    # Take screenshot
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")

    # Send screenshot to Discord webhook
    with open("screenshot.png", "rb") as f:
        file = {"file": f}
        payload = {
            "content": "Screenshot captured at {}".format(time.strftime("%Y-%m-%d %H:%M:%S"))
        }
        requests.post(webhook_url, data=payload, files=file)

    # Remove the screenshot file after sending
    os.remove("screenshot.png")

def main():
    config = load_the_config_pls()
    webhook_url = config.get("webhook")

    if not webhook_url:
        print("Invalid Configuration, Webhook URL not found on the config.json")
        return
                
    timer = float(config.get("timer", 0.5))  # Convert timer to float

    while True:
        try:
            print("Screenshot was sent at " + format(time.strftime("%Y-%m-%d %H:%M:%S")))
            take_screenshot_and_send(webhook_url)
            time.sleep(timer)  # Wait for the specified timer
        except KeyboardInterrupt:
            print("Program terminated by user.")
            payload = {
                "content": "The program has been terminated by the user."
            }
            requests.post(webhook_url, data=payload)
            break
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()
