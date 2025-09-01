import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


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
    dashboard_url = os.getenv("DASHBOARD_URL", "https://20.220.18.183/")
    driver.get(dashboard_url)

    # Check username field
    username_input = driver.find_element(By.NAME, "username")
    assert username_input.is_displayed()

    # Check password field
    password_input = driver.find_element(By.NAME, "password")
    assert password_input.is_displayed()

    # Check login button
    login_button = driver.find_element(By.TAG_NAME, "button")
    assert login_button.is_displayed()

