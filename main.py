from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import datetime
import telegram_send
import pytz

tz = pytz.timezone('Asia/Kolkata')

def send(msg):
    telegram_send.send(messages=[msg])

def get_timediff(start, end):
    elapsedTime = end - start
    min, sec = divmod(elapsedTime.total_seconds(), 60)
    if min == 0:
        return f"{int(sec)} seconds"
    else:
        return f"{int(min)} minutes {int(sec)} seconds"


os.system('printf "1864074321:AAGI08sTSospH1Q6KmfGZ3ghTrhiVvQWRd0\npub\nt.me/watsonBro" | telegram-send --configure-channel')  # watson bot
send("deployed...")

# XPath selectors
# NEW_CHAT_BTN = '//div[@class=\'sbcXq\']//div[2]//div[1]//span[1]'
NEW_CHAT_BTN = '//*[@id="side"]/header/div[2]/div/span/div[2]'
# INPUT_TXT_BOX = '//div[@class=\'_1KDYa _14Mgc copyable-area\']//div//input[@class=\'_2zCfw copyable-text selectable-text\']'
INPUT_TXT_BOX = '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[1]/div/label/div/div[2]'
# ONLINE_STATUS_LABEL = '//span[@class=\'_315-i _F7Vk\']'
ONLINE_STATUS_LABEL = '//*[@id="main"]/header/div[2]/div[2]/span'
# Replace below with the list of targets to be tracked
TARGETS = {'"Self"': '+919002320075'} #{'"Self"': '+919002320075', '"contactName2"': 'phoneNumber2'}

# Replace below path with the absolute path
browser = webdriver.Chrome(r'/Users/ashish.ranjan/Documents/chromedriver')

# Load Whatsapp Web page
browser.get("https://web.whatsapp.com/")
wait = WebDriverWait(browser, 600)
os.system('export TERM=${TERM:-dumb}')




is_online = False
is_first_run = True
start_time = None
end_time = None
while True:
    # Clear screen
    # os.system('clear')

    # For each target
    for target in TARGETS:
        tryAgain = True

        # Wait untill new chat button is visible
        new_chat_title = wait.until(EC.presence_of_element_located((By.XPATH, NEW_CHAT_BTN)))

        while tryAgain:
            try:
                # Click on new chat button
                new_chat_title.click()

                # Wait untill input text box is visible
                input_box = wait.until(EC.presence_of_element_located((By.XPATH, INPUT_TXT_BOX)))

                time.sleep(0.5)

                # Write phone number
                input_box.send_keys(TARGETS[target])

                time.sleep(1)

                # Press enter to confirm the phone number
                input_box.send_keys(Keys.ENTER)

                time.sleep(5)
                tryAgain = False

                try:
                    try:
                        browser.find_element_by_xpath(ONLINE_STATUS_LABEL)
                        # print(target + ' is online')
                        if (not is_online) or (is_first_run):
                            start_time = datetime.datetime.now(tz)
                            send("came online")
                        is_online = True
                    except:
                        if is_online:
                            end_time = datetime.datetime.now(tz)
                            send(f"""{start_time.strftime("%H:%M:%S")}\t till {end_time.strftime("%H:%M:%S")}""")
                            send(get_timediff(start_time, end_time)+'\n')
                        is_online = False
                        # print(target + ' is offline')
                    is_first_run = False
                    time.sleep(1)
                except Exception as e:
                    print(f'Exception 1\n{e}')
                    time.sleep(10)
            except Exception as e:
                print(f'Exception 2\n{e}')
                time.sleep(4)

