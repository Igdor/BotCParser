import time
import logging

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
        logging.info("Firefox webdriver loaded")

    except Exception as err:
        logging.warning("Firefox error: " + str(err))
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            logging.info("Chrome webdriver loaded")
        except Exception as err:
            logging.error("Chrome error:" + str(err))
            return "No"

    return driver


def get_source_data(link):
    driver = driver_start()
    if driver == "No":
        logging.error("Webdriver initialisation failed")
        return "No"
    driver.implicitly_wait(15)

    driver.get(link)
    try:
        elem = WebDriverWait(driver, 30).until(exp.presence_of_element_located((By.ID, "content-reveal-grimoire-to-all-tooltip")))
        time.sleep(5)
    except Exception as error:
        logging.error("Wrong link")
        return "No"
    # if player link used, this will press "reveal grimoire" button
    try:
        driver.find_element(By.XPATH, '//button[normalize-space()="Reveal Grimoire"]').click()
        time.sleep(2)
    except Exception as error:
        logging.warning("'Reveal Grimoire' button not found: " + str(error))

    page_source = driver.page_source
    driver.close()

    return page_source
