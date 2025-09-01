import os
import tempfile
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Selenium fixture for Chrome
@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore self-signed HTTPS
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Create a unique temp profile to avoid session conflicts
    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


def test_dashboard_title(driver):
    """Check Wazuh dashboard title."""
    dashboard_url = os.getenv("DASHBOARD_URL", "https://20.220.18.183")
    driver.get(dashboard_url)

    # Wait until page title contains "Wazuh"
    WebDriverWait(driver, 10).until(lambda d: "Wazuh" in d.title)
    assert "Wazuh" in driver.title, f"Unexpected page title: {driver.title}"


def test_login_form_elements(driver):
    """Check Wazuh login form elements."""
    dashboard_url = os.getenv("DASHBOARD_URL", "https://20.220.18.183/app/login")
    driver.get(dashboard_url)

    # Wait for username input
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )

    assert username_input.is_displayed()
    assert password_input.is_displayed()
    assert login_button.is_displayed()
