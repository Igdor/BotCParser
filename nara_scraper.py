import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp
from dotenv import dotenv_values

config = dotenv_values("settings.env")


def driver_start():
    try:
        options = webdriver.FirefoxOptions()
        options.binary_location = config.get("FF_PATH")
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)

    except Exception as err:
        print("Firefox error: " + str(err))
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

    return driver


def get_source_data(link):
    driver = driver_start()
    driver.implicitly_wait(15)

    driver.get(link)
    # waiting for page to fully load all JS
    elem = WebDriverWait(driver, 30).until(
        exp.presence_of_element_located((By.ID, "content-reveal-grimoire-to-all-tooltip")))
    time.sleep(5)
    # if player link used, this required to press "reveal grimoire" button
    try:
        driver.find_element(By.XPATH, '//button[normalize-space()="Reveal Grimoire"]').click()
        time.sleep(2)
    except Exception as error:
        print("No button found: " + str(error))

    page_source = driver.page_source
    driver.close()

    return page_source
