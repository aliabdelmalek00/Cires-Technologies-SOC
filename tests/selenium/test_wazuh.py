import os
import tempfile
import json
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -----------------------------
# Configuration via environment variables
# -----------------------------
WAZUH_URL = os.getenv("WAZUH_URL", "https://20.220.18.183")
API_URL = os.getenv("WAZUH_API_URL", "https://20.220.18.183:55000")
TEST_USERNAME = os.getenv("kibanaserver")
TEST_PASSWORD = os.getenv("kibanaserver")


# -----------------------------
# Pytest fixture for Selenium Chrome driver
# -----------------------------
@pytest.fixture(scope="session")
def chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Unique temporary user data directory to avoid session conflicts
    tmp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={tmp_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


# -----------------------------
# UI Tests
# -----------------------------
def test_dashboard_https_and_login_elements(chrome_driver):
    chrome_driver.get(WAZUH_URL)

    # Check HTTPS
    assert chrome_driver.current_url.startswith("https://"), "Dashboard is not HTTPS"

    # Check page title
    assert "Wazuh" in chrome_driver.title, f"Unexpected page title: {chrome_driver.title}"

    # Wait for login form
    wait = WebDriverWait(chrome_driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    assert username_field.is_displayed() and password_field.is_displayed() and login_button.is_displayed(), \
        "Login form elements are not visible"


@pytest.mark.skipif(not (TEST_USERNAME and TEST_PASSWORD), reason="No test credentials provided")
def test_dashboard_login(chrome_driver):
    chrome_driver.get(WAZUH_URL)
    wait = WebDriverWait(chrome_driver, 10)

    # Fill in login form
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    username_field.send_keys(TEST_USERNAME)
    password_field.send_keys(TEST_PASSWORD)
    login_button.click()

    # Check landing page element after login
    landing_panel = wait.until(EC.presence_of_element_located((By.ID, "dashboard-main-panel")))
    assert landing_panel.is_displayed(), "Landing panel not found after login"


# -----------------------------
# API Health Check
# -----------------------------
def test_wazuh_api_health():
    try:
        response = requests.get(f"{API_URL}/manager/info", verify=False, timeout=5)
        assert response.status_code == 200, f"API returned status {response.status_code}"

        data = response.json()
        assert "version" in data, "Missing 'version' in API response"
        assert "cluster_name" in data, "Missing 'cluster_name' in API response"
    except Exception as e:
        pytest.fail(f"API health check failed: {e}")
