import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import json

def scrape(url):
    # Define Chrome options
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--no-sandbox")
    # Add more options here if needed

    # Define paths
    user_home_dir = os.path.expanduser("~")
    chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
    chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

    # Set binary location and service
    chrome_options.binary_location = chrome_binary_path
    service = Service(chromedriver_path)


    driver = webdriver.Chrome(service=service, options=chrome_options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )

    driver.get(url)

    result = driver.find_element(By.XPATH, "/html/body").text

    driver.close()

    return json.loads(result)
