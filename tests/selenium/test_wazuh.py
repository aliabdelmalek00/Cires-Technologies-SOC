import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


def test_dashboard_https(driver):
    dashboard_url = os.getenv("DASHBOARD_URL", "https://20.220.18.183/")  
    driver.get(dashboard_url)

    # Check if using HTTPS
    assert dashboard_url.startswith("https://"), "Dashboard must be served over HTTPS"


def test_login_form_elements(driver):
    dashboard_url = os.getenv("DASHBOARD_URL", "https://20.220.18.183/app/login")
    driver.get(dashboard_url)

    # Wait up to 10 seconds for username input to appear
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    assert username_input.is_displayed()
    assert password_input.is_displayed()
    assert login_button.is_displayed()

    # Check login button
    login_button = driver.find_element(By.TAG_NAME, "button")
    assert login_button.is_displayed()




